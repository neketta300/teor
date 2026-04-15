# Все направления

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

### Python основы
1. ✅ `python_basics/numpy_tutorial.py` — массивы, математика, ML-задачи
2. ✅ `python_basics/pandas_tutorial.py` — таблицы, фильтрация, группировка
3. ✅ `python_basics/algorithms_basics.py` — сортировки, k-NN, расстояния

**Как запускать:**
```bash
python "C:\it chalenge\python_basics\numpy_tutorial.py"
```

### Машинное обучение
1. ✅ `ml_tasks/01_classification/churn_prediction.py` — классификация
2. ✅ `ml_tasks/02_regression/car_price_prediction.py` — регрессия
3. ✅ `ml_tasks/03_clustering/customer_segmentation.py` — кластеризация
4. ✅ `ml_tasks/practice_tasks.py` — 5 задач для практики

**Ключевые понятия:**
- Accuracy, Precision, Recall, F1, ROC-AUC (классификация)
- MAE, MSE, RMSE, R² (регрессия)
- Silhouette, Elbow, Inertia (кластеризация)
- Train/Test split, масштабирование, кросс-валидация

### Анализ данных
1. ✅ `data_analysis/exploratory_data_analysis.py` — EDA, визуализация, статистика
2. ✅ `data_analysis/ab_testing.py` — A/B тестирование

**Ключевые понятия:**
- Гистограммы, boxplot, scatter plot, heatmap
- t-test, ANOVA, Chi-square, Shapiro-Wilk
- Доверительные интервалы, p-value

### Кибербезопасность
1. ✅ `cybersecurity/web_security_cheatsheet.md` — изучить шпаргалку
2. ✅ `cybersecurity/log_analysis.py` — анализ логов

**Ключевые понятия:**
- SQLi, XSS, IDOR, Broken Auth
- DevTools, Burp Suite, ffuf, dirsearch
- HTTP-методы, коды ответов, заголовки

### Повторение и практика
- Реши `practice_tasks.py` БЕЗ подсказок
- Повтори шпаргалки

## 💡 Советы 

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

Вот краткая и практичная инструкция по стандартному рабочему процессу в GitLab. Все команды проверены на современных версиях Git (2.23+).

### 🔧 0. Подготовка (делается один раз)
```bash
git config --global user.name "Ваше Имя"
git config --global user.email "ваш@email.com"
```
*Для доступа к GitLab используйте SSH-ключ или HTTPS + Personal Access Token (Settings → Access Tokens в GitLab).*

---

### 📥 1. Клонирование репозитория
```bash
git clone <URL_репозитория>
cd <имя_папки_репозитория>
```
> 💡 URL можно взять на главной странице репозитория в GitLab (кнопка `Clone` → `SSH` или `HTTPS`).

---

### 🌿 2. Создание и переключение на свою ветку
```bash
git switch -c feature/название-задачи
```
*`-c` = create + switch. Имя ветки начинайте с префикса: `feature/`, `bugfix/`, `hotfix/`, `docs/` и т.д.*

---

### 📝 3. Внесение изменений и коммит
```bash
# Проверка статуса
git status

# Добавление изменённых файлов (или укажите конкретные файлы)
git add .

# Фиксация изменений
git commit -m "feat: добавил валидацию формы логина"
```
> 💡 Пишите понятные сообщения. Можно сделать несколько коммитов по ходу работы.

---

### 🚀 4. Отправка ветки в GitLab
```bash
git push -u origin feature/название-задачи
```
* `-u` (upstream) запоминает связь локальной ветки с удалённой. После этого в будущем достаточно писать просто `git push`.
* В консоли Git обычно выводит прямую ссылку на создание Merge Request.

---

### 🔀 5. Создание Merge Request (MR) в GitLab
1. Перейдите в репозиторий на gitlab.com
2. Слева в меню появится уведомление: `New branch` → `Create merge request`
3. Выберите целевую ветку (обычно `main` или `master`)
4. Добавьте описание, reviewers, назначьте labels (если нужно)
5. Нажмите `Create merge request`

После ревью и одобрения MR будет смёржен в основную ветку.

---

### 🛠 Полезные команды на каждый день
| Задача | Команда |
|--------|---------|
| Посмотреть текущую ветку | `git branch --show-current` |
| Список локальных веток | `git branch` |
| Обновить ветку из удалённой | `git pull origin main` (если нужно подтянуть чужие изменения) |
| Отменить последний коммит (только локально) | `git reset --soft HEAD~1` |
| Вернуть изменённый файл в исходное состояние | `git restore <файл>` |

---

### ⚠️ Важные нюансы
- Никогда не пушьте напрямую в `main`/`master`. Работайте только через feature-ветки.
- Если перед пушем появились конфликты, сначала сделайте `git pull --rebase origin main`, разрешите конфликты, затем `git push`.
- Для автоматизации работы с GitLab из терминала можно установить утилиту [`glab`](https://gitlab.com/gitlab-org/cli) (аналог `gh` для GitHub).

Если нужно, могу показать пример с настройкой SSH-ключа, настройкой `.gitignore` или автоматическим CI/CD пайплайном.


**Всего: ~4,600+ строк кода и документации**

---

