# 📊 Классификация — Churn Prediction (Предсказание оттока)

## 📋 Условие задачи

Банк предоставляет данные о клиентах. Нужно предсказать, **уйдёт ли клиент** к конкурентам (`churn = 1`) или **останется** (`churn = 0`).

### Входные данные

| Признак | Тип | Описание |
|---------|-----|----------|
| `age` | число | Возраст клиента |
| `balance` | число | Баланс на счёте |
| `num_products` | число | Число продуктов банка |
| `has_credit_card` | 0/1 | Есть ли кредитная карта |
| `is_active` | 0/1 | Активный клиент или нет |
| `satisfaction` | 1-5 | Оценка удовлетворённости |

---

## 🔄 Полный пайплайн решения

```
┌─────────────────────────────────────────────────────┐
│  ШАГ 1: Данные                                       │
│  Генерация/загрузка → обзор → распределение классов  │
└──────────────────────┬──────────────────────────────┘
                       ▼
┌─────────────────────────────────────────────────────┐
│  ШАГ 2: EDA                                          │
│  groupby().mean(), корреляции, поиск зависимостей    │
└──────────────────────┬──────────────────────────────┘
                       ▼
┌─────────────────────────────────────────────────────┐
│  ШАГ 3: Подготовка                                   │
│  X/y → train_test_split → StandardScaler             │
└──────────────────────┬──────────────────────────────┘
                       ▼
┌─────────────────────────────────────────────────────┐
│  ШАГ 4: Обучение                                     │
│  LogisticRegression + RandomForestClassifier          │
└──────────────────────┬──────────────────────────────┘
                       ▼
┌─────────────────────────────────────────────────────┐
│  ШАГ 5: Оценка                                       │
│  Accuracy, Precision, Recall, F1, ROC-AUC,           │
│  Confusion Matrix, classification_report             │
└──────────────────────┬──────────────────────────────┘
                       ▼
┌─────────────────────────────────────────────────────┐
│  ШАГ 6: Прогноз                                      │
│  Предсказание для новых клиентов                     │
└─────────────────────────────────────────────────────┘
```

---

## 📖 Пошаговый разбор кода

### ШАГ 1: Загрузка данных

```python
np.random.seed(42)  # Фиксируем генератор для воспроизводимости

data = pd.DataFrame({
    'age': np.random.randint(18, 70, 500),           # Возраст 18-69
    'balance': np.random.normal(5000, 3000, 500),    # Баланс ~ N(5000, 3000)
    'num_products': np.random.randint(1, 6, 500),    # 1-5 продуктов
    'has_credit_card': np.random.choice([0, 1], 500), # 50/50
    'is_active': np.random.choice([0, 1], 500, p=[0.3, 0.7]), # 70% активных
    'satisfaction': np.random.randint(1, 6, 500)     # Оценка 1-5
})
```

**Целевая переменная** (churn) зависит от признаков:

```python
churn_prob = (
    0.3                                          # Базовая вероятность
    - 0.2 * data['is_active']                    # Активные реже уходят
    + 0.15 * (data['satisfaction'] <= 2)         # Недовольные чаще уходят
    - 0.1 * (data['num_products'] >= 3)          # С 3+ продуктами лояльнее
    + np.random.normal(0, 0.1, 500)              # Шум
)
data['churn'] = (churn_prob > 0.3).astype(int)   # Порог → 0 или 1
```

**Как работает:** Клиент **неактивный** + **недовольный** (оценка ≤ 2) + **мало продуктов** → с большей вероятностью `churn = 1`.

---

### ШАГ 2: EDA (Исследовательский анализ)

```python
# Средние значения: ушедшие vs оставшиеся
data.groupby('churn').mean()
```

**Что смотрим:**
- Ушедшие клиенты (`churn=1`) имеют **ниже** удовлетворённость?
- Ушедшие клиенты **реже** активны?
- Ушедшие клиенты имеют **меньше** продуктов?

```python
# Корреляция с churn
data.corr()['churn'].sort_values(ascending=False)
```

**Интерпретация:**
- `is_active: -0.45` → сильные обратная связь: активные = лояльные
- `satisfaction: -0.32` → чем выше оценка, тем реже уходят
- `num_products: -0.18` → больше продуктов = чуть реже уходят

---

### ШАГ 3: Подготовка данных

```python
# 1. Разделяем признаки (X) и ответ (y)
X = data.drop('churn', axis=1)   # Всё, кроме churn
y = data['churn']                 # Только churn

# 2. Делим на обучение (80%) и тест (20%)
X_train, X_test, y_train, y_test = train_test_split(
    X, y, test_size=0.2, random_state=42, stratify=y
)
```

**Зачем `stratify=y`:** Сохраняет пропорцию классов. Если 30% ушли в исходных данных, то и в train, и в test будет ~30% ушедших. Без этого может случиться перекос.

```python
# 3. Масштабирование (StandardScaler)
scaler = StandardScaler()
X_train_scaled = scaler.fit_transform(X_train)  # fit + transform
X_test_scaled = scaler.transform(X_test)        # ТОЛЬКО transform!
```

**Почему fit только на train?**
- `fit()` — вычисляет среднее и станд. отклонение
- `transform()` — применяет формулу `(x - mean) / std`
- Если сделать `fit` на test — модель «подглядит» в тестовые данные → завышенные метрики!

**Результат масштабирования:**
- До: `balance` = [500, 8000, 12000], `age` = [20, 45, 65]
- После: все признаки имеют `mean ≈ 0`, `std ≈ 1`

---

### ШАГ 4: Обучение моделей

#### Модель 1: Логистическая регрессия

```python
lr = LogisticRegression(random_state=42, max_iter=1000)
lr.fit(X_train_scaled, y_train)  # Нужны масштабированные данные!

y_pred_lr = lr.predict(X_test_scaled)       # Предсказания (0 или 1)
y_prob_lr = lr.predict_proba(X_test_scaled)[:, 1]  # Вероятности ухода
```

**Как работает логистическая регрессия:**

```
z = w1*x1 + w2*x2 + ... + wn*xn + b
probability = 1 / (1 + e^(-z))   # Сигмоида → число от 0 до 1
```

Если `probability > 0.5` → класс 1 (уйдёт), иначе → класс 0 (останется).

**Коэффициенты модели:**

```python
feature_importance = pd.DataFrame({
    'feature': X.columns,
    'coefficient': lr.coef_[0]
}).sort_values('coefficient', ascending=False)
```

**Интерпретация:**
- **Положительный** коэффициент → увеличивает вероятность ухода
- **Отрицательный** коэффициент → уменьшает вероятность ухода
- Чем **больше** по модулю → тем важнее признак

---

#### Модель 2: Случайный лес

```python
rf = RandomForestClassifier(n_estimators=100, random_state=42)
rf.fit(X_train, y_train)  # НЕ нужно масштабирование!

y_pred_rf = rf.predict(X_test)
y_prob_rf = rf.predict_proba(X_test)[:, 1]
```

**Как работает Random Forest:**

```
1. Создаёт 100 «деревьев решений»
   Каждое дерево — набор правил if-else:
   ┌── is_active == 0?
   │   ├── Да → satisfaction <= 2?
   │   │   ├── Да → churn = 1 (уйдёт)
   │   │   └── Нет → churn = 0 (останется)
   │   └── Нет → churn = 0 (останется)

2. Каждое дерево голосует
3. Результат = большинство голосов
```

**Почему не нужно масштабирование:** Деревья сравнивают значения внутри одного признака (`age > 30?`), а не между признаками.

**Важность признаков:**

```python
feature_importance_rf = pd.DataFrame({
    'feature': X.columns,
    'importance': rf.feature_importances_
}).sort_values('importance', ascending=False)
```

`feature_importances_` — насколько уменьшается «неопределённость» (Gini impurity) при разбиении по этому признаку.

---

### ШАГ 5: Метрики оценки

```python
from sklearn.metrics import (
    accuracy_score, precision_score, recall_score,
    f1_score, confusion_matrix, classification_report,
    roc_auc_score
)
```

#### Confusion Matrix (Матрица ошибок)

```
              Предсказано
              Останется    Уйдёт
Реально  Останется   85 (TN)     10 (FP)
         Уйдёт       15 (FN)     90 (TP)
```

| Термин | Расшифровка | Значение |
|--------|------------|----------|
| **TP** | True Positive | Правильно: сказали «уйдёт» и он ушёл = 90 |
| **TN** | True Negative | Правильно: сказали «останется» и остался = 85 |
| **FP** | False Positive | Ошибка: сказали «уйдёт», но остался = 10 |
| **FN** | False Negative | Ошибка: сказали «останется», но ушёл = 15 |

#### Метрики (формулы + смысл)

| Метрика | Формула | Значение | Когда важна |
|---------|---------|----------|-------------|
| **Accuracy** | (TP+TN) / Все | `(90+85)/200 = 0.875` | Когда классы сбалансированы |
| **Precision** | TP / (TP+FP) | `90/(90+10) = 0.900` | Когда дорого ложное срабатывание |
| **Recall** | TP / (TP+FN) | `90/(90+15) = 0.857` | Когда дорого пропустить (медицина, мошенничество) |
| **F1-score** | 2×P×R / (P+R) | `2×0.9×0.857/(0.9+0.857) = 0.878` | Баланс Precision и Recall |
| **ROC-AUC** | Площадь под ROC | `0.92` | Способность различать классы |

**Примеры из жизни:**

- **Спам-фильтр:** важен **Precision** — лучше пропустить спам, чем удалить важное письмо
- **Диагностика рака:** важен **Recall** — нельзя пропустить больного, пусть будет больше ложных тревог
- **Churn:** важен **F1** — баланс между тем, чтобы найти уходящих, и не тратить ресурсы на лояльных

**ROC-AUC подробно:**
- `1.0` — идеальная модель (различает все пары)
- `0.9-0.95` — отлично
- `0.8-0.9` — хорошо
- `0.7-0.8` — приемлемо
- `0.5` — как случайное угадывание (бросаем монетку)

---

### ШАГ 6: Прогноз для новых клиентов

```python
new_clients = pd.DataFrame({
    'age': [25, 45, 60],
    'balance': [1000, 8000, 15000],
    'num_products': [1, 4, 3],
    'has_credit_card': [0, 1, 1],
    'is_active': [0, 1, 1],
    'satisfaction': [2, 5, 3]
})

predictions = rf.predict(new_clients)           # 0 или 1
probabilities = rf.predict_proba(new_clients)[:, 1]  # Вероятность

for i, (pred, prob) in enumerate(zip(predictions, probabilities)):
    status = "УЙДЁТ" if pred == 1 else "ОСТАНЕТСЯ"
    print(f"Клиент {i+1}: {status} (вероятность: {prob:.2%})")
```

**Вывод:**
```
Клиент 1: УЙДЁТ (вероятность: 78.5%)   ← Неактивный, недовольный, 1 продукт
Клиент 2: ОСТАНЕТСЯ (вероятность: 8.2%) ← Активный, доволен, 4 продукта
Клиент 3: ОСТАНЕТСЯ (вероятность: 22.1%) ← Активный, средний баланс
```

---

## 🛠 Как улучшить результат

### 1. Подбор гиперпараметров (GridSearchCV)

```python
from sklearn.model_selection import GridSearchCV

params = {
    'n_estimators': [50, 100, 200],
    'max_depth': [5, 10, None],
    'min_samples_split': [2, 5, 10]
}

grid = GridSearchCV(RandomForestClassifier(), params, cv=5, scoring='f1')
grid.fit(X_train, y_train)

print(f"Лучшие параметры: {grid.best_params_}")
print(f"Лучший F1: {grid.best_score_:.4f}")
```

**Как работает:** Перебирает **все комбинации** параметров, оценивает каждую через кросс-валидацию, выбирает лучшую.

### 2. Кросс-валидация

```python
from sklearn.model_selection import cross_val_score

scores = cross_val_score(rf, X, y, cv=5, scoring='f1')
print(f"Средний F1: {scores.mean():.4f} (+/- {scores.std() * 2:.4f})")
```

**Как работает cv=5:**
```
Данные: [■■■■■]  (5 фолдов)

Fold 1: [test][train][train][train][train]
Fold 2: [train][test][train][train][train]
Fold 3: [train][train][test][train][train]
Fold 4: [train][train][train][test][train]
Fold 5: [train][train][train][train][test]

Результат = среднее по 5 фолдам
```

### 3. Feature Engineering

```python
# Новые признаки
data['age_group'] = pd.cut(data['age'], bins=[0, 25, 40, 55, 100],
                           labels=['молодой', 'средний', 'зрелый', 'пожилой'])
data['balance_per_product'] = data['balance'] / data['num_products']
data['is_unsatisfied'] = (data['satisfaction'] <= 2).astype(int)
data['is_low_activity'] = (data['is_active'] == 0).astype(int)
```

---

## 📊 Шпаргалка: какую модель выбрать?

| Ситуация | Модель | Почему |
|----------|--------|--------|
| Быстрый результат | `LogisticRegression` | Быстрая, интерпретируемая |
| Данные с выбросами | `RandomForest` | Устойчив к выбросам |
| Нужно объяснить | `LogisticRegression` | Коэффициенты = важность |
| Максимальная точность | `GradientBoosting` / `XGBoost` | Обычно лучшая точность |
| Мало данных | `LogisticRegression` | Не переобучается |
| Много данных | `RandomForest` / `GB` | Раскрываются на больших данных |

---

## 🚀 Запуск

```bash
python "C:\itChalenge\ml_tasks\01_classification\churn_prediction.py"
```

## 📦 Зависимости

```bash
pip install pandas numpy scikit-learn matplotlib seaborn
```
