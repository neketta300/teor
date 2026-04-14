"""
ОСНОВЫ АЛГОРИТМОВ PYTHON ДЛЯ ML
=================================
На олимпиаде могут быть задачи на:
1. Базовые алгоритмы (сортировки, поиск)
2. Работа со списками, словарями
3. Функции и лямбды
4. List comprehensions
5. Алгоритмы для обработки данных

Этот файл покрывает необходимые основы.
"""

import math
import numpy as np
from collections import Counter

# ============================================================
# ЧАСТЬ 1: LIST COMPREHENSIONS (генераторы списков)
# ============================================================

print("=" * 60)
print("ЧАСТЬ 1: LIST COMPREHENSIONS")
print("=" * 60)

# Обычный способ
squares = []
for i in range(10):
    squares.append(i ** 2)
print(f"Квадраты (обычный): {squares}")

# С list comprehension — БЫСТРЕЕ и ЧИЩЕ
squares = [i ** 2 for i in range(10)]
print(f"Квадраты (comprehension): {squares}")

# С условием
even_squares = [i ** 2 for i in range(10) if i % 2 == 0]
print(f"Квадраты чётных: {even_squares}")

# Для словарей
data = {'a': 1, 'b': 2, 'c': 3}
doubled = {k: v * 2 for k, v in data.items()}
print(f"Удвоенные значения: {doubled}")

# Инвертирование словаря
inverted = {v: k for k, v in data.items()}
print(f"Инвертированный: {inverted}")

# ============================================================
# ЧАСТЬ 2: Сортировки
# ============================================================

print("\n" + "=" * 60)
print("ЧАСТЬ 2: СОРТИРОВКИ")
print("=" * 60)

# Встроенная сортировка
numbers = [64, 34, 25, 12, 22, 11, 90]
print(f"Исходный: {numbers}")

# sorted() — возвращает новый список
sorted_asc = sorted(numbers)
sorted_desc = sorted(numbers, reverse=True)
print(f"По возрастанию: {sorted_asc}")
print(f"По убыванию: {sorted_desc}")

# sort() — сортирует на месте
numbers.sort()
print(f"После sort(): {numbers}")

# Сортировка сложных структур
students = [
    {'name': 'Анна', 'grade': 85},
    {'name': 'Борис', 'grade': 92},
    {'name': 'Вика', 'grade': 78},
    {'name': 'Глеб', 'grade': 92}
]

# По оценке
by_grade = sorted(students, key=lambda x: x['grade'], reverse=True)
print(f"\nПо оценке (убывание):")
for s in by_grade:
    print(f"  {s['name']}: {s['grade']}")

# По оценке, затем по имени (при равных)
by_grade_name = sorted(students, key=lambda x: (-x['grade'], x['name']))
print(f"\nПо оценке, затем по имени:")
for s in by_grade_name:
    print(f"  {s['name']}: {s['grade']}")

# ============================================================
# ЧАСТЬ 3: Lambda-функции
# ============================================================

print("\n" + "=" * 60)
print("ЧАСТЬ 3: LAMBDA-ФУНКЦИИ")
print("=" * 60)

# Обычная функция
def square(x):
    return x ** 2

# Lambda
square_lambda = lambda x: x ** 2

print(f"square(5) = {square(5)}")
print(f"lambda(5) = {square_lambda(5)}")

# Lambda с несколькими аргументами
add = lambda x, y: x + y
print(f"add(3, 4) = {add(3, 4)}")

# Использование с map, filter
numbers = [1, 2, 3, 4, 5, 6, 7, 8, 9, 10]

# map — применить функцию к каждому элементу
squared = list(map(lambda x: x ** 2, numbers))
print(f"\nmap (квадраты): {squared}")

# filter — отфильтровать элементы
evens = list(filter(lambda x: x % 2 == 0, numbers))
print(f"filter (чётные): {evens}")

# Комбинация
even_squares = list(map(lambda x: x ** 2, filter(lambda x: x % 2 == 0, numbers)))
print(f"filter + map (квадраты чётных): {even_squares}")

# ============================================================
# ЧАСТЬ 4: Словари — важные операции
# ============================================================

print("\n" + "=" * 60)
print("ЧАСТЬ 4: СЛОВАРИ")
print("=" * 60)

# Подсчёт частот (очень важно для ML!)
text = "яблоко груша яблоко апельсин яблоко груша"
words = text.split()

freq = {}
for word in words:
    freq[word] = freq.get(word, 0) + 1

print(f"Частоты слов: {freq}")

# Через defaultdict
from collections import Counter
freq_counter = Counter(words)
print(f"Через Counter: {dict(freq_counter)}")
print(f"Топ-2: {freq_counter.most_common(2)}")

# Сортировка словаря
scores = {'Анна': 85, 'Борис': 92, 'Вика': 78, 'Глеб': 95}

# По значению (оценке)
sorted_by_score = dict(sorted(scores.items(), key=lambda x: x[1], reverse=True))
print(f"\nПо оценке (убывание): {sorted_by_score}")

# ============================================================
# ЧАСТЬ 5: Бинарный поиск
# ============================================================

print("\n" + "=" * 60)
print("ЧАСТЬ 5: БИНАРНЫЙ ПОИСК")
print("=" * 60)

def binary_search(arr, target):
    """
    Бинарный поиск в отсортированном массиве.
    Возвращает индекс элемента или -1.
    Сложность: O(log n)
    """
    left, right = 0, len(arr) - 1
    
    while left <= right:
        mid = (left + right) // 2
        
        if arr[mid] == target:
            return mid
        elif arr[mid] < target:
            left = mid + 1
        else:
            right = mid - 1
    
    return -1

# Пример
sorted_array = [2, 5, 8, 12, 16, 23, 38, 56, 72, 91]
target = 23

idx = binary_search(sorted_array, target)
print(f"Массив: {sorted_array}")
print(f"Ищем: {target}")
print(f"Найден на индексе: {idx}")

# ============================================================
# ЧАСТЬ 6: Расстояние между точками (важно для k-NN, кластеризации)
# ============================================================

print("\n" + "=" * 60)
print("ЧАСТЬ 6: РАССТОЯНИЯ")
print("=" * 60)

import math

def euclidean_distance(p1, p2):
    """Евклидово расстояние"""
    return math.sqrt(sum((a - b) ** 2 for a, b in zip(p1, p2)))

def manhattan_distance(p1, p2):
    """Манхэттенское расстояние (сумма модулей разностей)"""
    return sum(abs(a - b) for a, b in zip(p1, p2))

def cosine_similarity(v1, v2):
    """Косинусное сходство (от -1 до 1)"""
    dot_product = sum(a * b for a, b in zip(v1, v2))
    norm_v1 = math.sqrt(sum(a ** 2 for a in v1))
    norm_v2 = math.sqrt(sum(b ** 2 for b in v2))
    return dot_product / (norm_v1 * norm_v2)

# Примеры
point_a = (1, 2, 3)
point_b = (4, 5, 6)

print(f"Точка A: {point_a}")
print(f"Точка B: {point_b}")
print(f"\nЕвклидово: {euclidean_distance(point_a, point_b):.4f}")
print(f"Манхэттенское: {manhattan_distance(point_a, point_b):.4f}")

vec1 = [1, 2, 3]
vec2 = [2, 4, 6]
print(f"\nВектор 1: {vec1}")
print(f"Вектор 2: {vec2}")
print(f"Cosine similarity: {cosine_similarity(vec1, vec2):.4f}")

# ============================================================
# ЧАСТЬ 7: k-NN алгоритм (k ближайших соседей)
# ============================================================

print("\n" + "=" * 60)
print("ЧАСТЬ 7: K-NN (K БЛИЖАЙШИХ СОСЕДЕЙ)")
print("=" * 60)

def knn_classify(train_data, train_labels, query, k=3):
    """
    Простая реализация k-NN для классификации.
    
    train_data: список точек обучения
    train_labels: метки классов
    query: точка для классификации
    k: число соседей
    """
    # 1. Считаем расстояния до всех точек
    distances = []
    for i, point in enumerate(train_data):
        dist = euclidean_distance(point, query)
        distances.append((dist, train_labels[i]))
    
    # 2. Сортируем по расстоянию
    distances.sort(key=lambda x: x[0])
    
    # 3. Берём k ближайших
    k_nearest = distances[:k]
    print(f"  {k} ближайших соседей: {k_nearest}")
    
    # 4. Голосование большинства
    from collections import Counter
    k_nearest_labels = [label for _, label in k_nearest]
    majority_vote = Counter(k_nearest_labels).most_common(1)[0][0]
    
    return majority_vote

# Учебные данные (2D точки)
train_data = [
    (1, 2), (2, 3), (3, 3),  # Класс A
    (6, 7), (7, 6), (8, 8)   # Класс B
]
train_labels = ['A', 'A', 'A', 'B', 'B', 'B']

# Тестируем
query_point = (3, 4)
prediction = knn_classify(train_data, train_labels, query_point, k=3)
print(f"\nТочка {query_point} -> Класс: {prediction}")

query_point2 = (7, 7)
prediction2 = knn_classify(train_data, train_labels, query_point2, k=3)
print(f"Точка {query_point2} -> Класс: {prediction2}")

# ============================================================
# ЧАСТЬ 8: Работа с файлами CSV (чтение/запись без pandas)
# ============================================================

print("\n" + "=" * 60)
print("ЧАСТЬ 8: РАБОТА С CSV")
print("=" * 60)

import csv
import io

# Создание CSV в памяти (для примера)
csv_data = """имя,возраст,город,зарплата
Анна,25,Минск,2500
Борис,30,Гомель,3000
Вика,35,Минск,3500
Глеб,28,Брест,2800"""

# Чтение CSV
print("Чтение CSV:")
reader = csv.DictReader(io.StringIO(csv_data))
for row in reader:
    print(f"  {row['имя']}: {row['зарплата']} руб.")

# Запись в файл (пример)
# with open('output.csv', 'w', newline='', encoding='utf-8') as f:
#     writer = csv.writer(f)
#     writer.writerow(['имя', 'возраст'])
#     writer.writerow(['Данила', 22])

# ============================================================
# ЧАСТЬ 9: Генераторы (экономия памяти)
# ============================================================

print("\n" + "=" * 60)
print("ЧАСТЬ 9: ГЕНЕРАТОРЫ")
print("=" * 60)

# List — хранит всё в памяти
squares_list = [x ** 2 for x in range(1000000)]
print(f"List размер: {len(squares_list)} элементов")

# Generator — генерирует по одному
squares_gen = (x ** 2 for x in range(1000000))
print(f"Generator: {type(squares_gen)}")
print(f"Первые 5: {[next(squares_gen) for _ in range(5)]}")

# Generator функция
def fibonacci(n):
    """Генератор чисел Фибоначчи"""
    a, b = 0, 1
    for _ in range(n):
        yield a
        a, b = b, a + b

fib = list(fibonacci(10))
print(f"\nФибоначчи (10): {fib}")

# ============================================================
# ЧАСТЬ 10: Рекурсия (может быть на олимпиаде)
# ============================================================

print("\n" + "=" * 60)
print("ЧАСТЬ 10: РЕКУРСИЯ")
print("=" * 60)

def factorial(n):
    """Факториал через рекурсию"""
    if n <= 1:
        return 1
    return n * factorial(n - 1)

def fibonacci_recursive(n):
    """Фибоначчи через рекурсию (неэффективно, но для понимания)"""
    if n <= 1:
        return n
    return fibonacci_recursive(n-1) + fibonacci_recursive(n-2)

print(f"5! = {factorial(5)}")
print(f"fib(10) = {fibonacci_recursive(10)}")

# ============================================================
# ЧАСТЬ 11: Практические задачи для олимпиады
# ============================================================

print("\n" + "=" * 60)
print("ЧАСТЬ 11: ПРАКТИЧЕСКИЕ ЗАДАЧИ")
print("=" * 60)

# --- Задача 1: Найти медиану списка ---
print("\n--- Медиана ---")
def find_median(lst):
    """Нахождение медианы"""
    sorted_lst = sorted(lst)
    n = len(sorted_lst)
    mid = n // 2
    
    if n % 2 == 0:
        return (sorted_lst[mid - 1] + sorted_lst[mid]) / 2
    return sorted_lst[mid]

numbers = [7, 1, 3, 6, 2, 9, 5]
print(f"Список: {numbers}")
print(f"Медиана: {find_median(numbers)}")
print(f"Проверка numpy: {np.median(numbers)}")

# --- Задача 2: Найти моду (часто встречающийся элемент) ---
print("\n--- Мода ---")
def find_mode(lst):
    """Нахождение моды"""
    freq = Counter(lst)
    return freq.most_common(1)[0][0]

data = [1, 2, 2, 3, 3, 3, 4, 4, 5]
print(f"Список: {data}")
print(f"Мода: {find_mode(data)}")

# --- Задача 3: Вычислить корреляцию Пирсона ---
print("\n--- Корреляция Пирсона ---")
def pearson_correlation(x, y):
    """Вычисление корреляции Пирсона вручную"""
    n = len(x)
    mean_x = sum(x) / n
    mean_y = sum(y) / n
    
    numerator = sum((xi - mean_x) * (yi - mean_y) for xi, yi in zip(x, y))
    
    sum_sq_x = sum((xi - mean_x) ** 2 for xi in x)
    sum_sq_y = sum((yi - mean_y) ** 2 for yi in y)
    
    denominator = math.sqrt(sum_sq_x * sum_sq_y)
    
    if denominator == 0:
        return 0
    
    return numerator / denominator

x = [1, 2, 3, 4, 5]
y = [2, 4, 5, 4, 5]
corr = pearson_correlation(x, y)
print(f"X: {x}")
print(f"Y: {y}")
print(f"Корреляция Пирсона: {corr:.4f}")
print(f"Проверка numpy: {np.corrcoef(x, y)[0, 1]:.4f}")

# --- Задача 4: Нормализация данных ---
print("\n--- Нормализация ---")
def normalize(lst):
    """Min-Max нормализация"""
    min_val = min(lst)
    max_val = max(lst)
    if max_val == min_val:
        return [0.0] * len(lst)
    return [(x - min_val) / (max_val - min_val) for x in lst]

data = [20, 40, 60, 80, 100]
print(f"Исходные: {data}")
print(f"Нормализованные: {normalize(data)}")

# --- Задача 5: Стандартизация (Z-score) ---
print("\n--- Стандартизация ---")
def standardize(lst):
    """Z-score стандартизация"""
    mean = sum(lst) / len(lst)
    variance = sum((x - mean) ** 2 for x in lst) / len(lst)
    std = math.sqrt(variance)
    
    if std == 0:
        return [0.0] * len(lst)
    
    return [(x - mean) / std for x in lst]

data = [2, 4, 4, 4, 5, 5, 7, 9]
print(f"Исходные: {data}")
std_data = standardize(data)
print(f"Стандартизированные: {[f'{x:.3f}' for x in std_data]}")
print(f"Среднее результата: {sum(std_data)/len(std_data):.6f}")
print(f"Стд результата: {math.sqrt(sum(x**2 for x in std_data)/len(std_data)):.6f}")

print("\n" + "=" * 60)
print("УРОК ЗАВЕРШЁН!")
print("=" * 60)
print("""
Что дальше:
1. Запусти все файлы и проверь вывод
2. Попробуй изменить параметры в задачах
3. Реши задачу классификации в ml_tasks/01_classification/
4. Изучи шпаргалку в cheatsheets/ml_models_when_to_use.md
""")
