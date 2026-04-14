"""
АНАЛИЗ ДАННЫХ — Визуализация и статистика
===========================================
На олимпиаде нужно не только строить ML-модели,
но и уметь исследовать, визуализировать и делать выводы.

Этот файл покрывает:
1. Основные типы графиков для анализа данных
2. Статистические тесты
3. A/B тестирование
4. Исследовательский анализ (EDA)

Установка: pip install pandas numpy matplotlib seaborn scipy
"""

import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
from scipy import stats

# Настройка стиля графиков
sns.set_style("whitegrid")
plt.rcParams['font.size'] = 11

# ============================================================
# ЧАСТЬ 1: Генерация датасета для анализа
# ============================================================

print("=" * 60)
print("ГЕНЕРАЦИЯ ДАННЫХ ДЛЯ АНАЛИЗА")
print("=" * 60)

np.random.seed(42)

# Датасет: Продажи интернет-магазина за 6 месяцев
n = 1000

sales_data = pd.DataFrame({
    'date': pd.date_range('2024-01-01', periods=n, freq='D'),
    'product_category': np.random.choice(['Электроника', 'Одежда', 'Книги', 'Еда', 'Спорт'], n),
    'price': np.random.exponential(3000, n).clip(100, 20000),
    'quantity': np.random.randint(1, 10, n),
    'customer_age': np.random.normal(35, 12, n).clip(18, 70).astype(int),
    'customer_gender': np.random.choice(['М', 'Ж'], n, p=[0.52, 0.48]),
    'city': np.random.choice(['Минск', 'Гомель', 'Могилёв', 'Витебск', 'Гродно', 'Брест'], n, 
                              p=[0.35, 0.15, 0.12, 0.13, 0.13, 0.12]),
    'discount_percent': np.random.choice([0, 5, 10, 15, 20], n, p=[0.3, 0.2, 0.2, 0.2, 0.1]),
    'is_return': np.random.choice([0, 1], n, p=[0.9, 0.1]),
    'rating': np.random.choice([1, 2, 3, 4, 5], n, p=[0.05, 0.08, 0.15, 0.35, 0.37])
})

# Выручка
sales_data['revenue'] = sales_data['price'] * sales_data['quantity'] * (1 - sales_data['discount_percent'] / 100)

print(f"Размер: {sales_data.shape}")
print(f"\nПервые 5 строк:")
print(sales_data.head())
print(f"\nТипы данных:")
print(sales_data.dtypes)

# ============================================================
# ЧАСТЬ 2: Базовый EDA
# ============================================================

print("\n" + "=" * 60)
print("ЧАСТЬ 2: БАЗОВЫЙ EDA")
print("=" * 60)

# Общая информация
print("\n--- Общая информация ---")
print(f"Период: {sales_data['date'].min()} — {sales_data['date'].max()}")
print(f"Всего заказов: {len(sales_data)}")
print(f"Уникальных категорий: {sales_data['product_category'].nunique()}")
print(f"Уникальных городов: {sales_data['city'].nunique()}")

# Статистика числовых
print("\n--- Статистика числовых ---")
numeric_cols = ['price', 'quantity', 'revenue', 'customer_age', 'discount_percent', 'rating']
print(sales_data[numeric_cols].describe().round(2))

# Категориальные
print("\n--- Распределение категорий ---")
print("Категории товаров:")
print(sales_data['product_category'].value_counts())
print(f"\nГорода:")
print(sales_data['city'].value_counts())
print(f"\nВозвраты: {sales_data['is_return'].mean():.1%}")

# ============================================================
# ЧАСТЬ 3: Визуализация — распределения
# ============================================================

print("\n" + "=" * 60)
print("ЧАСТЬ 3: ВИЗУАЛИЗАЦИЯ — РАСПРЕДЕЛЕНИЯ")
print("=" * 60)

fig, axes = plt.subplots(2, 2, figsize=(14, 10))

# 1. Гистограмма цены
axes[0, 0].hist(sales_data['price'], bins=50, color='skyblue', edgecolor='black', alpha=0.7)
axes[0, 0].set_title('Распределение цены товара')
axes[0, 0].set_xlabel('Цена (руб.)')
axes[0, 0].set_ylabel('Частота')

# 2. Гистограмма выручки
axes[0, 1].hist(sales_data['revenue'], bins=50, color='lightgreen', edgecolor='black', alpha=0.7)
axes[0, 1].set_title('Распределение выручки')
axes[0, 1].set_xlabel('Выручка (руб.)')
axes[0, 1].set_ylabel('Частота')

# 3. Возраст клиентов
axes[1, 0].hist(sales_data['customer_age'], bins=30, color='salmon', edgecolor='black', alpha=0.7)
axes[1, 0].set_title('Распределение возраста клиентов')
axes[1, 0].set_xlabel('Возраст')
axes[1, 0].set_ylabel('Частота')
axes[1, 0].axvline(sales_data['customer_age'].mean(), color='red', linestyle='--', 
                   label=f"Средний: {sales_data['customer_age'].mean():.1f}")
axes[1, 0].legend()

# 4. Boxplot цены по категориям
sales_data.boxplot(column='price', by='product_category', ax=axes[1, 1])
axes[1, 1].set_title('Цена по категориям')
axes[1, 1].set_xlabel('Категория')
axes[1, 1].set_ylabel('Цена (руб.)')
plt.sca(axes[1, 1])
plt.xticks(rotation=45)

plt.suptitle('')
plt.tight_layout()
plt.savefig('C:\\it chalenge\\data_analysis\\01_distributions.png', dpi=150)
print("График сохранён: 01_distributions.png")

# ============================================================
# ЧАСТЬ 4: Визуализация — сравнения
# ============================================================

print("\n" + "=" * 60)
print("ЧАСТЬ 4: ВИЗУАЛИЗАЦИЯ — СРАВНЕНИЯ")
print("=" * 60)

fig, axes = plt.subplots(2, 2, figsize=(14, 10))

# 1. Средняя выручка по категориям
category_revenue = sales_data.groupby('product_category')['revenue'].mean().sort_values(ascending=False)
axes[0, 0].bar(category_revenue.index, category_revenue.values, color='steelblue', alpha=0.7)
axes[0, 0].set_title('Средняя выручка по категориям')
axes[0, 0].set_xlabel('Категория')
axes[0, 0].set_ylabel('Выручка (руб.)')
plt.sca(axes[0, 0])
plt.xticks(rotation=45)

# 2. Выручка по городам (boxplot)
sales_data.boxplot(column='revenue', by='city', ax=axes[0, 1])
axes[0, 1].set_title('Выручка по городам')
axes[0, 1].set_xlabel('Город')
axes[0, 1].set_ylabel('Выручка (руб.)')
plt.sca(axes[0, 1])
plt.xticks(rotation=45)

# 3. Влияние скидки на выручку
discount_rev = sales_data.groupby('discount_percent').agg({
    'revenue': 'mean',
    'quantity': 'mean'
}).round(2)
axes[1, 0].plot(discount_rev.index, discount_rev['revenue'], 'bo-', linewidth=2, markersize=8, label='Выручка')
axes[1, 0].set_title('Влияние скидки на среднюю выручку')
axes[1, 0].set_xlabel('Скидка (%)')
axes[1, 0].set_ylabel('Средняя выручка (руб.)', color='b')
axes[1, 0].grid(True, alpha=0.3)

# 4. Распределение оценок
rating_counts = sales_data['rating'].value_counts().sort_index()
colors = ['#ff4444', '#ff8844', '#ffcc44', '#88cc44', '#44aa44']
axes[1, 1].bar(rating_counts.index, rating_counts.values, color=colors, alpha=0.7, edgecolor='black')
axes[1, 1].set_title('Распределение оценок')
axes[1, 1].set_xlabel('Оценка')
axes[1, 1].set_ylabel('Количество')
axes[1, 1].set_xticks(range(1, 6))

plt.suptitle('')
plt.tight_layout()
plt.savefig('C:\\it chalenge\\data_analysis\\02_comparisons.png', dpi=150)
print("График сохранён: 02_comparisons.png")

# ============================================================
# ЧАСТЬ 5: Визуализация — корреляции
# ============================================================

print("\n" + "=" * 60)
print("ЧАСТЬ 5: ВИЗУАЛИЗАЦИЯ — КОРРЕЛЯЦИИ")
print("=" * 60)

# Корреляционная матрица
corr_cols = ['price', 'quantity', 'discount_percent', 'customer_age', 'rating', 'revenue']
corr_matrix = sales_data[corr_cols].corr()

print("\nКорреляционная матрица:")
print(corr_matrix.round(3))

fig, axes = plt.subplots(1, 2, figsize=(16, 6))

# Heatmap
sns.heatmap(corr_matrix, annot=True, cmap='coolwarm', center=0, fmt='.2f', 
            linewidths=0.5, ax=axes[0])
axes[0].set_title('Корреляционная матрица')

# Scatter plot: скидка vs количество
axes[1].scatter(sales_data['discount_percent'], sales_data['quantity'], alpha=0.3, s=20)
axes[1].set_title('Скидка vs Количество')
axes[1].set_xlabel('Скидка (%)')
axes[1].set_ylabel('Количество')
axes[1].grid(True, alpha=0.3)

# Линия тренда
z = np.polyfit(sales_data['discount_percent'], sales_data['quantity'], 1)
p = np.poly1d(z)
x_line = np.linspace(0, 20, 100)
axes[1].plot(x_line, p(x_line), "r--", alpha=0.8, label=f'Тренд: y={z[0]:.3f}x+{z[1]:.2f}')
axes[1].legend()

plt.tight_layout()
plt.savefig('C:\\it chalenge\\data_analysis\\03_correlations.png', dpi=150)
print("График сохранён: 03_correlations.png")

# ============================================================
# ЧАСТЬ 6: Временной анализ
# ============================================================

print("\n" + "=" * 60)
print("ЧАСТЬ 6: ВРЕМЕННОЙ АНАЛИЗ")
print("=" * 60)

# Группировка по дням
daily_sales = sales_data.groupby('date').agg({
    'revenue': 'sum',
    'quantity': 'sum',
    'price': 'mean'
}).reset_index()

# Скользящее среднее (7 дней)
daily_sales['revenue_ma7'] = daily_sales['revenue'].rolling(window=7).mean()

fig, axes = plt.subplots(2, 1, figsize=(14, 8))

# Выручка по дням
axes[0].plot(daily_sales['date'], daily_sales['revenue'], alpha=0.3, color='gray', label='Ежедневно')
axes[0].plot(daily_sales['date'], daily_sales['revenue_ma7'], color='red', linewidth=2, label='Скользящее среднее (7 дней)')
axes[0].set_title('Выручка по дням')
axes[0].set_xlabel('Дата')
axes[0].set_ylabel('Выручка (руб.)')
axes[0].legend()
axes[0].grid(True, alpha=0.3)

# Количество заказов по дням
axes[1].plot(daily_sales['date'], daily_sales['quantity'], alpha=0.5, color='steelblue')
axes[1].set_title('Количество проданных товаров по дням')
axes[1].set_xlabel('Дата')
axes[1].set_ylabel('Количество')
axes[1].grid(True, alpha=0.3)

plt.tight_layout()
plt.savefig('C:\\it chalenge\\data_analysis\\04_time_series.png', dpi=150)
print("График сохранён: 04_time_series.png")

# Статистика по месяцам
sales_data['month'] = sales_data['date'].dt.month
monthly = sales_data.groupby('month').agg({
    'revenue': 'sum',
    'quantity': 'sum'
}).round(0)
print("\nВыручка по месяцам:")
print(monthly)

# ============================================================
# ЧАСТЬ 7: Статистические тесты
# ============================================================

print("\n" + "=" * 60)
print("ЧАСТЬ 7: СТАТИСТИЧЕСКИЕ ТЕСТЫ")
print("=" * 60)

# --- Тест 1: Сравнение средних (t-test) ---
print("\n--- 1. T-тест: разница выручки М vs Ж ---")

male_rev = sales_data[sales_data['customer_gender'] == 'М']['revenue']
female_rev = sales_data[sales_data['customer_gender'] == 'Ж']['revenue']

t_stat, p_value = stats.ttest_ind(male_rev, female_rev)
print(f"Средняя выручка М: {male_rev.mean():.2f} руб.")
print(f"Средняя выручка Ж: {female_rev.mean():.2f} руб.")
print(f"t-statistic: {t_stat:.4f}")
print(f"p-value: {p_value:.6f}")
print(f"Вывод: {'Разница значима' if p_value < 0.05 else 'Разница НЕ значима'} (α=0.05)")

# --- Тест 2: ANOVA (сравнение нескольких групп) ---
print("\n--- 2. ANOVA: разница выручки по городам ---")

city_groups = [group['revenue'].values for name, group in sales_data.groupby('city')]
f_stat, p_value_anova = stats.f_oneway(*city_groups)

print(f"F-statistic: {f_stat:.4f}")
print(f"p-value: {p_value_anova:.6f}")
print(f"Вывод: {'Разница значима' if p_value_anova < 0.05 else 'Разница НЕ значима'} (α=0.05)")

if p_value_anova < 0.05:
    print("  → Хотя бы один город отличается от остальных")

# --- Тест 3: Хи-квадрат (связь категориальных) ---
print("\n--- 3. Хи-квадрат: связь категории и возвратов ---")

contingency = pd.crosstab(sales_data['product_category'], sales_data['is_return'])
print(f"\nТаблица сопряжённости:")
print(contingency)

chi2, p_value_chi2, dof, expected = stats.chi2_contingency(contingency)
print(f"\nχ² = {chi2:.4f}")
print(f"p-value = {p_value_chi2:.6f}")
print(f"Степени свободы = {dof}")
print(f"Вывод: {'Связь значима' if p_value_chi2 < 0.05 else 'Связь НЕ значима'} (α=0.05)")

# --- Тест 4: Проверка нормальности ---
print("\n--- 4. Тест Шапиро-Уилка: нормальность распределения ---")

# Берём подвыборку (тест чувствителен к размеру)
sample = sales_data['revenue'].sample(n=100, random_state=42)
stat, p_value_shapiro = stats.shapiro(sample)
print(f"Статистика: {stat:.4f}")
print(f"p-value: {p_value_shapiro:.6f}")
print(f"Вывод: {'Нормальное' if p_value_shapiro > 0.05 else 'НЕ нормальное'} распределение (α=0.05)")

# --- Тест 5: Корреляция Пирсона ---
print("\n--- 5. Корреляция Пирсона: скидка vs количество ---")

r, p_value_pearson = stats.pearsonr(sales_data['discount_percent'], sales_data['quantity'])
print(f"r = {r:.4f}")
print(f"p-value = {p_value_pearson:.6f}")
print(f"Вывод: {'Корреляция значима' if p_value_pearson < 0.05 else 'Корреляция НЕ значима'}")
print(f"Сила: {'слабая' if abs(r) < 0.3 else 'средняя' if abs(r) < 0.7 else 'сильная'}")

# ============================================================
# ЧАСТЬ 8: A/B тестирование
# ============================================================

print("\n" + "=" * 60)
print("ЧАСТЬ 8: A/B ТЕСТИРОВАНИЕ")
print("=" * 60)

# Симуляция A/B теста: две версии сайта
np.random.seed(42)

# Версия A (старая): конверсия 10%
n_a = 1000
conversions_a = np.random.binomial(1, 0.10, n_a)

# Версия B (новая): конверсия 13%
n_b = 1000
conversions_b = np.random.binomial(1, 0.13, n_b)

print("--- A/B Тест: Конверсия ---")
print(f"Версия A: {conversions_a.sum()}/{n_a} = {conversions_a.mean():.1%}")
print(f"Версия B: {conversions_b.sum()}/{n_b} = {conversions_b.mean():.1%}")
print(f"Разница: {(conversions_b.mean() - conversions_a.mean())*100:.1f} п.п.")

# Z-тест для пропорций
from statsmodels.stats.proportion import proportions_ztest

count = np.array([conversions_b.sum(), conversions_a.sum()])
nobs = np.array([n_b, n_a])

z_stat, p_value_ab = proportions_ztest(count, nobs)
print(f"\nz-statistic: {z_stat:.4f}")
print(f"p-value: {p_value_ab:.6f}")
print(f"Вывод: {'Версия B значительно лучше' if p_value_ab < 0.05 and z_stat > 0 else 'Разница НЕ значима'}")

# Визуализация A/B теста
fig, ax = plt.subplots(figsize=(8, 5))
groups = ['Версия A', 'Версия B']
conversions = [conversions_a.mean(), conversions_b.mean()]
colors = ['#3498db', '#2ecc71']

bars = ax.bar(groups, conversions, color=colors, alpha=0.7, edgecolor='black', width=0.5)
ax.set_ylabel('Конверсия')
ax.set_title('A/B Тест: Конверсия версий')
ax.set_ylim(0, 0.20)

# Подписи значений
for bar, val in zip(bars, conversions):
    ax.text(bar.get_x() + bar.get_width()/2, bar.get_height() + 0.005, 
            f'{val:.1%}', ha='center', fontweight='bold')

# Линия значимости
if p_value_ab < 0.05:
    ax.text(0.5, 0.18, '✓ Значимо (p < 0.05)', ha='center', color='green', 
            fontweight='bold', fontsize=12)

ax.grid(True, alpha=0.3, axis='y')
plt.tight_layout()
plt.savefig('C:\\it chalenge\\data_analysis\\05_ab_test.png', dpi=150)
print("График сохранён: 05_ab_test.png")

# ============================================================
# ЧАСТЬ 9: Доверительные интервалы
# ============================================================

print("\n" + "=" * 60)
print("ЧАСТЬ 9: ДОВЕРИТЕЛЬНЫЕ ИНТЕРВАЛЫ")
print("=" * 60)

# Доверительный интервал для среднего
def confidence_interval(data, confidence=0.95):
    """Расчёт доверительного интервала для среднего"""
    n = len(data)
    mean = np.mean(data)
    sem = stats.sem(data)  # Стандартная ошибка среднего
    margin = sem * stats.t.ppf((1 + confidence) / 2, n - 1)
    return mean, margin, (mean - margin, mean + margin)

mean_rev, margin_rev, ci_rev = confidence_interval(sales_data['revenue'])
print(f"\nСредняя выручка: {mean_rev:.2f} руб.")
print(f"95% ДИ: ({ci_rev[0]:.2f}, {ci_rev[1]:.2f})")
print(f"Погрешность: ±{margin_rev:.2f}")

# По категориям
print("\nСредняя выручка по категориям (95% ДИ):")
for cat in sales_data['product_category'].unique():
    cat_data = sales_data[sales_data['product_category'] == cat]['revenue']
    mean, margin, ci = confidence_interval(cat_data)
    print(f"  {cat}: {mean:.0f} руб. (±{margin:.0f})")

# ============================================================
# ЧАСТЬ 10: Сводный отчёт
# ============================================================

print("\n" + "=" * 60)
print("ЧАСТЬ 10: СВОДНЫЙ ОТЧЁТ")
print("=" * 60)

# Ключевые метрики
total_revenue = sales_data['revenue'].sum()
avg_revenue = sales_data['revenue'].mean()
avg_order = sales_data['price'].mean()
return_rate = sales_data['is_return'].mean()
avg_rating = sales_data['rating'].mean()

print(f"""
═══════════════════════════════════════════
       ОТЧЁТ ПО ПРОДАЖАМ
═══════════════════════════════════════════

📊 ОБЩИЕ МЕТРИКИ:
  • Общая выручка:          {total_revenue:,.0f} руб.
  • Средняя выручка/заказ:  {avg_revenue:,.0f} руб.
  • Средняя цена товара:    {avg_order:,.0f} руб.
  • Средний рейтинг:        {avg_rating:.2f}/5.00
  • Процент возвратов:      {return_rate:.1%}

🏆 ЛУЧШАЯ КАТЕГОРИЯ:
  {sales_data.groupby('product_category')['revenue'].mean().idxmax()}: 
  {sales_data.groupby('product_category')['revenue'].mean().max():,.0f} руб. (средняя)

🏆 ЛУЧШИЙ ГОРОД:
  {sales_data.groupby('city')['revenue'].mean().idxmax()}: 
  {sales_data.groupby('city')['revenue'].mean().max():,.0f} руб. (средняя)

📈 СТАТИСТИЧЕСКИЕ ВЫВОДЫ:
  • Пол и выручка: {'значимая разница' if p_value < 0.05 else 'нет значимой разницы'}
  • Города: {'значимые различия' if p_value_anova < 0.05 else 'нет значимых различий'}
  • Категория и возвраты: {'значимая связь' if p_value_chi2 < 0.05 else 'нет значимой связи'}
  • Скидка и количество: {'значимая корреляция' if p_value_pearson < 0.05 else 'нет значимой корреляции'}

═══════════════════════════════════════════
""")

# ============================================================
# ЧАСТЬ 11: Чек-лист EDA для олимпиады
# ============================================================

print("=" * 60)
print("ЧАСТЬ 11: ЧЕК-ЛИСТ EDA")
print("=" * 60)
print("""
✅ 1. Обзор данных:
   • df.info(), df.describe(), df.isna().sum()
   • Размер, типы данных, пропуски

✅ 2. Распределения:
   • Гистограммы для числовых
   • Bar chart для категориальных
   • Boxplot для поиска выбросов

✅ 3. Сравнения:
   • groupby().mean() / sum()
   • Bar chart сравнений
   • Boxplot по группам

✅ 4. Корреляции:
   • df.corr()
   • Heatmap корреляций
   • Scatter plots для пар признаков

✅ 5. Временной анализ (если есть даты):
   • Группировка по дням/месяцам
   • Line plot тренда
   • Скользящее среднее

✅ 6. Статистические тесты:
   • t-test: сравнение 2 групп
   • ANOVA: сравнение 3+ групп
   • Chi-square: связь категориальных
   • Pearson/Spearman: корреляция

✅ 7. Визуализации:
   • Минимум 3-4 графика
   • Подписи осей и заголовки
   • Сохранение в файл

✅ 8. Выводы:
   • Сводный отчёт с ключевыми числами
   • Интерпретация результатов
   • Рекомендации
""")

print("=" * 60)
print("УРОК ЗАВЕРШЁН!")
print("=" * 60)
print("""
Следующие шаги:
1. Изучи cybersecurity/ — основы безопасности
2. Повтори шпаргалку cheatsheets/ml_models_when_to_use.md
3. Попробуй решить задачи самостоятельно без подсказок
""")
