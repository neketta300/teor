"""
ЗАДАЧА ПО КЛАССИФИКАЦИИ — Олимпиадный уровень
==============================================
Тема: Классификация клиентов банка — уйдёт ли клиент (Churn Prediction)

УСЛОВИЕ ЗАДАЧИ:
Банк предоставляет данные о клиентах. Нужно предсказать, уйдёт ли клиент
к конкурентам (churn = 1) или останется (churn = 0).

ВХОДНЫЕ ДАННЫЕ:
- Возраст клиента
- Баланс на счёте
- Число продуктов банка
- Есть ли кредитная карта
- Активный клиент или нет
- Оценка удовлетворённости (1-5)

ЗАДАНИЕ:
1. Загрузить и исследовать данные
2. Подготовить данные (обработка пропусков, кодирование)
3. Обучить модель классификации
4. Оценить качество модели
5. Сделать прогноз для новых данных

Установка зависимостей:
pip install pandas numpy scikit-learn matplotlib seaborn
"""

import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import StandardScaler
from sklearn.linear_model import LogisticRegression
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import (
    accuracy_score, precision_score, recall_score, 
    f1_score, confusion_matrix, classification_report,
    roc_auc_score, roc_curve
)

# ============================================================
# ШАГ 1: Генерация учебного датасета (на олимпиаде будет CSV)
# ============================================================

print("=" * 60)
print("ШАГ 1: ЗАГРУЗКА ДАННЫХ")
print("=" * 60)

np.random.seed(42)
n_clients = 500

# Генерация признаков
data = pd.DataFrame({
    'age': np.random.randint(18, 70, n_clients),
    'balance': np.random.normal(5000, 3000, n_clients).astype(int),
    'num_products': np.random.randint(1, 6, n_clients),
    'has_credit_card': np.random.choice([0, 1], n_clients),
    'is_active': np.random.choice([0, 1], n_clients, p=[0.3, 0.7]),
    'satisfaction': np.random.randint(1, 6, n_clients)
})

# Целевая переменная: churn зависит от признаков
# Неактивные + недовольные клиенты чаще уходят
churn_prob = (
    0.3 -
    0.2 * data['is_active'] +
    0.15 * (data['satisfaction'] <= 2).astype(int) -
    0.1 * (data['num_products'] >= 3).astype(int) +
    np.random.normal(0, 0.1, n_clients)
)
data['churn'] = (churn_prob > 0.3).astype(int)

print(f"Размер датасета: {data.shape}")
print(f"\nПервые 10 строк:")
print(data.head(10))
print(f"\nРаспределение целевой переменной:")
print(data['churn'].value_counts())
print(f"\nБазовая статистика:")
print(data.describe())

# ============================================================
# ШАГ 2: Исследовательский анализ данных (EDA)
# ============================================================

print("\n" + "=" * 60)
print("ШАГ 2: ИССЛЕДОВАТЕЛЬСКИЙ АНАЛИЗ")
print("=" * 60)

# Средние значения по группам
print("\nСредние значения по группам (churn = 0 vs churn = 1):")
print(data.groupby('churn').mean())

# Корреляция с целевой переменной
print("\nКорреляция признаков с churn:")
correlations = data.corr()['churn'].sort_values(ascending=False)
print(correlations)

# ============================================================
# ШАГ 3: Подготовка данных
# ============================================================

print("\n" + "=" * 60)
print("ШАГ 3: ПОДГОТОВКА ДАННЫХ")
print("=" * 60)

# Разделение на признаки (X) и целевую переменную (y)
X = data.drop('churn', axis=1)
y = data['churn']

print(f"Признаки X: {X.shape}")
print(f"Метки y: {y.shape}")

# Разделение на обучающую и тестовую выборки
# 80% на обучение, 20% на тест
X_train, X_test, y_train, y_test = train_test_split(
    X, y, test_size=0.2, random_state=42, stratify=y
)

print(f"\nОбучающая выборка: {X_train.shape[0]} примеров")
print(f"Тестовая выборка: {X_test.shape[0]} примеров")
print(f"Доля churn в train: {y_train.mean():.2%}")
print(f"Доля churn в test: {y_test.mean():.2%}")

# Масштабирование признаков (ВАЖНО для многих алгоритмов!)
scaler = StandardScaler()
X_train_scaled = scaler.fit_transform(X_train)
X_test_scaled = scaler.transform(X_test)

print("\nМасштабирование выполнено (среднее ≈ 0, станд.отклонение ≈ 1)")
print(f"Среднее X_train_scaled: {X_train_scaled.mean(axis=0).round(2)}")
print(f"Стд X_train_scaled: {X_train_scaled.std(axis=0).round(2)}")

# ============================================================
# ШАГ 4: Обучение моделей
# ============================================================

print("\n" + "=" * 60)
print("ШАГ 4: ОБУЧЕНИЕ МОДЕЛЕЙ")
print("=" * 60)

# --- Модель 1: Логистическая регрессия ---
print("\n--- Логистическая регрессия ---")
lr = LogisticRegression(random_state=42, max_iter=1000)
lr.fit(X_train_scaled, y_train)

y_pred_lr = lr.predict(X_test_scaled)
y_prob_lr = lr.predict_proba(X_test_scaled)[:, 1]

print(f"Accuracy: {accuracy_score(y_test, y_pred_lr):.4f}")
print(f"Precision: {precision_score(y_test, y_pred_lr):.4f}")
print(f"Recall: {recall_score(y_test, y_pred_lr):.4f}")
print(f"F1-score: {f1_score(y_test, y_pred_lr):.4f}")
print(f"ROC-AUC: {roc_auc_score(y_test, y_prob_lr):.4f}")

# Важность признаков (коэффициенты)
feature_importance = pd.DataFrame({
    'feature': X.columns,
    'coefficient': lr.coef_[0]
}).sort_values('coefficient', ascending=False)
print(f"\nВажность признаков (коэффициенты):")
print(feature_importance)

# --- Модель 2: Случайный лес ---
print("\n--- Случайный лес ---")
rf = RandomForestClassifier(n_estimators=100, random_state=42)
rf.fit(X_train, y_train)  # Случайному лесу не нужно масштабирование

y_pred_rf = rf.predict(X_test)
y_prob_rf = rf.predict_proba(X_test)[:, 1]

print(f"Accuracy: {accuracy_score(y_test, y_pred_rf):.4f}")
print(f"Precision: {precision_score(y_test, y_pred_rf):.4f}")
print(f"Recall: {recall_score(y_test, y_pred_rf):.4f}")
print(f"F1-score: {f1_score(y_test, y_pred_rf):.4f}")
print(f"ROC-AUC: {roc_auc_score(y_test, y_prob_rf):.4f}")

# Важность признаков
feature_importance_rf = pd.DataFrame({
    'feature': X.columns,
    'importance': rf.feature_importances_
}).sort_values('importance', ascending=False)
print(f"\nВажность признаков (Random Forest):")
print(feature_importance_rf)

# ============================================================
# ШАГ 5: Детальный анализ результатов
# ============================================================

print("\n" + "=" * 60)
print("ШАГ 5: ДЕТАЛЬНЫЙ АНАЛИЗ")
print("=" * 60)

# Матрица ошибок (Confusion Matrix)
print("\n--- Матрица ошибок (Random Forest) ---")
cm = confusion_matrix(y_test, y_pred_rf)
print(cm)
print("""
Значение:
[[TN  FP]   TN = True Negative  (правильно: не уйдёт)
 [FN  TP]]  TP = True Positive  (правильно: уйдёт)
            FP = False Positive (ошибка: сказали уйдёт, но нет)
            FN = False Negative (ошибка: сказали останется, но ушёл)
""")

# Полный отчёт
print("\n--- Классификационный отчёт ---")
print(classification_report(y_test, y_pred_rf, target_names=['Останется', 'Уйдёт']))

# Что означают метрики:
print("""
МЕТРИКИ КЛАССИФИКАЦИИ:
- Accuracy: Общая точность = (TP + TN) / Все. Не всегда хороша при дисбалансе!
- Precision: Точность положительных = TP / (TP + FP). 
             Среди тех, кого назвали "уйдёт" — сколько реально ушло?
- Recall: Полнота = TP / (TP + FN). 
          Среди реально ушедших — сколько мы нашли?
- F1-score: Гармоническое среднее Precision и Recall. 
            Одна метрика для оценки баланса.
- ROC-AUC: Способность модели различать классы. 
           1.0 = идеально, 0.5 = как случайное угадывание.
""")

# ============================================================
# ШАГ 6: Прогноз для новых клиентов
# ============================================================

print("\n" + "=" * 60)
print("ШАГ 6: ПРОГНОЗ ДЛЯ НОВЫХ КЛИЕНТОВ")
print("=" * 60)

new_clients = pd.DataFrame({
    'age': [25, 45, 60],
    'balance': [1000, 8000, 15000],
    'num_products': [1, 4, 3],
    'has_credit_card': [0, 1, 1],
    'is_active': [0, 1, 1],
    'satisfaction': [2, 5, 3]
})

print("Новые клиенты:")
print(new_clients)

# Прогноз
predictions = rf.predict(new_clients)
probabilities = rf.predict_proba(new_clients)[:, 1]

for i, (pred, prob) in enumerate(zip(predictions, probabilities)):
    status = "УЙДЁТ" if pred == 1 else "ОСТАНЕТСЯ"
    print(f"Клиент {i+1}: {status} (вероятность ухода: {prob:.2%})")

# ============================================================
# ШАГ 7: Как улучшить результат (для олимпиады)
# ============================================================

print("\n" + "=" * 60)
print("ШАГ 7: КАК УЛУЧШИТЬ РЕЗУЛЬТАТ")
print("=" * 60)
print("""
1. ПОДБОР ГИПЕРПАРАМЕТРОВ:
   from sklearn.model_selection import GridSearchCV
   params = {'n_estimators': [50, 100, 200], 'max_depth': [5, 10, None]}
   grid = GridSearchCV(RandomForestClassifier(), params, cv=5)
   grid.fit(X_train, y_train)

2. КРОСС-ВАЛИДАЦИЯ:
   from sklearn.model_selection import cross_val_score
   scores = cross_val_score(rf, X, y, cv=5, scoring='f1')
   print(f"Средний F1: {scores.mean():.4f} (+/- {scores.std() * 2:.4f})")

3. ДРУГИЕ МОДЕЛИ:
   - GradientBoostingClassifier
   - XGBoost / LightGBM / CatBoost (очень мощные!)
   - SVM (Support Vector Machine)

4. FEATURE ENGINEERING:
   - Создание новых признаков (возраст / продукты, баланс / возраст)
   - Удаление неважных признаков
   - Обработка выбросов

5. БАЛАНСИРОВКА КЛАССОВ:
   class_weight='balanced' в моделях
   SMOTE для синтетического баланса
""")

print("\n" + "=" * 60)
print("ЗАДАЧА ВЫПОЛНЕНА!")
print("=" * 60)
