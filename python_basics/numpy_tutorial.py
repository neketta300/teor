"""
NumPy - основа машинного обучения в Python
============================================
NumPy (Numerical Python) - библиотека для работы с многомерными массивами
и математическими операциями. Все ML-библиотеки (scikit-learn, TensorFlow, PyTorch)
построены на NumPy.

Установка: pip install numpy
"""

import numpy as np

# ============================================================
# ЧАСТЬ 1: Создание массивов
# ============================================================

print("=" * 60)
print("ЧАСТЬ 1: СОЗДАНИЕ МАССИВОВ")
print("=" * 60)

# Из обычного списка
arr = np.array([1, 2, 3, 4, 5])
print(f"Из списка: {arr}")

# Двумерный массив (матрица)
matrix = np.array([[1, 2, 3], [4, 5, 6]])
print(f"Матрица 2x3:\n{matrix}")

# Специальные массивы
zeros = np.zeros((3, 4))  # Матрица 3x4 из нулей
ones = np.ones((2, 3))    # Матрица 2x3 из единиц
full = np.full((2, 2), 7) # Матрица 2x2, заполненная 7
identity = np.eye(3)      # Единичная матрица 3x3

print(f"\nНули 3x4:\n{zeros}")
print(f"\nЕдиницы 2x3:\n{ones}")
print(f"\nЗаполненная 2x2:\n{full}")
print(f"\nЕдиничная 3x3:\n{identity}")

# Массивы с диапазонами
range_arr = np.arange(0, 10, 2)  # start, stop, step
linspace = np.linspace(0, 1, 5)  # 5 точек от 0 до 1

print(f"\narange(0, 10, 2): {range_arr}")
print(f"linspace(0, 1, 5): {linspace}")

# Случайные числа (очень важно для ML!)
random_arr = np.random.rand(5)           # Равномерное распределение [0, 1)
random_normal = np.random.randn(5)       # Нормальное распределение (среднее=0, станд=1)
random_int = np.random.randint(0, 100, 5) # Случайные целые от 0 до 100

print(f"\nСлучайные [0,1): {random_arr}")
print(f"Нормальное распределение: {random_normal}")
print(f"Случайные целые: {random_int}")

# ============================================================
# ЧАСТЬ 2: Атрибуты массивов
# ============================================================

print("\n" + "=" * 60)
print("ЧАСТЬ 2: АТРИБУТЫ МАССИВОВ")
print("=" * 60)

data = np.array([[1, 2, 3, 4], [5, 6, 7, 8], [9, 10, 11, 12]])

print(f"Массив:\n{data}")
print(f"Размерность (shape): {data.shape}")      # (строки, столбцы)
print(f"Число измерений (ndim): {data.ndim}")     # 2
print(f"Общее число элементов (size): {data.size}")  # 12
print(f"Тип данных (dtype): {data.dtype}")         # int32/int64

# ============================================================
# ЧАСТЬ 3: Индексация и срезы
# ============================================================

print("\n" + "=" * 60)
print("ЧАСТЬ 3: ИНДЕКСАЦИЯ И СРЕЗЫ")
print("=" * 60)

data = np.array([[1, 2, 3], [4, 5, 6], [7, 8, 9]])
print(f"Массив:\n{data}")

# Доступ к элементам
print(f"\ndata[0, 1] = {data[0, 1]}")  # Строка 0, столбец 1
print(f"data[2, 2] = {data[2, 2]}")    # Строка 2, столбец 2

# Срезы
print(f"\nПервая строка: {data[0, :]}")
print(f"Второй столбец: {data[:, 1]}")
print(f"Подматрица 2x2:\n{data[0:2, 0:2]}")

# Логическая индексация (ВАЖНО для фильтрации данных!)
data = np.array([1, 2, 3, 4, 5, 6, 7, 8, 9, 10])
mask = data > 5
print(f"\nМассив: {data}")
print(f"Элементы > 5: {data[mask]}")
print(f"Чётные: {data[data % 2 == 0]}")

# ============================================================
# ЧАСТЬ 4: Математические операции
# ============================================================

print("\n" + "=" * 60)
print("ЧАСТЬ 4: МАТЕМАТИЧЕСКИЕ ОПЕРАЦИИ")
print("=" * 60)

a = np.array([1, 2, 3, 4])
b = np.array([5, 6, 7, 8])

print(f"a = {a}")
print(f"b = {b}")

# Поэлементные операции
print(f"\na + b = {a + b}")
print(f"a - b = {a - b}")
print(f"a * b = {a * b}")  # Поэлементное умножение (НЕ матричное!)
print(f"a / b = {a / b}")
print(f"a ** 2 = {a ** 2}")

# Скалярные операции
print(f"\na + 10 = {a + 10}")
print(f"a * 3 = {a * 3}")

# Статистика
data = np.array([[1, 2, 3], [4, 5, 6]])
print(f"\nДанные:\n{data}")
print(f"Сумма всех: {data.sum()}")
print(f"Среднее: {data.mean()}")
print(f"Медиана: {np.median(data)}")
print(f"Стандартное отклонение: {data.std():.2f}")
print(f"Минимум: {data.min()}, Максимум: {data.max()}")

# По осям
print(f"\nСумма по столбцам (axis=0): {data.sum(axis=0)}")
print(f"Сумма по строкам (axis=1): {data.sum(axis=1)}")

# ============================================================
# ЧАСТЬ 5: Изменение формы массива (reshape)
# ============================================================

print("\n" + "=" * 60)
print("ЧАСТЬ 5: RESHAPE (ИЗМЕНЕНИЕ ФОРМЫ)")
print("=" * 60)

arr = np.arange(1, 13)  # [1, 2, ..., 12]
print(f"Исходный: {arr}")

# Преобразование в матрицу
matrix = arr.reshape(3, 4)
print(f"reshape(3, 4):\n{matrix}")

matrix2 = arr.reshape(4, 3)
print(f"\nreshape(4, 3):\n{matrix2}")

# -1 означает "автоматически вычислить"
auto = arr.reshape(2, -1)
print(f"\nreshape(2, -1):\n{auto}")

# Flatten - обратно в одномерный
flat = matrix.flatten()
print(f"\nflatten(): {flat}")

# ============================================================
# ЧАСТЬ 6: Объединение и разделение массивов
# ============================================================

print("\n" + "=" * 60)
print("ЧАСТЬ 6: ОБЪЕДИНЕНИЕ И РАЗДЕЛЕНИЕ")
print("=" * 60)

a = np.array([[1, 2], [3, 4]])
b = np.array([[5, 6], [7, 8]])

# По вертикали
v_stack = np.vstack([a, b])
print(f"vstack:\n{v_stack}")

# По горизонтали
h_stack = np.hstack([a, b])
print(f"\nhstack:\n{h_stack}")

# Разделение
data = np.arange(1, 10)
parts = np.split(data, 3)
print(f"\nsplit([1..9], 3): {parts}")

# ============================================================
# ЧАСТЬ 7: Линейная алгебра (важно для понимания ML!)
# ============================================================

print("\n" + "=" * 60)
print("ЧАСТЬ 7: ЛИНЕЙНАЯ АЛГЕБРА")
print("=" * 60)

a = np.array([[1, 2], [3, 4]])
b = np.array([[5, 6], [7, 8]])

# Матричное умножение
print(f"a:\n{a}")
print(f"b:\n{b}")
print(f"\nМатричное умножение a @ b:\n{a @ b}")
print(f"Или np.dot(a, b):\n{np.dot(a, b)}")

# Транспонирование
print(f"\nТранспонирование a.T:\n{a.T}")

# Определитель, обратная матрица
det = np.linalg.det(a)
inv = np.linalg.inv(a)
print(f"Определитель a: {det:.2f}")
print(f"Обратная матрица a:\n{inv}")

# ============================================================
# ЧАСТЬ 8: Практические ML-задачи
# ============================================================

print("\n" + "=" * 60)
print("ЧАСТЬ 8: ПРАКТИЧЕСКИЕ ML-ЗАДАЧИ")
print("=" * 60)

# --- Задача 1: Нормализация данных ---
# В ML данные нужно приводить к одному масштабу
print("\n--- Нормализация (Min-Max scaling) ---")
data = np.array([20, 45, 60, 80, 100])
normalized = (data - data.min()) / (data.max() - data.min())
print(f"Исходные: {data}")
print(f"Нормализованные: {normalized}")

# --- Задача 2: Стандартизация (Z-score) ---
# Приведение к среднему=0, станд.отклонению=1
print("\n--- Стандартизация (Z-score) ---")
data = np.array([2, 4, 4, 4, 5, 5, 7, 9])
standardized = (data - data.mean()) / data.std()
print(f"Исходные: {data}")
print(f"Среднее исходных: {data.mean():.2f}")
print(f"Стандартизированные: {standardized}")
print(f"Среднее стандартизированных: {standardized.mean():.2f}")
print(f"Стд.отклонение стандартизированных: {standardized.std():.2f}")

# --- Задача 3: Генерация синтетических данных для классификации ---
print("\n--- Генерация данных для классификации ---")
np.random.seed(42)  # Для воспроизводимости

# Класс 0: точки вокруг (2, 2)
class_0 = np.random.randn(50, 2) + np.array([2, 2])
# Класс 1: точки вокруг (6, 6)
class_1 = np.random.randn(50, 2) + np.array([6, 6])

X = np.vstack([class_0, class_1])  # Признаки (100 точек, 2 признака)
y = np.array([0] * 50 + [1] * 50)  # Метки классов

print(f"Признаки X: форма {X.shape}")
print(f"Метки y: форма {y.shape}")
print(f"Первые 5 точек X:\n{X[:5]}")
print(f"Первые 5 меток y: {y[:5]}")

# --- Задача 4: Вычисление евклидова расстояния ---
print("\n--- Евклидово расстояние между точками ---")
point1 = np.array([1, 2, 3])
point2 = np.array([4, 5, 6])
distance = np.sqrt(np.sum((point1 - point2) ** 2))
# Или проще:
distance_np = np.linalg.norm(point1 - point2)
print(f"Точка 1: {point1}")
print(f"Точка 2: {point2}")
print(f"Евклидово расстояние: {distance:.2f}")
print(f"Через np.linalg.norm: {distance_np:.2f}")

# --- Задача 5: Cosine similarity (мера похожести) ---
print("\n--- Cosine Similarity ---")
vec1 = np.array([1, 2, 3])
vec2 = np.array([2, 4, 6])
cosine_sim = np.dot(vec1, vec2) / (np.linalg.norm(vec1) * np.linalg.norm(vec2))
print(f"Вектор 1: {vec1}")
print(f"Вектор 2: {vec2}")
print(f"Cosine similarity: {cosine_sim:.4f}")
print("(1.0 = полностью похожи, 0.0 = не похожи)")

print("\n" + "=" * 60)
print("УРОК ЗАВЕРШЁН!")
print("=" * 60)
print("\nСледующий шаг: pandas_tutorial.py — работа с табличными данными")
