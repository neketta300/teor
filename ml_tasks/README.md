# 🤖 ML Практикум — 5 задач для самостоятельного решения

## 📁 Файл

| Файл | Описание | Строк |
|------|----------|-------|
| `practice_tasks.py` | 5 задач: спам, оценки, песни, ирисы, Титаник | 450+ |

---

## 📋 Структура задач

Каждая задача имеет:
1. **Условие** — что нужно сделать
2. **Данные** — готовый датасет
3. **`# TODO: Реши сам!`** — место для твоего кода
4. **Решение** (закомментировано) — раскомментируй для проверки

**Совет:** Сначала решай САМ, потом смотри решение!

---

## 📝 Задача 1: Классификация спама (лёгкая ⭐)

### Условие

Даны тексты сообщений. Классифицируй: **спам (1)** или **не спам (0)**.

### Данные

```python
messages = [
    ("Вы выиграли 1000$! Нажмите ссылку!", 1),    # СПАМ
    ("Бесплатный iPhone! Перейдите по ссылке!", 1), # СПАМ
    ("Привет, как дела?", 0),                       # НЕ СПАМ
    ("Встречаемся завтра в 15:00", 0),             # НЕ СПАМ
    ...
]
```

### Ключевые шаги

```
1. Создать DataFrame
        ↓
2. TF-IDF векторизация (текст → числа)
        ↓
3. LogisticRegression
        ↓
4. Accuracy + F1-score
        ↓
5. Тест на новых сообщениях
```

### TF-IDF — как текст превращается в числа

```python
from sklearn.feature_extraction.text import TfidfVectorizer

tfidf = TfidfVectorizer(max_features=50)
X_tfidf = tfidf.fit_transform(df_spam['text'])
```

**Как работает TF-IDF:**

| Слово | В спаме | В обычных | TF-IDF |
|-------|---------|-----------|--------|
| «выиграли» | Часто | Никогда | **Высокий** (характерно для спама) |
| «iPhone» | Часто | Редко | **Высокий** |
| «привет» | Редко | Часто | **Низкий** (обычное слово) |
| «срочно» | Часто | Никогда | **Высокий** |

**TF** (Term Frequency) = как часто слово в документе.
**IDF** (Inverse Document Frequency) = насколько слово редкое во всей коллекции.

`max_features=50` — берём только 50 самых информативных слов.

### Решение

```python
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.linear_model import LogisticRegression

# Векторизация
tfidf = TfidfVectorizer(max_features=50)
X_tfidf = tfidf.fit_transform(df_spam['text'])
y_spam = df_spam['label']

# Разделение
X_train, X_test, y_train, y_test = train_test_split(X_tfidf, y_spam, test_size=0.3, random_state=42)

# Обучение
model = LogisticRegression()
model.fit(X_train, y_train)

# Оценка
y_pred = model.predict(X_test)
print(f"Accuracy: {accuracy_score(y_test, y_pred):.4f}")
print(f"F1-score: {f1_score(y_test, y_pred):.4f}")

# Тест
test_msgs = ["Срочно переведите деньги!", "Увидимся в пятницу"]
test_vec = tfidf.transform(test_msgs)
preds = model.predict(test_vec)
```

---

## 📝 Задача 2: Предсказание оценки студента (средняя ⭐⭐)

### Условие

Даны данные о студентах: часы учёбы, посещаемость, домашние задания. Предскажите **итоговую оценку (0-100)**.

### Данные

```python
students = pd.DataFrame({
    'study_hours': np.random.uniform(5, 40, 100),     # 5-40 часов
    'attendance': np.random.uniform(50, 100, 100),     # 50-100%
    'homework_score': np.random.uniform(3, 10, 100),   # 3-10 баллов
    'projects_count': np.random.randint(0, 5, 100)     # 0-4 проекта
})

# Оценка = формула + шум
students['final_grade'] = (
    students['study_hours'] * 1.5 +       # Каждый час = +1.5 балла
    students['attendance'] * 0.3 +         # Каждый % = +0.3 балла
    students['homework_score'] * 5 +       # Каждый балл ДЗ = +5 баллов
    students['projects_count'] * 3 +       # Каждый проект = +3 балла
    np.random.normal(0, 5, 100)            # Шум
).clip(0, 100).round(1)
```

### Ключевые шаги

```
1. Создать датасет
        ↓
2. LinearRegression vs RandomForestRegressor
        ↓
3. Сравнить MAE и R²
        ↓
4. Определить самый важный признак
```

### Решение

```python
from sklearn.linear_model import LinearRegression
from sklearn.ensemble import RandomForestRegressor
from sklearn.preprocessing import StandardScaler

X = students.drop('final_grade', axis=1)
y = students['final_grade']

X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

# Linear Regression (нужно масштабирование)
scaler = StandardScaler()
X_train_s = scaler.fit_transform(X_train)
X_test_s = scaler.transform(X_test)

lr = LinearRegression()
lr.fit(X_train_s, y_train)
lr_pred = lr.predict(X_test_s)

print(f"Linear Regression: MAE={mean_absolute_error(y_test, lr_pred):.2f}, R²={r2_score(y_test, lr_pred):.4f}")

# Random Forest (НЕ нужно масштабирование)
rf = RandomForestRegressor(n_estimators=50, random_state=42)
rf.fit(X_train, y_train)
rf_pred = rf.predict(X_test)

print(f"Random Forest: MAE={mean_absolute_error(y_test, rf_pred):.2f}, R²={r2_score(y_test, rf_pred):.4f}")

# Важность признаков
importance = pd.DataFrame({
    'feature': X.columns,
    'importance': rf.feature_importances_
}).sort_values('importance', ascending=False)
```

**Ожидаемый результат:**
```
Linear Regression: MAE=4.50, R²=0.8200
Random Forest: MAE=3.20, R²=0.9100  ← лучше
```

**Важность признаков (типичная):**
```
homework_score    0.45  ← самый важный!
study_hours       0.30
attendance        0.15
projects_count    0.10
```

---

## 📝 Задача 3: Группировка песен (средняя ⭐⭐⭐)

### Условие

Даны характеристики песен. Найди **естественные группы жанров** без меток.

### Данные — 4 жанра

| Жанр | Tempo | Energy | Loudness | Acousticness | Danceability |
|------|-------|--------|----------|--------------|-------------|
| **Рок** (30) | 140±15 | 0.8±0.1 | -5±2 | 0.1±0.05 | 0.5±0.1 |
| **Поп** (40) | 120±10 | 0.6±0.1 | -7±2 | 0.2±0.1 | 0.75±0.08 |
| **Акустика** (25) | 80±15 | 0.3±0.1 | -15±3 | 0.85±0.08 | 0.4±0.1 |
| **Электроника** (35) | 130±20 | 0.9±0.05 | -4±2 | 0.02±0.01 | 0.8±0.08 |

### Ключевые шаги

```
1. StandardScaler
        ↓
2. Elbow Method (k=2..8) → Inertia
        ↓
3. Silhouette Score → подтвердить k
        ↓
4. K-Means с оптимальным k
        ↓
5. Характеристика каждого кластера
```

### Решение

```python
from sklearn.cluster import KMeans
from sklearn.metrics import silhouette_score
from sklearn.preprocessing import StandardScaler

scaler = StandardScaler()
songs_scaled = scaler.fit_transform(songs)

# Elbow + Silhouette
inertias = []
sil_scores = []
for k in range(2, 8):
    km = KMeans(n_clusters=k, random_state=42, n_init=10)
    km.fit(songs_scaled)
    inertias.append(km.inertia_)
    sil_scores.append(silhouette_score(songs_scaled, km.labels_))

# Оптимальное k = максимум silhouette
optimal_k = sil_scores.index(max(sil_scores)) + 2

# K-Means
km = KMeans(n_clusters=optimal_k, random_state=42, n_init=10)
labels = km.fit_predict(songs_scaled)

# Характеристика кластеров
songs['cluster'] = labels
for i in range(optimal_k):
    cluster_data = songs[songs['cluster'] == i].mean()
    print(f"Кластер {i}: Tempo={cluster_data['tempo']:.0f}, Energy={cluster_data['energy']:.2f}")
```

**Ожидаемый результат:** k ≈ 4 (4 жанра), silhouette ≈ 0.5-0.6

---

## 📝 Задача 4: Ирисы Фишера (лёгкая ⭐) — КЛАССИКА ML

### Условие

Классический датасет **Iris**. Определи **сорт ириса** по характеристикам цветка.

Это **multi-class классификация** — 3 класса, не 2!

### Данные

```python
from sklearn.datasets import load_iris

iris = load_iris()
X = iris.data    # 150 образцов, 4 признака
y = iris.target  # 0=setosa, 1=versicolor, 2=virginica

# Признаки:
#   sepal length (cm)   — длина чашелистика
#   sepal width (cm)    — ширина чашелистика
#   petal length (cm)   — длина лепестка
#   petal width (cm)    — ширина лепестка
```

### Ключевые шаги

```
1. Загрузить iris
        ↓
2. train/test split (stratify=y!)
        ↓
3. Обучить 3 классификатора
        ↓
4. Сравнить accuracy
        ↓
5. Confusion matrix (3×3!)
```

### Решение

```python
from sklearn.ensemble import RandomForestClassifier, GradientBoostingClassifier
from sklearn.svm import SVC
from sklearn.metrics import confusion_matrix, classification_report

X_train, X_test, y_train, y_test = train_test_split(
    X, y, test_size=0.2, random_state=42, stratify=y
)

models = {
    'Logistic Regression': LogisticRegression(max_iter=200),
    'Random Forest': RandomForestClassifier(n_estimators=50, random_state=42),
    'SVM': SVC(kernel='rbf', random_state=42)
}

scaler = StandardScaler()
X_train_s = scaler.fit_transform(X_train)
X_test_s = scaler.transform(X_test)

for name, model in models.items():
    if name in ['SVM', 'Logistic Regression']:
        model.fit(X_train_s, y_train)
        pred = model.predict(X_test_s)
    else:
        model.fit(X_train, y_train)
        pred = model.predict(X_test)

    acc = accuracy_score(y_test, pred)
    print(f"{name}: Accuracy = {acc:.4f}")
```

**Confusion Matrix (3×3):**

```
              Предсказано
              setosa  versicolor  virginica
Реально setosa   10         0          0
      versicolor  0         9          1
      virginica   0         1          9

setosa: идеально (10/10)
versicolor: 1 ошибка (спутали с virginica)
virginica: 1 ошибка (спутали с versicolor)
```

**Почему путают versicolor и virginica:** Их лепестки похожи. setosa сильно отличается — поэтому идеально.

---

## 📝 Задача 5: Титаник — Feature Engineering (сложная ⭐⭐⭐⭐)

### Условие

Синтетический датасет по мотивам Титаника. Нужно **создать новые признаки** и сравнить с baseline.

### Данные

```python
titanic = pd.DataFrame({
    'pclass': np.random.choice([1, 2, 3], 500, p=[0.25, 0.25, 0.50]),  # Класс билета
    'sex': np.random.choice(['male', 'female'], 500),                   # Пол
    'age': np.random.normal(30, 15, 500).clip(1, 80).round(1),          # Возраст
    'fare': np.random.exponential(50, 500).clip(5, 500).round(2),       # Стоимость
    'embarked': np.random.choice(['C', 'Q', 'S'], 500, p=[0.3, 0.1, 0.6]), # Порт
    'has_cabin': np.random.choice([0, 1], 500, p=[0.7, 0.3])            # Есть каюта
})

# Пропуски в возрасте!
titanic.loc[np.random.choice(500, 30, replace=False), 'age'] = np.nan

# Выживание зависит от признаков:
# 1-й класс, женщины, дети, дорогие билеты → выше шанс
titanic['survived'] = (...)
```

### Ключевые шаги

```
1. Baseline: базовые признаки (pclass, sex, age, fare, embarked, has_cabin)
        ↓
2. Feature Engineering: СОЗДАТЬ новые признаки
        ↓
3. Сравнить F1 baseline vs engineered
        ↓
4. Важность признаков
```

### Feature Engineering — какие признаки создать?

```python
def prepare_features(df, create_features=False):
    df_prep = df.copy()

    # ОБЯЗАТЕЛЬНО: обработка пропусков
    df_prep['age'] = df_prep['age'].fillna(df_prep['age'].median())

    # Кодирование пола: female → 1, male → 0
    df_prep['sex'] = (df_prep['sex'] == 'female').astype(int)

    # One-Hot Encoding для порта
    df_prep = pd.get_dummies(df_prep, columns=['embarked'], prefix='embarked', dtype=int)

    if create_features:
        # 1. Is_child — дети спасали первыми
        df_prep['is_child'] = (df_prep['age'] < 12).astype(int)

        # 2. Is_elderly — пожилые имели меньше шансов
        df_prep['is_elderly'] = (df_prep['age'] > 60).astype(int)

        # 3. Family_size — размер семьи (синтетический)
        df_prep['family_size'] = np.random.poisson(2, len(df_prep))

        # 4. Fare_per_person — стоимость на человека
        df_prep['fare_per_class'] = df_prep['fare'] / df_prep['pclass']

        # 5. Age × Class — взаимодействие
        df_prep['age_class'] = df_prep['age'] * df_prep['pclass']

        # 6. Male child — особый риск
        df_prep['is_male_child'] = ((df_prep['sex'] == 0) & (df_prep['age'] < 12)).astype(int)

    return df_prep
```

**Почему это помогает:**
- `is_child` — ловит нелинейность: дети < 12 имели особый приоритет
- `is_elderly` — пожилые > 60 имели меньше шансов
- `fare_per_class` — нормализует стоимость билета относительно класса
- `age_class` — взаимодействие: пожилой в 3-м классе = двойной риск
- `is_male_child` — мальчики-дети имели меньший шанс, чем девочки

### Сравнение результатов

```python
# Baseline
df_baseline = prepare_features(titanic, create_features=False)
# ... обучение ...
print(f"BASELINE: Accuracy = {acc:.4f}, F1 = {f1:.4f}")

# Engineered
df_engineered = prepare_features(titanic, create_features=True)
# ... обучение ...
print(f"ENGINEERED: Accuracy = {acc:.4f}, F1 = {f1:.4f}")

improvement = f1_engineered - f1_baseline
print(f"Улучшение F1: {improvement:+.4f}")
```

**Ожидаемый результат:**
```
BASELINE:    Accuracy = 0.7800, F1 = 0.7500
ENGINEERED:  Accuracy = 0.8200, F1 = 0.8000
Улучшение F1: +0.0500
```

---

## 🎯 Общие советы для всех задач

### 1. Всегда начинай с EDA

```python
df.head()
df.info()
df.describe()
df.isna().sum()
df['target'].value_counts()
```

### 2. Правильный порядок шагов

```
Данные → EDA → Пропуски → Кодирование → Масштабирование → Split → Обучение → Оценка
```

### 3. Когда нужно масштабирование?

| Нужно | НЕ нужно |
|-------|----------|
| LogisticRegression | DecisionTree |
| SVM | RandomForest |
| K-Means | GradientBoosting |
| KNN | XGBoost |
| PCA | CatBoost |

**Правило:** Если модель использует **расстояния** или **градиенты** — нужно масштабирование. Если только **разделения** (if-else) — не нужно.

### 4. Выбор модели по умолчанию

| Задача | Модель по умолчанию |
|--------|-------------------|
| Классификация | `RandomForestClassifier` |
| Регрессия | `RandomForestRegressor` |
| Текст | `TfidfVectorizer + LogisticRegression` |
| Кластеризация | `KMeans` |

### 5. Засекай время!

На олимпиаде время ограничено. Тренируйся:
- Лёгкая задача: 30-45 мин
- Средняя: 1-1.5 часа
- Сложная: 2-3 часа

---

## 🚀 Запуск

```bash
python "C:\itChalenge\ml_tasks\practice_tasks.py"
```

## 📦 Зависимости

```bash
pip install pandas numpy scikit-learn matplotlib seaborn
```
