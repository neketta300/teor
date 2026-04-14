# 🏆 Подготовка к IT CHALLENGE 2026 — Все направления

## 📁 Полная структура проекта

```
C:\it chalenge\
│
├── 📘 README.md                       ← Ты здесь!
│
├── 🐍 python_basics/                  # ОСНОВЫ PYTHON
│   ├── numpy_tutorial.py              # ➜ МАССИВЫ: создание, индексация, математика, нормализация
│   ├── pandas_tutorial.py             # ➜ ТАБЛИЦЫ: DataFrame, фильтрация, groupby, merge
│   └── algorithms_basics.py           # ➜ АЛГОРИТМЫ: сортировки, k-NN, расстояния, рекурсия
│
├── 🤖 ml_tasks/                       # МАШИННОЕ ОБУЧЕНИЕ
│   ├── 01_classification/
│   │   └── churn_prediction.py        # ➜ КЛАССИФИКАЦИЯ: отток клиентов (LR, RF, GB)
│   ├── 02_regression/
│   │   └── car_price_prediction.py    # ➜ РЕГРЕССИЯ: цена авто (LR, Ridge, RF, GB)
│   ├── 03_clustering/
│   │   └── customer_segmentation.py   # ➜ КЛАСТЕРИЗАЦИЯ: сегментация (KMeans, DBSCAN)
│   └── practice_tasks.py              # ➜ ПРАКТИКУМ: 5 задач для самостоятельного решения
│
├── 📊 data_analysis/                  # АНАЛИЗ ДАННЫХ
│   ├── exploratory_data_analysis.py   # ➜ EDA: визуализация, статистика, корреляции
│   └── ab_testing.py                  # ➜ A/B ТЕСТЫ: конверсия, значимость, рекомендации
│
├── 🔒 cybersecurity/                  # КИБЕРБЕЗОПАСНОСТЬ
│   ├── web_security_cheatsheet.md     # ➜ ШПАРГАЛКА: уязвимости, инструменты, команды
│   └── log_analysis.py                # ➜ АНАЛИЗ ЛОГОВ: обнаружение SQLi, XSS, brute-force
│
└── 📚 cheatsheets/                    # ШПАРГАЛКИ
    └── ml_models_when_to_use.md       # ➜ МОДЕЛИ + МЕТРИКИ + ЧЕК-ЛИСТ
```

## 🚀 Порядок изучения

### НЕДЕЛЯ 1-2: Python основы
1. ✅ `python_basics/numpy_tutorial.py` — массивы, математика, ML-задачи
2. ✅ `python_basics/pandas_tutorial.py` — таблицы, фильтрация, группировка
3. ✅ `python_basics/algorithms_basics.py` — сортировки, k-NN, расстояния

**Как запускать:**
```bash
python "C:\it chalenge\python_basics\numpy_tutorial.py"
```

### НЕДЕЛЯ 3-4: Машинное обучение
1. ✅ `ml_tasks/01_classification/churn_prediction.py` — классификация
2. ✅ `ml_tasks/02_regression/car_price_prediction.py` — регрессия
3. ✅ `ml_tasks/03_clustering/customer_segmentation.py` — кластеризация
4. ✅ `ml_tasks/practice_tasks.py` — 5 задач для практики

**Ключевые понятия:**
- Accuracy, Precision, Recall, F1, ROC-AUC (классификация)
- MAE, MSE, RMSE, R² (регрессия)
- Silhouette, Elbow, Inertia (кластеризация)
- Train/Test split, масштабирование, кросс-валидация

### НЕДЕЛЯ 5-6: Анализ данных
1. ✅ `data_analysis/exploratory_data_analysis.py` — EDA, визуализация, статистика
2. ✅ `data_analysis/ab_testing.py` — A/B тестирование

**Ключевые понятия:**
- Гистограммы, boxplot, scatter plot, heatmap
- t-test, ANOVA, Chi-square, Shapiro-Wilk
- Доверительные интервалы, p-value

### НЕДЕЛЯ 7: Кибербезопасность
1. ✅ `cybersecurity/web_security_cheatsheet.md` — изучить шпаргалку
2. ✅ `cybersecurity/log_analysis.py` — анализ логов

**Ключевые понятия:**
- SQLi, XSS, IDOR, Broken Auth
- DevTools, Burp Suite, ffuf, dirsearch
- HTTP-методы, коды ответов, заголовки

### НЕДЕЛЯ 8: Повторение и практика
- Реши `practice_tasks.py` БЕЗ подсказок
- Засекай время (2-3 часа на задачу)
- Повтори шпаргалки

## 📋 Чек-лист навыков

### Python основы
- [ ] List comprehensions
- [ ] Lambda-функции, map, filter
- [ ] Словари, подсчёт частот
- [ ] Сортировка (в т.ч. по ключу)
- [ ] Чтение/запись CSV

### NumPy
- [ ] Создание массивов
- [ ] Индексация и срезы
- [ ] Математические операции
- [ ] Reshape, flatten
- [ ] Статистика (mean, std, min, max)
- [ ] Нормализация, стандартизация

### Pandas
- [ ] Создание DataFrame
- [ ] Фильтрация по условию
- [ ] Группировка (groupby)
- [ ] Обработка пропусков
- [ ] One-Hot Encoding
- [ ] merge (join)

### Машинное обучение — Классификация
- [ ] Train/test split
- [ ] Масштабирование признаков
- [ ] Logistic Regression
- [ ] Random Forest
- [ ] Gradient Boosting
- [ ] Метрики: accuracy, precision, recall, F1, ROC-AUC
- [ ] Confusion matrix
- [ ] Важность признаков

### Машинное обучение — Регрессия
- [ ] Linear Regression
- [ ] Ridge / Lasso
- [ ] RandomForestRegressor
- [ ] GradientBoostingRegressor
- [ ] Метрики: MAE, MSE, RMSE, R²
- [ ] Кросс-валидация

### Машинное обучение — Кластеризация
- [ ] K-Means
- [ ] DBSCAN
- [ ] Elbow method
- [ ] Silhouette score
- [ ] Характеристика кластеров
- [ ] Визуализация (PCA)

### Анализ данных
- [ ] Гистограммы, boxplot, scatter plot
- [ ] Heatmap корреляций
- [ ] Временные ряды
- [ ] t-test (2 группы)
- [ ] ANOVA (3+ групп)
- [ ] Chi-square (категориальные)
- [ ] A/B тестирование
- [ ] Доверительные интервалы

### Кибербезопасность
- [ ] DevTools (Network, Console, Sources)
- [ ] HTTP-методы и коды ответов
- [ ] SQL-инъекции (обнаружение)
- [ ] XSS (обнаружение)
- [ ] Сканирование директорий
- [ ] Brute-force (обнаружение)
- [ ] Анализ HTTP-логов
- [ ] OWASP Top 10 (понимание)

## 💡 Советы для олимпиады

1. **Начинай с простой модели** (Logistic/Linear Regression) — это даст базовый результат
2. **Random Forest — хороший выбор по умолчанию** для большинства задач
3. **Всегда смотри на несколько метрик**, не только на Accuracy
4. **Используй `random_state=42`** для воспроизводимости результатов
5. **Комментируй код** — это влияет на оценку!
6. **Проверяй данные на пропуски** перед обучением
7. **Масштабируй данные** для моделей, кроме деревьев

## 📦 Установка библиотек

```bash
# Обязательные (для ML и анализа данных)
pip install pandas numpy scikit-learn matplotlib seaborn scipy

# Рекомендуемые (для продвинутого ML)
pip install xgboost lightgbm

# Для A/B тестирования
pip install statsmodels
```

## 📊 Итого в проекте

| Файл | Тип | Строк | Тема |
|------|-----|-------|------|
| `numpy_tutorial.py` | Туториал | 300+ | Массивы, математика, ML-задачи |
| `pandas_tutorial.py` | Туториал | 300+ | DataFrame, фильтрация, группировка |
| `algorithms_basics.py` | Туториал | 470+ | Сортировки, k-NN, расстояния |
| `churn_prediction.py` | Задача | 300+ | Классификация (полный пример) |
| `car_price_prediction.py` | Задача | 300+ | Регрессия (полный пример) |
| `customer_segmentation.py` | Задача | 400+ | Кластеризация (KMeans, DBSCAN) |
| `practice_tasks.py` | Практикум | 450+ | 5 задач для самостоятельного решения |
| `exploratory_data_analysis.py` | Задача | 500+ | EDA, визуализация, статистика |
| `ab_testing.py` | Задача | 350+ | A/B тестирование |
| `log_analysis.py` | Задача | 400+ | Анализ логов, обнаружение атак |
| `ml_models_when_to_use.md` | Шпаргалка | 250+ | Модели, метрики, чек-лист |
| `web_security_cheatsheet.md` | Шпаргалка | 400+ | Уязвимости, инструменты, команды |

**Всего: ~4,600+ строк кода и документации**

---

**Удачи на олимпиаде! 🇧🇾🏆**

*Создано для подготовки к IT CHALLENGE 2026, Республика Беларусь*
