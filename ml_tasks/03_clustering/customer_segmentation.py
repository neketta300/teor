"""
ЗАДАЧА ПО КЛАСТЕРИЗАЦИИ — Олимпиадный уровень
===============================================
Тема: Сегментация покупателей интернет-магазина

УСЛОВИЕ ЗАДАЧИ:
Интернет-магазин хочет понять типы своих покупателей для таргетированного
маркетинга. Даны данные о поведении клиентов. Нужно найти естественные
группы (кластеры) без предварительных меток.

ВХОДНЫЕ ДАННЫЕ:
- Частота покупок (сколько раз покупал за месяц)
- Средний чек (сколько тратит за одну покупку)
- Процент возвратов товаров
- Время на сайте (минуты за месяц)
- Число просмотренных страниц

ЗАДАНИЕ:
1. Загрузить и исследовать данные
2. Подготовить данные (масштабирование обязательно!)
3. Определить оптимальное число кластеров (Elbow + Silhouette)
4. Применить K-Means и DBSCAN
5. Охарактеризовать каждый кластер
6. Визуализировать результаты

Установка: pip install pandas numpy scikit-learn matplotlib seaborn
"""

import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
from sklearn.preprocessing import StandardScaler
from sklearn.cluster import KMeans, DBSCAN, AgglomerativeClustering
from sklearn.metrics import silhouette_score, calinski_harabasz_score

# ============================================================
# ШАГ 1: Генерация датасета
# ============================================================

print("=" * 60)
print("ШАГ 1: ГЕНЕРАЦИЯ ДАННЫХ")
print("=" * 60)

np.random.seed(42)

# Создаём 4 естественные группы покупателей

# Группа 1: "Частые, но дешёвые покупки" (50 клиентов)
group1 = pd.DataFrame({
    'frequency': np.random.normal(15, 3, 50),
    'avg_check': np.random.normal(500, 100, 50),
    'return_rate': np.random.normal(0.05, 0.02, 50),
    'time_on_site': np.random.normal(120, 20, 50),
    'pages_viewed': np.random.normal(30, 5, 50)
})

# Группа 2: "Редкие, но дорогие покупки" (40 клиентов)
group2 = pd.DataFrame({
    'frequency': np.random.normal(2, 1, 40),
    'avg_check': np.random.normal(5000, 1000, 40),
    'return_rate': np.random.normal(0.15, 0.05, 40),
    'time_on_site': np.random.normal(60, 15, 40),
    'pages_viewed': np.random.normal(15, 3, 40)
})

# Группа 3: "Активные исследователи" (60 клиентов)
group3 = pd.DataFrame({
    'frequency': np.random.normal(8, 2, 60),
    'avg_check': np.random.normal(2000, 500, 60),
    'return_rate': np.random.normal(0.10, 0.03, 60),
    'time_on_site': np.random.normal(300, 50, 60),
    'pages_viewed': np.random.normal(80, 15, 60)
})

# Группа 4: "Пассивные" (30 клиентов)
group4 = pd.DataFrame({
    'frequency': np.random.normal(1, 0.5, 30),
    'avg_check': np.random.normal(800, 200, 30),
    'return_rate': np.random.normal(0.20, 0.05, 30),
    'time_on_site': np.random.normal(30, 10, 30),
    'pages_viewed': np.random.normal(8, 2, 30)
})

# Объединяем
data = pd.concat([group1, group2, group3, group4], ignore_index=True)
data.columns = ['frequency', 'avg_check', 'return_rate', 'time_on_site', 'pages_viewed']

# Реальные метки (для проверки, на олимпиаде их НЕ БУДЕТ)
true_labels = np.array([0]*50 + [1]*40 + [2]*60 + [3]*30)

print(f"Размер датасета: {data.shape}")
print(f"\nПервые 10 строк:")
print(data.head(10))
print(f"\nСтатистика:")
print(data.describe())

# ============================================================
# ШАГ 2: Подготовка данных
# ============================================================

print("\n" + "=" * 60)
print("ШАГ 2: ПОДГОТОВКА ДАННЫХ")
print("=" * 60)

# Проверка пропусков
print(f"\nПропуски: {data.isna().sum().sum()}")

# Масштабирование — КРИТИЧЕСКИ ВАЖНО для кластеризации!
scaler = StandardScaler()
data_scaled = scaler.fit_transform(data)

print(f"\nМасштабирование выполнено:")
print(f"Среднее: {data_scaled.mean(axis=0).round(4)}")
print(f"Стд: {data_scaled.std(axis=0).round(4)}")

# ============================================================
# ШАГ 3: Определение оптимального k (Elbow Method + Silhouette)
# ============================================================

print("\n" + "=" * 60)
print("ШАГ 3: ОПТИМАЛЬНОЕ ЧИСЛО КЛАСТЕРОВ")
print("=" * 60)

# Elbow Method
inertias = []
silhouette_scores = []
k_range = range(2, 11)

for k in k_range:
    kmeans = KMeans(n_clusters=k, random_state=42, n_init=10)
    kmeans.fit(data_scaled)
    inertias.append(kmeans.inertia_)
    silhouette_scores.append(silhouette_score(data_scaled, kmeans.labels_))

print("\nМетод локтя (Inertia):")
for k, inertia in zip(k_range, inertias):
    print(f"  k={k}: {inertia:.1f}")

print("\nSilhouette Score:")
for k, score in zip(k_range, silhouette_scores):
    print(f"  k={k}: {score:.4f}")

# Визуализация Elbow
fig, axes = plt.subplots(1, 2, figsize=(14, 5))

axes[0].plot(k_range, inertias, 'bo-', linewidth=2, markersize=8)
axes[0].set_xlabel('Число кластеров (k)')
axes[0].set_ylabel('Inertia (WCSS)')
axes[0].set_title('Метод локтя (Elbow Method)')
axes[0].grid(True, alpha=0.3)

axes[1].plot(k_range, silhouette_scores, 'ro-', linewidth=2, markersize=8)
axes[1].set_xlabel('Число кластеров (k)')
axes[1].set_ylabel('Silhouette Score')
axes[1].set_title('Силуэтный коэффициент')
axes[1].grid(True, alpha=0.3)

plt.tight_layout()
plt.savefig('C:\\it chalenge\\ml_tasks\\03_clustering\\elbow_silhouette.png', dpi=150)
print("\nГрафик сохранён: elbow_silhouette.png")

# Оптимальное k (обычно выбирают по максимуму silhouette)
optimal_k = list(k_range)[np.argmax(silhouette_scores)]
print(f"\n✓ Оптимальное k (по Silhouette): {optimal_k}")

# ============================================================
# ШАГ 4: K-Means кластеризация
# ============================================================

print("\n" + "=" * 60)
print("ШАГ 4: K-MEANS КЛАСТЕРИЗАЦИЯ")
print("=" * 60)

kmeans = KMeans(n_clusters=optimal_k, random_state=42, n_init=10, max_iter=300)
kmeans_labels = kmeans.predict(data_scaled)
kmeans_centers = scaler.inverse_transform(kmeans.cluster_centers_)

print(f"Число кластеров: {optimal_k}")
print(f"Inertia: {kmeans.inertia_:.1f}")
print(f"Silhouette: {silhouette_score(data_scaled, kmeans_labels):.4f}")
print(f"Calinski-Harabasz: {calinski_harabasz_score(data_scaled, kmeans_labels):.1f}")

# Распределение по кластерам
print(f"\nРазмер кластеров:")
for i in range(optimal_k):
    count = (kmeans_labels == i).sum()
    print(f"  Кластер {i}: {count} клиентов ({count/len(data)*100:.1f}%)")

# Характеристика кластеров
print(f"\nХарактеристика кластеров (средние значения):")
cluster_data = data.copy()
cluster_data['cluster'] = kmeans_labels

for i in range(optimal_k):
    print(f"\n--- Кластер {i} ---")
    cluster_stats = cluster_data[cluster_data['cluster'] == i].mean()
    print(f"  Частота покупок: {cluster_stats['frequency']:.1f}")
    print(f"  Средний чек: {cluster_stats['avg_check']:.0f} руб.")
    print(f"  Процент возвратов: {cluster_stats['return_rate']:.1%}")
    print(f"  Время на сайте: {cluster_stats['time_on_site']:.0f} мин.")
    print(f"  Просмотрено страниц: {cluster_stats['pages_viewed']:.0f}")

# ============================================================
# ШАГ 5: DBSCAN (поиск кластеров произвольной формы)
# ============================================================

print("\n" + "=" * 60)
print("ШАГ 5: DBSCAN КЛАСТЕРИЗАЦИЯ")
print("=" * 60)

# DBSCAN сам определяет число кластеров
# eps — радиус окрестности, min_samples — минимальное число точек
dbscan = DBSCAN(eps=0.5, min_samples=5)
dbscan_labels = dbscan.fit_predict(data_scaled)

n_clusters_dbscan = len(set(dbscan_labels)) - (1 if -1 in dbscan_labels else 0)
n_noise = list(dbscan_labels).count(-1)

print(f"Найдено кластеров: {n_clusters_dbscan}")
print(f"Выбросов (шум): {n_noise} ({n_noise/len(data)*100:.1f}%)")
print(f"Silhouette (без шума): {silhouette_score(data_scaled[dbscan_labels != -1], dbscan_labels[dbscan_labels != -1]):.4f}")

print(f"\nРазмер кластеров DBSCAN:")
for i in range(n_clusters_dbscan):
    count = (dbscan_labels == i).sum()
    print(f"  Кластер {i}: {count} клиентов ({count/len(data)*100:.1f}%)")
if n_noise > 0:
    print(f"  Шум (-1): {n_noise} клиентов ({n_noise/len(data)*100:.1f}%)")

# ============================================================
# ШАГ 6: Иерархическая кластеризация
# ============================================================

print("\n" + "=" * 60)
print("ШАГ 6: ИЕРАРХИЧЕСКАЯ КЛАСТЕРИЗАЦИЯ")
print("=" * 60)

agg = AgglomerativeClustering(n_clusters=optimal_k)
agg_labels = agg.fit_predict(data_scaled)

print(f"Число кластеров: {optimal_k}")
print(f"Silhouette: {silhouette_score(data_scaled, agg_labels):.4f}")
print(f"Calinski-Harabasz: {calinski_harabasz_score(data_scaled, agg_labels):.1f}")

# ============================================================
# ШАГ 7: Сравнение методов
# ============================================================

print("\n" + "=" * 60)
print("ШАГ 7: СРАВНЕНИЕ МЕТОДОВ")
print("=" * 60)

# K-Means с лучшим k
km_sil = silhouette_score(data_scaled, kmeans_labels)
km_ch = calinski_harabasz_score(data_scaled, kmeans_labels)

# DBSCAN (без шума)
mask = dbscan_labels != -1
dbscan_sil = silhouette_score(data_scaled[mask], dbscan_labels[mask]) if mask.sum() > 1 else 0

# Иерархическая
agg_sil = silhouette_score(data_scaled, agg_labels)
agg_ch = calinski_harabasz_score(data_scaled, agg_labels)

comparison = pd.DataFrame({
    'Метод': ['K-Means', 'DBSCAN*', 'Иерархическая'],
    'Silhouette': [km_sil, dbscan_sil, agg_sil],
    'Calinski-Harabasz': [km_ch, 0, agg_ch],
    'Число кластеров': [optimal_k, n_clusters_dbscan, optimal_k]
})
print(comparison)
print("\n*DBSCAN: Silhouette рассчитан без учёта выбросов")

# ============================================================
# ШАГ 8: Визуализация (PCA для 2D проекции)
# ============================================================

print("\n" + "=" * 60)
print("ШАГ 8: ВИЗУАЛИЗАЦИЯ")
print("=" * 60)

from sklearn.decomposition import PCA

# PCA для проекции в 2D
pca = PCA(n_components=2)
data_2d = pca.fit_transform(data_scaled)

print(f"Объяснённая дисперсия: {pca.explained_variance_ratio_}")
print(f"Суммарная: {pca.explained_variance_ratio_.sum():.2%}")

fig, axes = plt.subplots(1, 3, figsize=(18, 5))

# K-Means
scatter1 = axes[0].scatter(data_2d[:, 0], data_2d[:, 1], c=kmeans_labels, 
                           cmap='viridis', alpha=0.7, s=50, edgecolors='k')
axes[0].set_title(f'K-Means (k={optimal_k})')
axes[0].set_xlabel('PC1')
axes[0].set_ylabel('PC2')
axes[0].grid(True, alpha=0.3)

# DBSCAN
scatter2 = axes[1].scatter(data_2d[:, 0], data_2d[:, 1], c=dbscan_labels, 
                           cmap='tab10', alpha=0.7, s=50, edgecolors='k')
axes[1].set_title(f'DBSCAN ({n_clusters_dbscan} кластеров)')
axes[1].set_xlabel('PC1')
axes[1].set_ylabel('PC2')
axes[1].grid(True, alpha=0.3)

# Иерархическая
scatter3 = axes[2].scatter(data_2d[:, 0], data_2d[:, 1], c=agg_labels, 
                           cmap='plasma', alpha=0.7, s=50, edgecolors='k')
axes[2].set_title(f'Иерархическая (k={optimal_k})')
axes[2].set_xlabel('PC1')
axes[2].set_ylabel('PC2')
axes[2].grid(True, alpha=0.3)

plt.tight_layout()
plt.savefig('C:\\it chalenge\\ml_tasks\\03_clustering\\clusters_comparison.png', dpi=150)
print("График сохранён: clusters_comparison.png")

# ============================================================
# ШАГ 9: Характеристика лучшего кластера
# ============================================================

print("\n" + "=" * 60)
print("ШАГ 9: ПРОФИЛИРОВАНИЕ КЛАСТЕРОВ")
print("=" * 60)

# Названия кластеров на основе характеристик
def name_cluster(row):
    """Даём название кластеру на основе характеристик"""
    freq_norm = (row['frequency'] - data['frequency'].mean()) / data['frequency'].std()
    check_norm = (row['avg_check'] - data['avg_check'].mean()) / data['avg_check'].std()
    time_norm = (row['time_on_site'] - data['time_on_site'].mean()) / data['time_on_site'].std()
    
    if freq_norm > 0.5 and check_norm < -0.5:
        return "Частые покупки (мелкие)"
    elif freq_norm < -0.5 and check_norm > 0.5:
        return "Редкие покупки (крупные)"
    elif time_norm > 0.5:
        return "Активные исследователи"
    else:
        return "Пассивные клиенты"

print("\nПрофили кластеров K-Means:")
for i in range(optimal_k):
    cluster_mean = cluster_data[cluster_data['cluster'] == i].mean()
    name = name_cluster(cluster_mean)
    count = (kmeans_labels == i).sum()
    print(f"\n  Кластер {i} ({count} чел.): {name}")
    print(f"    Частота: {cluster_mean['frequency']:.1f}, Чек: {cluster_mean['avg_check']:.0f} руб.")
    print(f"    Возвраты: {cluster_mean['return_rate']:.1%}, Время: {cluster_mean['time_on_site']:.0f} мин")

# ============================================================
# ШАГ 10: Как определить параметры DBSCAN
# ============================================================

print("\n" + "=" * 60)
print("ШАГ 10: ПОДБОР ПАРАМЕТРОВ DBSCAN")
print("=" * 60)

# K-distance graph для подбора eps
from sklearn.neighbors import NearestNeighbors

# Расстояние до k-го ближайшего соседа
k = 5
nn = NearestNeighbors(n_neighbors=k)
nn.fit(data_scaled)
distances, _ = nn.kneighbors(data_scaled)
distances = np.sort(distances[:, -1])  # Расстояние до k-го соседа

plt.figure(figsize=(8, 5))
plt.plot(range(len(distances)), distances, linewidth=1.5)
plt.axhline(y=0.5, color='r', linestyle='--', alpha=0.7, label='eps=0.5')
plt.axhline(y=1.0, color='g', linestyle='--', alpha=0.7, label='eps=1.0')
plt.xlabel('Точки (отсортированы)')
plt.ylabel(f'Расстояние до {k}-го соседа')
plt.title('K-distance Graph (для подбора eps)')
plt.legend()
plt.grid(True, alpha=0.3)
plt.tight_layout()
plt.savefig('C:\\it chalenge\\ml_tasks\\03_clustering\\k_distance.png', dpi=150)
print("График сохранён: k_distance.png")

print("""
Как использовать K-distance graph:
1. Сортируем расстояния до k-го соседа
2. Ищем "локоть" — резкий перегиб кривой
3. Значение расстояния в точке перегиба = хороший eps
4. На графике видно: eps ≈ 0.5-0.7 — хороший выбор
""")

# ============================================================
# ШАГ 11: Чек-лист для олимпиады
# ============================================================

print("\n" + "=" * 60)
print("ШАГ 11: ЧЕК-ЛИСТ КЛАСТЕРИЗАЦИИ")
print("=" * 60)
print("""
✅ 1. Проверить пропуски → заполнить или удалить
✅ 2. ОБЯЗАТЕЛЬНО масштабировать данные (StandardScaler)
✅ 3. Elbow Method → найти оптимальное k
✅ 4. Silhouette Score → подтвердить k
✅ 5. K-Means — базовый вариант (знаю k)
✅ 6. DBSCAN — если не знаю k, возможны выбросы
✅ 7. Охарактеризовать каждый кластер (средние значения)
✅ 8. Визуализировать (PCA для 2D)
✅ 9. Дать осмысленные имена кластерам

ПАРМЕТРЫ DBSCAN:
- eps: использовать K-distance graph
- min_samples: обычно = n_features + 1 или 5-10

МЕТРИКИ:
- Silhouette: от -1 до 1 (чем больше, тем лучше)
- Calinski-Harabasz: чем больше, тем лучше
- Inertia: чем меньше, тем лучше (но падает с ростом k)

КОГДА ИСПОЛЬЗОВАТЬ:
- K-Means: знаю k, кластеры сферические, нет выбросов
- DBSCAN: не знаю k, кластеры произвольной формы, есть выбросы
- Иерархическая: нужна иерархия, мало данных
""")

print("\n" + "=" * 60)
print("ЗАДАЧА ВЫПОЛНЕНА!")
print("=" * 60)
