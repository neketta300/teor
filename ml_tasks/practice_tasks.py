"""
ПРАКТИКУМ: ML-задачи для самостоятельного решения
===================================================
Здесь 5 задач разного сложности.
В каждой задаче: условие + скелет решения + место для твоего кода.

Совет: Попробуй решить сам, потом подсмотри подсказки.
"""

import pandas as pd
import numpy as np
from sklearn.model_selection import train_test_split
from sklearn.metrics import accuracy_score, f1_score, mean_absolute_error, r2_score

# ============================================================
# ЗАДАЧА 1: Классификация — Определение спама (лёгкая)
# ============================================================

print("=" * 60)
print("ЗАДАЧА 1: КЛАССИФИКАЦИЯ — ОПРЕДЕЛЕНИЕ СПАМА")
print("=" * 60)

print("""
УСЛОВИЕ:
Даны тексты сообщений. Нужно классифицировать: спам (1) или не спам (0).

Подсказка: Используй TF-IDF векторизацию + Logistic Regression.

Шаги:
1. Создать DataFrame с текстами и метками
2. Использовать TfidfVectorizer для преобразования текстов
3. Обучить LogisticRegression
4. Оценить accuracy и f1-score
""")

# Данные
messages = [
    ("Вы выиграли 1000$! Нажмите ссылку!", 1),
    ("Бесплатный iPhone! Перейдите по ссылке!", 1),
    ("СРОЧНО! Ваш аккаунт взломан! Подтвердите данные!", 1),
    ("Заработок в интернете! 500$ в день!", 1),
    ("Купите сейчас! Скидка 99%! Только сегодня!", 1),
    ("Привет, как дела?", 0),
    ("Встречаемся завтра в 15:00", 0),
    ("Отправил тебе документы на почту", 0),
    ("Мама звонила, перезвони ей", 0),
    ("Отчёт готов, можно скачивать", 0),
    ("Спасибо за помощь!", 0),
    ("Завтра совещание в 10 утра", 0),
]

# TODO: Реши сам!
# Подсказки:
# from sklearn.feature_extraction.text import TfidfVectorizer
# from sklearn.linear_model import LogisticRegression

print("\nТвоё решение:")
print("# Напиши код здесь...")

# ============================================
# РЕШЕНИЕ (раскомментируй для проверки)
# ============================================

df_spam = pd.DataFrame(messages, columns=['text', 'label'])

# Векторизация
from sklearn.feature_extraction.text import TfidfVectorizer
tfidf = TfidfVectorizer(max_features=50)
X_tfidf = tfidf.fit_transform(df_spam['text'])
y_spam = df_spam['label']

X_train, X_test, y_train, y_test = train_test_split(X_tfidf, y_spam, test_size=0.3, random_state=42)

from sklearn.linear_model import LogisticRegression
model = LogisticRegression()
model.fit(X_train, y_train)

y_pred = model.predict(X_test)
print(f"\nAccuracy: {accuracy_score(y_test, y_pred):.4f}")
print(f"F1-score: {f1_score(y_test, y_pred):.4f}")

# Тест на новых данных
test_msgs = ["Срочно переведите деньги!", "Увидимся в пятницу"]
test_vec = tfidf.transform(test_msgs)
preds = model.predict(test_vec)
for msg, pred in zip(test_msgs, preds):
    print(f"  '{msg}' → {'СПАМ' if pred == 1 else 'НЕ СПАМ'}")

# ============================================================
# ЗАДАЧА 2: Регрессия — Предсказание оценки студента (средняя)
# ============================================================

print("\n" + "=" * 60)
print("ЗАДАЧА 2: РЕГРЕССИЯ — ПРЕДСКАЗАНИЕ ОЦЕНКИ СТУДЕНТА")
print("=" * 60)

print("""
УСЛОВИЕ:
Даны данные о студентах: часы учёбы, посещаемость, домашние задания.
Предскажите итоговую оценку (0-100).

Шаги:
1. Создать датасет
2. Обучить LinearRegression и RandomForestRegressor
3. Сравнить MAE и R²
4. Определить самый важный признак
""")

np.random.seed(42)
n = 100

students = pd.DataFrame({
    'study_hours': np.random.uniform(5, 40, n),
    'attendance': np.random.uniform(50, 100, n),
    'homework_score': np.random.uniform(3, 10, n),
    'projects_count': np.random.randint(0, 5, n)
})

# Оценка зависит от признаков + шум
students['final_grade'] = (
    students['study_hours'] * 1.5 +
    students['attendance'] * 0.3 +
    students['homework_score'] * 5 +
    students['projects_count'] * 3 +
    np.random.normal(0, 5, n)
).clip(0, 100).round(1)

print(f"Датасет: {students.shape}")
print(students.head())

# TODO: Реши сам!
print("\nТвоё решение:")
print("# Напиши код здесь...")

# ============================================
# РЕШЕНИЕ
# ============================================

from sklearn.linear_model import LinearRegression
from sklearn.ensemble import RandomForestRegressor
from sklearn.preprocessing import StandardScaler

X_stud = students.drop('final_grade', axis=1)
y_stud = students['final_grade']

X_train, X_test, y_train, y_test = train_test_split(X_stud, y_stud, test_size=0.2, random_state=42)

# Линейная регрессия
scaler = StandardScaler()
X_train_s = scaler.fit_transform(X_train)
X_test_s = scaler.transform(X_test)

lr = LinearRegression()
lr.fit(X_train_s, y_train)
lr_pred = lr.predict(X_test_s)

print(f"\nLinear Regression:")
print(f"  MAE: {mean_absolute_error(y_test, lr_pred):.2f}")
print(f"  R²:  {r2_score(y_test, lr_pred):.4f}")

# Random Forest
rf = RandomForestRegressor(n_estimators=50, random_state=42)
rf.fit(X_train, y_train)
rf_pred = rf.predict(X_test)

print(f"\nRandom Forest:")
print(f"  MAE: {mean_absolute_error(y_test, rf_pred):.2f}")
print(f"  R²:  {r2_score(y_test, rf_pred):.4f}")

# Важность признаков
importance = pd.DataFrame({
    'feature': X_stud.columns,
    'importance': rf.feature_importances_
}).sort_values('importance', ascending=False)
print(f"\nВажность признаков:")
print(importance)

# ============================================================
# ЗАДАЧА 3: Кластеризация — Группировка песен (средняя)
# ============================================================

print("\n" + "=" * 60)
print("ЗАДАЧА 3: КЛАСТЕРИЗАЦИЯ — ГРУППИРОВКА ПЕСЕН")
print("=" * 60)

print("""
УСЛОВИЕ:
Даны характеристики песен. Найди естественные группы жанров.

Шаги:
1. Создать датасет с характеристиками песен
2. Определить оптимальное k (Elbow + Silhouette)
3. Применить K-Means
4. Охарактеризовать каждый кластер
""")

np.random.seed(42)

# Рок (громко, быстро, высокая энергия)
rock = pd.DataFrame({
    'tempo': np.random.normal(140, 15, 30),
    'energy': np.random.normal(0.8, 0.1, 30),
    'loudness': np.random.normal(-5, 2, 30),
    'acousticness': np.random.normal(0.1, 0.05, 30),
    'danceability': np.random.normal(0.5, 0.1, 30)
})

# Поп (танцевальная, средняя энергия)
pop = pd.DataFrame({
    'tempo': np.random.normal(120, 10, 40),
    'energy': np.random.normal(0.6, 0.1, 40),
    'loudness': np.random.normal(-7, 2, 40),
    'acousticness': np.random.normal(0.2, 0.1, 40),
    'danceability': np.random.normal(0.75, 0.08, 40)
})

# Акустика (тихо, медленно, акустично)
acoustic = pd.DataFrame({
    'tempo': np.random.normal(80, 15, 25),
    'energy': np.random.normal(0.3, 0.1, 25),
    'loudness': np.random.normal(-15, 3, 25),
    'acousticness': np.random.normal(0.85, 0.08, 25),
    'danceability': np.random.normal(0.4, 0.1, 25)
})

# Электроника (быстро, энергично, не акустично)
electronic = pd.DataFrame({
    'tempo': np.random.normal(130, 20, 35),
    'energy': np.random.normal(0.9, 0.05, 35),
    'loudness': np.random.normal(-4, 2, 35),
    'acousticness': np.random.normal(0.02, 0.01, 35),
    'danceability': np.random.normal(0.8, 0.08, 35)
})

songs = pd.concat([rock, pop, acoustic, electronic], ignore_index=True)
true_genres = ['рок']*30 + ['поп']*40 + ['акустика']*25 + ['электроника']*35

print(f"Датасет: {songs.shape}")
print(songs.head())

# TODO: Реши сам!
print("\nТвоё решение:")
print("# Напиши код здесь...")

# ============================================
# РЕШЕНИЕ
# ============================================

from sklearn.cluster import KMeans
from sklearn.metrics import silhouette_score
from sklearn.preprocessing import StandardScaler

scaler = StandardScaler()
songs_scaled = scaler.fit_transform(songs)

# Elbow method
inertias = []
sil_scores = []
for k in range(2, 8):
    km = KMeans(n_clusters=k, random_state=42, n_init=10)
    km.fit(songs_scaled)
    inertias.append(km.inertia_)
    sil_scores.append(silhouette_score(songs_scaled, km.labels_))

print(f"\nElbow:")
for k, (inertia, sil) in enumerate(zip(inertias, sil_scores), 2):
    print(f"  k={k}: Inertia={inertia:.0f}, Silhouette={sil:.4f}")

optimal_k = sil_scores.index(max(sil_scores)) + 2
print(f"\nОптимальное k: {optimal_k}")

# K-Means
km = KMeans(n_clusters=optimal_k, random_state=42, n_init=10)
labels = km.fit_predict(songs_scaled)

# Характеристика кластеров
songs['cluster'] = labels
print(f"\nХарактеристика кластеров:")
for i in range(optimal_k):
    cluster_data = songs[songs['cluster'] == i].mean()
    print(f"\nКластер {i} ({(labels==i).sum()} песен):")
    print(f"  Tempo: {cluster_data['tempo']:.0f}, Energy: {cluster_data['energy']:.2f}")
    print(f"  Loudness: {cluster_data['loudness']:.1f}, Acoustic: {cluster_data['acousticness']:.2f}")
    print(f"  Danceability: {cluster_data['danceability']:.2f}")

# ============================================================
# ЗАДАЧА 4: Multi-class классификация — Определение сорта ириса (лёгкая)
# ============================================================

print("\n" + "=" * 60)
print("ЗАДАЧА 4: MULTI-CLASS — ИРИСЫ (КЛАССИКА ML)")
print("=" * 60)

print("""
УСЛОВИЕ:
Классический датасет Iris. Определи сорт ириса по характеристикам.

Это классика — попробуй решить БЕЗ подсказок!

Шаги:
1. Загрузить iris из sklearn
2. Разделить на train/test
3. Обучить 3 разных классификатора
4. Сравнить accuracy
5. Построить confusion matrix
""")

# TODO: Реши сам!
from sklearn.datasets import load_iris

iris = load_iris()
X_iris = iris.data
y_iris = iris.target

print(f"Признаки: {iris.feature_names}")
print(f"Классы: {iris.target_names}")
print(f"Размер: {X_iris.shape}")

# Напиши код здесь...

# ============================================
# РЕШЕНИЕ
# ============================================

from sklearn.ensemble import RandomForestClassifier, GradientBoostingClassifier
from sklearn.svm import SVC
from sklearn.metrics import confusion_matrix, classification_report

X_train, X_test, y_train, y_test = train_test_split(X_iris, y_iris, test_size=0.2, random_state=42, stratify=y_iris)

models_iris = {
    'Logistic Regression': LogisticRegression(max_iter=200),
    'Random Forest': RandomForestClassifier(n_estimators=50, random_state=42),
    'SVM': SVC(kernel='rbf', random_state=42)
}

scaler_iris = StandardScaler()
X_train_s = scaler_iris.fit_transform(X_train)
X_test_s = scaler_iris.transform(X_test)

for name, model in models_iris.items():
    if name == 'SVM':
        model.fit(X_train_s, y_train)
        pred = model.predict(X_test_s)
    elif name == 'Logistic Regression':
        model.fit(X_train_s, y_train)
        pred = model.predict(X_test_s)
    else:
        model.fit(X_train, y_train)
        pred = model.predict(X_test)
    
    acc = accuracy_score(y_test, pred)
    print(f"\n{name}: Accuracy = {acc:.4f}")

# Confusion Matrix (лучшая модель)
best_model = models_iris['Random Forest']
best_model.fit(X_train, y_train)
y_pred = best_model.predict(X_test)

cm = confusion_matrix(y_test, y_pred)
print(f"\nConfusion Matrix:")
print(cm)
print(f"\nClassification Report:")
print(classification_report(y_test, y_pred, target_names=iris.target_names))

# ============================================================
# ЗАДАЧА 5: Feature Engineering — Предсказание выживших на Титанике (сложная)
# ============================================================

print("\n" + "=" * 60)
print("ЗАДАЧА 5: FEATURE ENGINEERING — ТИТАНИК")
print("=" * 60)

print("""
УСЛОВИЕ:
Синтетический датасет по мотивам Титаника. Нужно не только обучить модель,
но и создать новые признаки!

Исходные признаки:
- pclass: класс билета (1, 2, 3)
- sex: пол
- age: возраст
- fare: стоимость билета
- embarked: порт посадки (C, Q, S)
- has_cabin: есть ли каюта

ЗАДАНИЕ:
1. Создать НОВЫЕ признаки
2. Обработать пропуски
3. Обучить модель
4. Сравнить с baseline (без новых признаков)
""")

np.random.seed(42)
n = 500

titanic = pd.DataFrame({
    'pclass': np.random.choice([1, 2, 3], n, p=[0.25, 0.25, 0.50]),
    'sex': np.random.choice(['male', 'female'], n),
    'age': np.random.normal(30, 15, n).clip(1, 80).round(1),
    'fare': np.random.exponential(50, n).clip(5, 500).round(2),
    'embarked': np.random.choice(['C', 'Q', 'S'], n, p=[0.3, 0.1, 0.6]),
    'has_cabin': np.random.choice([0, 1], n, p=[0.7, 0.3])
})

# Пропуски в возрасте
titanic.loc[np.random.choice(n, 30, replace=False), 'age'] = np.nan

# Выживание зависит от признаков
survive_prob = (
    0.3 +
    (titanic['pclass'] == 1) * 0.3 +
    (titanic['pclass'] == 2) * 0.1 +
    (titanic['sex'] == 'female') * 0.25 +
    (titanic['age'] < 10) * 0.1 +
    (titanic['fare'] > 100) * 0.1 +
    (titanic['has_cabin'] == 1) * 0.05 -
    (titanic['age'] > 60) * 0.1
)
titanic['survived'] = (survive_prob.clip(0, 1) + np.random.normal(0, 0.1, n) > 0.5).astype(int)

print(f"Датасет: {titanic.shape}")
print(f"Пропуски:\n{titanic.isna().sum()}")
print(f"\nРаспределение выживших:")
print(titanic['survived'].value_counts())

# TODO: Реши сам!
print("\nТвоё решение:")
print("# 1. Создай новые признаки")
print("# 2. Обработай пропуски")
print("# 3. Обучи модель")
print("# 4. Сравни с baseline")

# ============================================
# РЕШЕНИЕ
# ============================================

def prepare_features(df, create_features=False):
    """Подготовка признаков"""
    df_prep = df.copy()
    
    # Обработка пропусков
    df_prep['age'] = df_prep['age'].fillna(df_prep['age'].median())
    
    # Кодирование пола
    df_prep['sex'] = (df_prep['sex'] == 'female').astype(int)
    
    # One-Hot Encoding для порта
    df_prep = pd.get_dummies(df_prep, columns=['embarked'], prefix='embarked', dtype=int)
    
    if create_features:
        # НОВЫЕ ПРИЗНАКИ
        # 1. Is_child
        df_prep['is_child'] = (df_prep['age'] < 12).astype(int)
        
        # 2. Is_elderly
        df_prep['is_elderly'] = (df_prep['age'] > 60).astype(int)
        
        # 3. Family_size (синтетический)
        df_prep['family_size'] = np.random.poisson(2, len(df_prep))
        
        # 4. Fare_per_person
        df_prep['fare_per_class'] = df_prep['fare'] / df_prep['pclass']
        
        # 5. Age × Class interaction
        df_prep['age_class'] = df_prep['age'] * df_prep['pclass']
        
        # 6. Title из синтетического
        df_prep['is_male_child'] = ((df_prep['sex'] == 0) & (df_prep['age'] < 12)).astype(int)
    
    return df_prep

# Baseline (без новых признаков)
df_baseline = prepare_features(titanic, create_features=False)
X_base = df_baseline.drop('survived', axis=1)
y_base = df_baseline['survived']

X_train, X_test, y_train, y_test = train_test_split(X_base, y_base, test_size=0.2, random_state=42)

model_base = RandomForestClassifier(n_estimators=100, random_state=42)
model_base.fit(X_train, y_train)
base_pred = model_base.predict(X_test)

print(f"\n{'='*40}")
print(f"BASELINE (без новых признаков):")
print(f"  Accuracy: {accuracy_score(y_test, base_pred):.4f}")
print(f"  F1: {f1_score(y_test, base_pred):.4f}")

# С новыми признаками
df_engineered = prepare_features(titanic, create_features=True)
X_eng = df_engineered.drop('survived', axis=1)
y_eng = df_engineered['survived']

X_train, X_test, y_train, y_test = train_test_split(X_eng, y_eng, test_size=0.2, random_state=42)

model_eng = RandomForestClassifier(n_estimators=100, random_state=42)
model_eng.fit(X_train, y_train)
eng_pred = model_eng.predict(X_test)

print(f"\nENGINEERED (с новыми признаками):")
print(f"  Accuracy: {accuracy_score(y_test, eng_pred):.4f}")
print(f"  F1: {f1_score(y_test, eng_pred):.4f}")

# Важность новых признаков
importance = pd.DataFrame({
    'feature': X_eng.columns,
    'importance': model_eng.feature_importances_
}).sort_values('importance', ascending=False)

print(f"\nТоп-10 важных признаков:")
print(importance.head(10))

improvement = f1_score(y_test, eng_pred) - f1_score(y_test, base_pred)
print(f"\nУлучшение F1: {improvement:+.4f}")

print("\n" + "=" * 60)
print("ВСЕ ЗАДАЧИ ВЫПОЛНЕНЫ!")
print("=" * 60)
print("""
💡 СОВЕТЫ:
1. Реши каждую задачу САМ, потом смотри решение
2. Меняй параметры моделей и смотри результат
3. Попробуй другие модели из шпаргалки
4. Засекай время — на олимпиаде оно ограничено!
""")
