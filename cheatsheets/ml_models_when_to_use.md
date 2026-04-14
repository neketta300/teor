# 🤖 ШПАРГАЛКА: Какую ML-модель выбрать?

## 📊 КЛАССИФИКАЦИЯ (предсказание категории)

### Когда использовать какую модель:

| Ситуация | Модель | Почему |
|----------|--------|--------|
| **Быстрый базовый результат** | `LogisticRegression` | Простая, быстрая, интерпретируемая |
| **Нужны вероятности** | `LogisticRegression`, `RandomForest` | Дают `predict_proba()` |
| **Много признаков, мало данных** | `LogisticRegression` | Не переобучается на малых данных |
| **Средний датасет, нужна точность** | `RandomForest` | robust, не требует масштабирования |
| **Максимальная точность** | `GradientBoosting`, `XGBoost`, `CatBoost` | Самые мощные для табличных данных |
| **Нелинейные зависимости** | `RandomForest`, `SVM (rbf)` | Ловят сложные паттерны |
| **Интерпретируемость** | `LogisticRegression`, `DecisionTree` | Понятно, почему принято решение |

### Примеры кода:

```python
# Логистическая регрессия (БАЗОВЫЙ ВАРИАНТ)
from sklearn.linear_model import LogisticRegression
model = LogisticRegression(max_iter=1000, random_state=42)
model.fit(X_train_scaled, y_train)

# Случайный лес (ХОРОШИЙ ВАРИАНТ)
from sklearn.ensemble import RandomForestClassifier
model = RandomForestClassifier(n_estimators=100, random_state=42)
model.fit(X_train, y_train)  # НЕ требует масштабирования!

# Градиентный бустинг (МОЩНЫЙ ВАРИАНТ)
from sklearn.ensemble import GradientBoostingClassifier
model = GradientBoostingClassifier(n_estimators=100, random_state=42)
model.fit(X_train, y_train)

# XGBoost (если установлен: pip install xgboost)
from xgboost import XGBClassifier
model = XGBClassifier(random_state=42)
model.fit(X_train, y_train)

# SVM (для сложных границ)
from sklearn.svm import SVC
model = SVC(probability=True, random_state=42)
model.fit(X_train_scaled, y_train)  # ТРЕБУЕТ масштабирования!
```

---

## 📈 РЕГРЕССИЯ (предсказание числа)

### Когда использовать:

| Ситуация | Модель |
|----------|--------|
| **Базовый вариант** | `LinearRegression` |
| **Есть выбросы** | `Ridge` (L2 регуляризация) |
| **Много неважных признаков** | `Lasso` (L1 — обнуляет лишнее) |
| **Средний датасет** | `RandomForestRegressor` |
| **Максимальная точность** | `GradientBoostingRegressor`, `XGBoost` |

### Примеры:

```python
# Линейная регрессия
from sklearn.linear_model import LinearRegression
model = LinearRegression()
model.fit(X_train, y_train)

# Ridge (защита от переобучения)
from sklearn.linear_model import Ridge
model = Ridge(alpha=1.0)
model.fit(X_train_scaled, y_train)

# Lasso (отбор признаков)
from sklearn.linear_model import Lasso
model = Lasso(alpha=0.1)
model.fit(X_train_scaled, y_train)

# Случайный лес
from sklearn.ensemble import RandomForestRegressor
model = RandomForestRegressor(n_estimators=100, random_state=42)
model.fit(X_train, y_train)

# Градиентный бустинг
from sklearn.ensemble import GradientBoostingRegressor
model = GradientBoostingRegressor(n_estimators=100, random_state=42)
model.fit(X_train, y_train)
```

---

## 🔍 КЛАСТЕРИЗАЦИЯ (без учителя, поиск групп)

### Когда использовать:

| Ситуация | Модель |
|----------|--------|
| **Знаю число кластеров** | `KMeans(n_clusters=k)` |
| **Не знаю число кластеров** | `DBSCAN` (сам находит кластеры) |
| **Иерархия кластеров** | `AgglomerativeClustering` |
| **Кластеры разной размера** | `DBSCAN` |

### Примеры:

```python
# K-Means (нужно знать k)
from sklearn.cluster import KMeans
model = KMeans(n_clusters=3, random_state=42)
model.fit(X_scaled)
labels = model.labels_  # Метки кластеров
centers = model.cluster_centers_  # Центры кластеров

# DBSCAN (сам находит кластеры, может найти выбросы)
from sklearn.cluster import DBSCAN
model = DBSCAN(eps=0.5, min_samples=5)
model.fit(X_scaled)
labels = model.labels_  # -1 = выброс

# Иерархическая кластеризация
from sklearn.cluster import AgglomerativeClustering
model = AgglomerativeClustering(n_clusters=3)
model.fit(X_scaled)
labels = model.labels_
```

### Как выбрать k для K-Means:

```python
# Метод локтя (Elbow Method)
inertias = []
for k in range(1, 11):
    km = KMeans(n_clusters=k, random_state=42)
    km.fit(X_scaled)
    inertias.append(km.inertia_)

plt.plot(range(1, 11), inertias, 'bo-')
plt.xlabel('k')
plt.ylabel('Inertia')
# Ищем "локоть" — где кривая начинает выравниваться
```

---

## 🎯 МЕТРИКИ КАЧЕСТВА

### Классификация:

| Метрика | Формула | Когда использовать |
|---------|---------|-------------------|
| **Accuracy** | (TP+TN)/Все | Классы сбалансированы |
| **Precision** | TP/(TP+FP) | Важны ложные срабатывания (спам) |
| **Recall** | TP/(TP+FN) | Важно не пропустить (болезнь) |
| **F1-score** | 2·P·R/(P+R) | Баланс Precision и Recall |
| **ROC-AUC** | Площадь под ROC | Общее качество модели |

```python
from sklearn.metrics import (
    accuracy_score, precision_score, recall_score, 
    f1_score, roc_auc_score, confusion_matrix,
    classification_report
)

y_pred = model.predict(X_test)
y_prob = model.predict_proba(X_test)[:, 1]

print(f"Accuracy:  {accuracy_score(y_test, y_pred):.4f}")
print(f"Precision: {precision_score(y_test, y_pred):.4f}")
print(f"Recall:    {recall_score(y_test, y_pred):.4f}")
print(f"F1:        {f1_score(y_test, y_pred):.4f}")
print(f"ROC-AUC:   {roc_auc_score(y_test, y_prob):.4f}")
print(f"\n{classification_report(y_test, y_pred)}")
```

### Регрессия:

| Метрика | Описание | Когда использовать |
|---------|----------|-------------------|
| **MAE** | Средняя абсолютная ошибка | Интерпретируема, устойчива к выбросам |
| **MSE** | Среднеквадратичная ошибка | Штрафует большие ошибки |
| **RMSE** | Корень из MSE | В тех же единицах, что данные |
| **R²** | Доля объяснённой дисперсии | 1.0 = идеально, 0.0 = как среднее |

```python
from sklearn.metrics import mean_absolute_error, mean_squared_error, r2_score

y_pred = model.predict(X_test)

print(f"MAE:  {mean_absolute_error(y_test, y_pred):.2f}")
print(f"MSE:  {mean_squared_error(y_test, y_pred):.2f}")
print(f"RMSE: {np.sqrt(mean_squared_error(y_test, y_pred)):.2f}")
print(f"R²:   {r2_score(y_test, y_pred):.4f}")
```

### Кластеризация:

```python
from sklearn.metrics import silhouette_score, calinski_harabasz_score

# silhouette: от -1 до 1 (чем больше, тем лучше)
sil = silhouette_score(X_scaled, labels)
print(f"Silhouette: {sil:.4f}")

# Calinski-Harabasz: чем больше, тем лучше
ch = calinski_harabasz_score(X_scaled, labels)
print(f"Calinski-Harabasz: {ch:.2f}")
```

---

## 🚀 БЫСТРЫЙ ЧЕКЛИСТ ДЛЯ ОЛИМПИАДЫ

### 1️⃣ Загрузка и обзор
```python
import pandas as pd
df = pd.read_csv('data.csv')
print(df.head())
print(df.info())
print(df.describe())
print(df.isna().sum())
```

### 2️⃣ Подготовка
```python
# Пропуски
df = df.fillna(df.mean())  # Числовые
df = df.dropna()  # Или удалить

# Кодирование категориальных
df = pd.get_dummies(df, columns=['category'], dtype=int)

# X и y
X = df.drop('target', axis=1)
y = df['target']
```

### 3️⃣ Разделение и масштабирование
```python
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import StandardScaler

X_train, X_test, y_train, y_test = train_test_split(
    X, y, test_size=0.2, random_state=42, stratify=y
)

scaler = StandardScaler()
X_train_scaled = scaler.fit_transform(X_train)
X_test_scaled = scaler.transform(X_test)
```

### 4️⃣ Обучение (начни с простого!)
```python
# 1. Логистическая регрессия (база)
from sklearn.linear_model import LogisticRegression
lr = LogisticRegression(max_iter=1000, random_state=42)
lr.fit(X_train_scaled, y_train)
print(f"LR Accuracy: {lr.score(X_test_scaled, y_test):.4f}")

# 2. Случайный лес (обычно лучше)
from sklearn.ensemble import RandomForestClassifier
rf = RandomForestClassifier(n_estimators=100, random_state=42)
rf.fit(X_train, y_train)
print(f"RF Accuracy: {rf.score(X_test, y_test):.4f}")

# 3. Градиентный бустинг (если нужно ещё лучше)
from sklearn.ensemble import GradientBoostingClassifier
gb = GradientBoostingClassifier(n_estimators=100, random_state=42)
gb.fit(X_train, y_train)
print(f"GB Accuracy: {gb.score(X_test, y_test):.4f}")
```

### 5️⃣ Оценка
```python
from sklearn.metrics import classification_report
y_pred = rf.predict(X_test)
print(classification_report(y_test, y_pred))
```

---

## ⚠️ ВАЖНЫЕ ПРАВИЛА

1. **Всегда начинай с простой модели** (Logistic/Linear Regression)
2. **Random Forest — хороший выбор по умолчанию** для табличных данных
3. **Для классификации нужно масштабирование** (кроме деревьев и лесов)
4. **Для регрессии не всегда нужно масштабирование**
5. **Используй `random_state=42`** для воспроизводимости
6. **`stratify=y`** при дисбалансе классов
7. **Всегда смотри на несколько метрик**, не только на Accuracy!

---

## 📦 БИБЛИОТЕКИ ДЛЯ УСТАНОВКИ

```bash
# Обязательные
pip install pandas numpy scikit-learn matplotlib seaborn

# Рекомендуемые
pip install xgboost lightgbm

# Опционально
pip install catboost  # Может потребоваться компиляция на Windows
```
