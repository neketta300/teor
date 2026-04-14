"""
ЗАДАЧА ПО РЕГРЕССИИ — Олимпиадный уровень
==========================================
Тема: Предсказание стоимости автомобилей

УСЛОВИЕ ЗАДАЧИ:
Даны характеристики автомобилей. Нужно предсказать цену продажи.

ВХОДНЫЕ ДАННЫЕ:
- Год выпуска
- Пробег (км)
- Объём двигателя (л)
- Мощность (л.с.)
- Тип топлива (бензин/дизель/электро)

ЗАДАНИЕ:
1. Загрузить и исследовать данные
2. Обработать категориальные признаки
3. Обучить модели регрессии
4. Сравнить метрики (MAE, MSE, R²)
5. Определить самые важные признаки

Установка: pip install pandas numpy scikit-learn matplotlib seaborn
"""

import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
from sklearn.model_selection import train_test_split, cross_val_score
from sklearn.preprocessing import StandardScaler
from sklearn.linear_model import LinearRegression, Ridge, Lasso
from sklearn.ensemble import RandomForestRegressor, GradientBoostingRegressor
from sklearn.metrics import (
    mean_absolute_error, mean_squared_error, r2_score
)

# ============================================================
# ШАГ 1: Генерация датасета
# ============================================================

print("=" * 60)
print("ШАГ 1: ГЕНЕРАЦИЯ ДАННЫХ")
print("=" * 60)

np.random.seed(42)
n_cars = 300

data = pd.DataFrame({
    'year': np.random.randint(2000, 2024, n_cars),
    'mileage_km': np.random.randint(10000, 300000, n_cars),
    'engine_volume': np.random.choice([1.4, 1.6, 2.0, 2.5, 3.0], n_cars),
    'horsepower': np.random.randint(90, 300, n_cars),
    'fuel_type': np.random.choice(['бензин', 'дизель', 'электро'], n_cars, p=[0.6, 0.3, 0.1])
})

# Цена зависит от характеристик + шум
data['price'] = (
    50000 -
    (2024 - data['year']) * 1000 -
    data['mileage_km'] * 0.05 +
    data['engine_volume'] * 2000 +
    data['horsepower'] * 100 +
    np.where(data['fuel_type'] == 'дизель', 2000, 0) +
    np.where(data['fuel_type'] == 'электро', 5000, 0) +
    np.random.normal(0, 3000, n_cars)
)

# Цена не может быть отрицательной
data['price'] = data['price'].clip(lower=5000)

print(f"Размер: {data.shape}")
print(f"\nПервые 10 строк:")
print(data.head(10))
print(f"\nСтатистика:")
print(data.describe())

# ============================================================
# ШАГ 2: EDA
# ============================================================

print("\n" + "=" * 60)
print("ШАГ 2: ИССЛЕДОВАТЕЛЬСКИЙ АНАЛИЗ")
print("=" * 60)

# Корреляция
print("\nКорреляция с ценой:")
corr_with_price = data.corr()['price'].sort_values(ascending=False)
print(corr_with_price)

# Средняя цена по типу топлива
print("\nСредняя цена по типу топлива:")
print(data.groupby('fuel_type')['price'].mean())

# ============================================================
# ШАГ 3: Подготовка данных
# ============================================================

print("\n" + "=" * 60)
print("ШАГ 3: ПОДГОТОВКА ДАННЫХ")
print("=" * 60)

# Кодирование категориального признака
data_encoded = pd.get_dummies(data, columns=['fuel_type'], dtype=int)
print(f"После One-Hot Encoding: {data_encoded.shape}")
print(f"Столбцы: {data_encoded.columns.tolist()}")

# X и y
X = data_encoded.drop('price', axis=1)
y = data_encoded['price']

print(f"\nX shape: {X.shape}")
print(f"y shape: {y.shape}")

# Разделение на train/test
X_train, X_test, y_train, y_test = train_test_split(
    X, y, test_size=0.2, random_state=42
)

print(f"\nTrain: {X_train.shape[0]}, Test: {X_test.shape[0]}")

# Масштабирование
scaler = StandardScaler()
X_train_scaled = scaler.fit_transform(X_train)
X_test_scaled = scaler.transform(X_test)

# ============================================================
# ШАГ 4: Обучение моделей
# ============================================================

print("\n" + "=" * 60)
print("ШАГ 4: ОБУЧЕНИЕ МОДЕЛЕЙ")
print("=" * 60)

models = {
    'Linear Regression': LinearRegression(),
    'Ridge': Ridge(alpha=1.0),
    'Lasso': Lasso(alpha=0.1),
    'Random Forest': RandomForestRegressor(n_estimators=100, random_state=42),
    'Gradient Boosting': GradientBoostingRegressor(n_estimators=100, random_state=42)
}

results = {}

for name, model in models.items():
    print(f"\n--- {name} ---")
    
    # Для линейных моделей — масштабированные данные
    if name in ['Linear Regression', 'Ridge', 'Lasso']:
        model.fit(X_train_scaled, y_train)
        y_pred = model.predict(X_test_scaled)
    else:
        model.fit(X_train, y_train)
        y_pred = model.predict(X_test)
    
    # Метрики
    mae = mean_absolute_error(y_test, y_pred)
    mse = mean_squared_error(y_test, y_pred)
    rmse = np.sqrt(mse)
    r2 = r2_score(y_test, y_pred)
    
    print(f"MAE:  {mae:.2f}")
    print(f"RMSE: {rmse:.2f}")
    print(f"R²:   {r2:.4f}")
    
    results[name] = {'MAE': mae, 'RMSE': rmse, 'R²': r2}

# Сравнение результатов
print("\n" + "=" * 60)
print("СРАВНЕНИЕ МОДЕЛЕЙ")
print("=" * 60)
results_df = pd.DataFrame(results).T
print(results_df)

# Лучшая модель по R²
best_model = max(results, key=lambda x: results[x]['R²'])
print(f"\nЛучшая модель по R²: {best_model}")

# ============================================================
# ШАГ 5: Важность признаков
# ============================================================

print("\n" + "=" * 60)
print("ШАГ 5: ВАЖНОСТЬ ПРИЗНАКОВ")
print("=" * 60)

# Из Random Forest
rf = models['Random Forest']
importance = pd.DataFrame({
    'feature': X.columns,
    'importance': rf.feature_importances_
}).sort_values('importance', ascending=False)

print(importance)

# Визуализация
plt.figure(figsize=(10, 6))
sns.barplot(data=importance, x='importance', y='feature', palette='viridis')
plt.title('Важность признаков (Random Forest)')
plt.tight_layout()
plt.savefig('C:\\it chalenge\\ml_tasks\\02_regression\\feature_importance.png')
print("\nГрафик сохранён: feature_importance.png")

# ============================================================
# ШАГ 6: Кросс-валидация
# ============================================================

print("\n" + "=" * 60)
print("ШАГ 6: КРОСС-ВАЛИДАЦИЯ")
print("=" * 60)

# Для Random Forest
rf = RandomForestRegressor(n_estimators=100, random_state=42)
cv_scores = cross_val_score(rf, X, y, cv=5, scoring='r2')

print(f"R² по фолдам: {cv_scores}")
print(f"Средний R²: {cv_scores.mean():.4f}")
print(f"Стандартное отклонение: {cv_scores.std():.4f}")

# ============================================================
# ШАГ 7: Прогноз для новых авто
# ============================================================

print("\n" + "=" * 60)
print("ШАГ 7: ПРОГНОЗ ДЛЯ НОВЫХ АВТО")
print("=" * 60)

new_cars = pd.DataFrame({
    'year': [2018, 2022, 2015],
    'mileage_km': [50000, 10000, 150000],
    'engine_volume': [2.0, 1.6, 3.0],
    'horsepower': [150, 120, 250],
    'fuel_type_бензин': [1, 1, 0],
    'fuel_type_дизель': [0, 0, 1],
    'fuel_type_электро': [0, 0, 0]
})

predictions = rf.predict(new_cars)

print("Новые авто:")
print(new_cars[['year', 'mileage_km', 'engine_volume', 'horsepower']])
print(f"\nПредсказанная цена:")
for i, price in enumerate(predictions):
    print(f"  Авто {i+1}: ${price:,.0f}")

# ============================================================
# ШАГ 8: Что можно улучшить
# ============================================================

print("\n" + "=" * 60)
print("ШАГ 8: УЛУЧШЕНИЯ")
print("=" * 60)
print("""
1. FEATURE ENGINEERING:
   - age = 2024 - year (возраст авто)
   - price_per_km = price / mileage_km
   - horsepower / engine_volume (мощность на литр)

2. ОБРАБОТКА ВЫБРОСОВ:
   - Удалить или ограничить экстремальные значения
   - Использовать RobustScaler вместо StandardScaler

3. ГИПЕРПАРАМЕТРЫ:
   from sklearn.model_selection import GridSearchCV
   params = {'n_estimators': [100, 200], 'max_depth': [5, 10, None]}
   grid = GridSearchCV(RandomForestRegressor(), params, cv=5)
   grid.fit(X_train, y_train)

4. АНСАМБЛИРОВАНИЕ:
   - Усреднить прогнозы нескольких моделей
   - Stacking

5. БОЛЬШЕ ДАННЫХ:
   - Больше признаков (марка, модель, комплектация)
   - Больше примеров
""")

print("\n" + "=" * 60)
print("ЗАДАЧА ВЫПОЛНЕНА!")
print("=" * 60)
