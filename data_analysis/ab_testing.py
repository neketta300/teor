"""
ЗАДАЧА ПО АНАЛИЗУ ДАННЫХ — A/B тестирование
=============================================
Тема: Анализ результатов A/B теста мобильного приложения

УСЛОВИЕ:
Компания запустила A/B тест для новой функции в приложении.
Нужно проанализировать результаты и дать рекомендацию.

ДАННЫЕ:
- user_id: ID пользователя
- group: A (контроль) или B (новая функция)
- converted: 1 если совершил целевое действие, 0 если нет
- session_duration: время сессии (минуты)
- pages_viewed: число просмотрых экранов
- device: тип устройства (iOS/Android)
- day_of_week: день запуска (1-7)

ЗАДАНИЕ:
1. Проанализировать конверсию по группам
2. Проверить статистическую значимость
3. Проанализировать по сегментам (устройства, дни)
4. Рассчитать доверительные интервалы
5. Дать рекомендацию
"""

import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
from scipy import stats

# Настройка стиля
sns.set_style("whitegrid")
plt.rcParams['font.size'] = 11

# ============================================================
# ШАГ 1: Генерация данных
# ============================================================

print("=" * 60)
print("ШАГ 1: ГЕНЕРАЦИЯ ДАННЫХ A/B ТЕСТА")
print("=" * 60)

np.random.seed(42)
n_users = 2000

data = pd.DataFrame({
    'user_id': range(1, n_users + 1),
    'group': np.random.choice(['A', 'B'], n_users),
    'device': np.random.choice(['iOS', 'Android'], n_users, p=[0.45, 0.55]),
    'day_of_week': np.random.randint(1, 8, n_users)
})

# Конверсия: B лучше на ~20%
conv_prob = np.where(data['group'] == 'B', 0.14, 0.11)
data['converted'] = np.random.binomial(1, conv_prob)

# Время сессии зависит от группы и конверсии
data['session_duration'] = np.where(
    data['group'] == 'B',
    np.random.normal(12, 4, n_users),
    np.random.normal(10, 4, n_users)
).clip(1, 30)

# Если конвертировался — сессия длиннее
data['session_duration'] += data['converted'] * np.random.normal(3, 1, n_users)

# Страницы
data['pages_viewed'] = np.random.poisson(5, n_users) + data['converted'] * 2

print(f"Размер: {data.shape}")
print(f"\nПервые 10 строк:")
print(data.head(10))
print(f"\nРаспределение по группам:")
print(data['group'].value_counts())

# ============================================================
# ШАГ 2: Основные метрики
# ============================================================

print("\n" + "=" * 60)
print("ШАГ 2: ОСНОВНЫЕ МЕТРИКИ")
print("=" * 60)

# Конверсия по группам
conversion = data.groupby('group').agg({
    'converted': ['sum', 'mean', 'count'],
    'session_duration': 'mean',
    'pages_viewed': 'mean'
}).round(4)
conversion.columns = ['converted_total', 'conversion_rate', 'total_users', 'avg_duration', 'avg_pages']

print("\nСводка по группам:")
print(conversion)

lift = (conversion.loc['B', 'conversion_rate'] - conversion.loc['A', 'conversion_rate']) / conversion.loc['A', 'conversion_rate']
print(f"\nLift (рост конверсии): {lift:.2%}")

# ============================================================
# ШАГ 3: Статистическая значимость
# ============================================================

print("\n" + "=" * 60)
print("ШАГ 3: СТАТИСТИЧЕСКАЯ ЗНАЧИМОСТЬ")
print("=" * 60)

# Z-тест для пропорций
from statsmodels.stats.proportion import proportions_ztest

count = data.groupby('group')['converted'].sum()
nobs = data.groupby('group')['converted'].count()

z_stat, p_value = proportions_ztest(count.values, nobs.values)

print(f"Конверсия A: {conversion.loc['A', 'conversion_rate']:.2%}")
print(f"Конверсия B: {conversion.loc['B', 'conversion_rate']:.2%}")
print(f"Z-statistic: {z_stat:.4f}")
print(f"P-value: {p_value:.6f}")
print(f"Результат: {'✓ ЗНАЧИМО' if p_value < 0.05 else '✗ НЕ ЗНАЧИМО'} (α = 0.05)")

# Доверительный интервал разницы
def ci_diff_proportions(df, group_col='group', target_col='converted', confidence=0.95):
    """Доверительный интервал разницы пропорций (бутобстрап)"""
    n_bootstraps = 10000
    diffs = []
    
    for _ in range(n_bootstraps):
        sample = df.sample(n=len(df), replace=True)
        p_a = sample[sample[group_col] == 'A'][target_col].mean()
        p_b = sample[sample[group_col] == 'B'][target_col].mean()
        diffs.append(p_b - p_a)
    
    alpha = 1 - confidence
    lower = np.percentile(diffs, 100 * alpha / 2)
    upper = np.percentile(diffs, 100 * (1 - alpha / 2))
    
    return lower, upper

ci_lower, ci_upper = ci_diff_proportions(data)
diff = conversion.loc['B', 'conversion_rate'] - conversion.loc['A', 'conversion_rate']
print(f"\nРазница конверсий: {diff:.4f}")
print(f"95% ДИ разницы: ({ci_lower:.4f}, {ci_upper:.4f})")
print(f"Вывод: {'ДИ не содержит 0 → значимо' if ci_lower > 0 else 'ДИ содержит 0 → не значимо'}")

# ============================================================
# ШАГ 4: Анализ по сегментам
# ============================================================

print("\n" + "=" * 60)
print("ШАГ 4: АНАЛИЗ ПО СЕГМЕНТАМ")
print("=" * 60)

# По устройствам
print("\n--- По устройствам ---")
device_conv = data.groupby(['group', 'device']).agg({
    'converted': ['mean', 'count']
}).round(4)
device_conv.columns = ['conversion_rate', 'users']
print(device_conv)

# По дням недели
print("\n--- По дням недели ---")
day_conv = data.groupby(['group', 'day_of_week'])['converted'].mean().unstack(0).round(4)
day_conv['diff'] = day_conv['B'] - day_conv['A']
print(day_conv)

# T-тест по времени сессии
print("\n--- T-тест: время сессии ---")
dur_a = data[data['group'] == 'A']['session_duration']
dur_b = data[data['group'] == 'B']['session_duration']
t_stat, p_val_dur = stats.ttest_ind(dur_a, dur_b)
print(f"Среднее A: {dur_a.mean():.2f} мин")
print(f"Среднее B: {dur_b.mean():.2f} мин")
print(f"p-value: {p_val_dur:.6f}")
print(f"Результат: {'✓ ЗНАЧИМО' if p_val_dur < 0.05 else '✗ НЕ ЗНАЧИМО'}")

# ============================================================
# ШАГ 5: Визуализация
# ============================================================

print("\n" + "=" * 60)
print("ШАГ 5: ВИЗУАЛИЗАЦИЯ")
print("=" * 60)

fig, axes = plt.subplots(2, 2, figsize=(14, 10))

# 1. Конверсия по группам
groups = ['A (контроль)', 'B (новая функция)']
rates = [conversion.loc['A', 'conversion_rate'], conversion.loc['B', 'conversion_rate']]
colors = ['#3498db', '#2ecc71']
bars = axes[0, 0].bar(groups, rates, color=colors, alpha=0.7, edgecolor='black', width=0.5)
axes[0, 0].set_title('Конверсия по группам')
axes[0, 0].set_ylabel('Конверсия')
axes[0, 0].set_ylim(0, 0.20)
for bar, val in zip(bars, rates):
    axes[0, 0].text(bar.get_x() + bar.get_width()/2, bar.get_height() + 0.005, 
                    f'{val:.1%}', ha='center', fontweight='bold')
if p_value < 0.05:
    axes[0, 0].text(0.5, 0.17, '✓ Значимо', ha='center', color='green', fontweight='bold')
axes[0, 0].grid(True, alpha=0.3, axis='y')

# 2. Конверсия по устройствам
device_pivot = data.groupby(['group', 'device'])['converted'].mean().unstack(0)
device_pivot.plot(kind='bar', ax=axes[0, 1], color=['#3498db', '#2ecc71'], alpha=0.7)
axes[0, 1].set_title('Конверсия по устройствам')
axes[0, 1].set_ylabel('Конверсия')
axes[0, 1].set_xticklabels(['Android', 'iOS'], rotation=0)
axes[0, 1].legend(['Группа A', 'Группа B'])
axes[0, 1].grid(True, alpha=0.3, axis='y')

# 3. Распределение времени сессии
axes[1, 0].hist(dur_a, bins=30, alpha=0.5, color='#3498db', label='Группа A', density=True)
axes[1, 0].hist(dur_b, bins=30, alpha=0.5, color='#2ecc71', label='Группа B', density=True)
axes[1, 0].set_title('Распределение времени сессии')
axes[1, 0].set_xlabel('Время (минуты)')
axes[1, 0].set_ylabel('Плотность')
axes[1, 0].legend()
axes[1, 0].grid(True, alpha=0.3)

# 4. Конверсия по дням недели
day_diff = (data.groupby(['day_of_week', 'group'])['converted'].mean()
            .unstack(1).assign(diff=lambda x: x['B'] - x['A'])['diff'])
axes[1, 1].bar(day_diff.index, day_diff.values, color=['green' if v > 0 else 'red' for v in day_diff.values], 
               alpha=0.7, edgecolor='black')
axes[1, 1].axhline(y=0, color='black', linewidth=1)
axes[1, 1].set_title('Разница конверсии по дням (B - A)')
axes[1, 1].set_xlabel('День недели')
axes[1, 1].set_ylabel('Разница')
days_ru = {1: 'Пн', 2: 'Вт', 3: 'Ср', 4: 'Чт', 5: 'Пт', 6: 'Сб', 7: 'Вс'}
axes[1, 1].set_xticks(range(1, 8))
axes[1, 1].set_xticklabels([days_ru[d] for d in range(1, 8)])
axes[1, 1].grid(True, alpha=0.3, axis='y')

plt.tight_layout()
plt.savefig('C:\\it chalenge\\data_analysis\\06_ab_analysis.png', dpi=150)
print("График сохранён: 06_ab_analysis.png")

# ============================================================
# ШАГ 6: Итоговая рекомендация
# ============================================================

print("\n" + "=" * 60)
print("ШАГ 6: РЕКОМЕНДАЦИЯ")
print("=" * 60)

# Расчёт бизнес-эффекта
monthly_users = 10000
current_conv = conversion.loc['A', 'conversion_rate']
new_conv = conversion.loc['B', 'conversion_rate']
value_per_conv = 500  # Средняя ценность конверсии

extra_conversions = monthly_users * (new_conv - current_conv)
extra_revenue = extra_conversions * value_per_conv

print(f"""
═══════════════════════════════════════════
       РЕКОМЕНДАЦИЯ ПО A/B ТЕСТУ
═══════════════════════════════════════════

📊 РЕЗУЛЬТАТЫ:
  • Конверсия A: {conversion.loc['A', 'conversion_rate']:.1%}
  • Конверсия B: {conversion.loc['B', 'conversion_rate']:.1%}
  • Lift: {lift:.1%}
  • P-value: {p_value:.6f}
  • 95% ДИ разницы: ({ci_lower:.3f}, {ci_upper:.3f})

📱 ПО СЕГМЕНТАМ:
  • Android A→B: {conversion.loc['A', 'conversion_rate']:.1%} → {conversion.loc['B', 'conversion_rate']:.1%}
  • Время сессии: {'значимо больше в B' if p_val_dur < 0.05 else 'нет значимой разницы'}

💰 БИЗНЕС-ЭФФЕКТ:
  • Дополнительных конверсий/мес: {extra_conversions:.0f}
  • Дополнительная выручка/мес: {extra_revenue:,.0f} руб.

🎯 РЕКОМЕНДАЦИЯ:
  {'✅ РЕКОМЕНДУЕМ запустить версию B для всех пользователей' if p_value < 0.05 else '❌ НЕ РЕКОМЕНДУЕМ — результат не значим'}

═══════════════════════════════════════════
""")

print("=" * 60)
print("ЗАДАЧА ВЫПОЛНЕНА!")
print("=" * 60)
