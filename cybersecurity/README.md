# 🔒 Кибербезопасность — Анализ логов веб-сервера

## 📁 Файлы раздела

| Файл | Тема | Строк |
|------|------|-------|
| `log_analysis.py` | Анализ логов, обнаружение атак | 400+ |
| `web_security_cheatsheet.md` | Шпаргалка: уязвимости, инструменты | 400+ |

---

## 📋 Задача

Даны **логи веб-сервера** (Apache/Nginx). Нужно обнаружить **подозрительную активность** и классифицировать типы атак.

### Типы атак для обнаружения

| Атака | Описание | Пример |
|-------|----------|--------|
| **SQL-инъекция** | Внедрение SQL-кода в запрос | `id=1' OR '1'='1` |
| **XSS** | Внедрение JavaScript в страницу | `<script>alert('XSS')</script>` |
| **Сканирование** | Поиск уязвимых эндпоинтов | `GET /admin, /wp-admin, /.env` |
| **Brute-force** | Подбор пароля перебором | 10× `POST /login` с 401 |

---

## 🔄 Полный пайплайн

```
┌─────────────────────────────────────────────────────┐
│  ШАГ 1: Генерация логов                              │
│  Нормальные + SQLi + XSS + Scan + Brute              │
└──────────────────────┬──────────────────────────────┘
                       ▼
┌─────────────────────────────────────────────────────┐
│  ШАГ 2: Парсинг                                      │
│  Regex → DataFrame (IP, путь, статус, User-Agent)    │
└──────────────────────┬──────────────────────────────┘
                       ▼
┌─────────────────────────────────────────────────────┐
│  ШАГ 3: SQL-инъекции                                 │
│  Regex-паттерны в URL: UNION, OR 1=1, DROP TABLE     │
└──────────────────────┬──────────────────────────────┘
                       ▼
┌─────────────────────────────────────────────────────┐
│  ШАГ 4: XSS                                          │
│  Regex: <script>, <img onerror=, alert()             │
└──────────────────────┬──────────────────────────────┘
                       ▼
┌─────────────────────────────────────────────────────┐
│  ШАГ 5: Сканирование                                 │
│  Подозрительные пути + User-Agent (Nmap, sqlmap)     │
└──────────────────────┬──────────────────────────────┘
                       ▼
┌─────────────────────────────────────────────────────┐
│  ШАГ 6: Brute-force                                  │
│  Много POST /login с 401 → failed/total > 80%        │
└──────────────────────┬──────────────────────────────┘
                       ▼
┌─────────────────────────────────────────────────────┐
│  ШАГ 7: Сводный отчёт                                │
│  Распределение атак, IP-адреса, статус-коды          │
└──────────────────────┬──────────────────────────────┘
                       ▼
┌─────────────────────────────────────────────────────┐
│  ШАГ 8: Визуализация                                 │
│  Пай-чарт, бар-чарт, статус-коды, User-Agent         │
└──────────────────────┬──────────────────────────────┘
                       ▼
┌─────────────────────────────────────────────────────┐
│  ШАГ 9: Рекомендации                                 │
│  Блокировка IP, WAF, rate limiting, CAPTCHA          │
└─────────────────────────────────────────────────────┘
```

---

## 📖 Пошаговый разбор

### ШАГ 1: Формат логов

**Apache/Nginx Combined Log Format:**

```
192.168.1.10 - - [10/Apr/2026:08:15:30 +0300] "GET / HTTP/1.1" 200 5123 "-" "Mozilla/5.0 Chrome/120.0"
│              │    │                           │    │          │    │     │    └─ User-Agent
│              │    │                           │    │          │    │     └─ Referrer
│              │    │                           │    │          │    └─ Размер ответа (байты)
│              │    │                           │    │          └─ HTTP статус-код
│              │    │                           │    └─ Запрашиваемый путь
│              │    │                           └─ HTTP-метод
│              │    └─ Дата и время
│              └─ Идентификатор (обычно -)
└─ IP-адрес клиента
```

**HTTP статус-коды:**
- `200` — OK (успех)
- `201` — Created (создано)
- `401` — Unauthorized (не авторизован)
- `403` — Forbidden (запрещено)
- `404` — Not Found (не найдено)
- `500` — Internal Server Error (ошибка сервера)

---

### ШАГ 2: Парсинг логов через Regex

```python
import re

# Регулярное выражение для парсинга
log_pattern = r'(\S+) - - \[([^\]]+)\] "(\S+) ([^"]*?) HTTP/\d\.\d" (\d+) (\d+) "[^"]*" "([^"]*)"'

def parse_logs(log_text):
    records = []
    for line in log_text.strip().split('\n'):
        match = re.match(log_pattern, line)
        if match:
            ip, timestamp, method, path, status, size, user_agent = match.groups()
            records.append({
                'ip': ip,
                'timestamp': timestamp,
                'method': method,
                'path': path,
                'status': int(status),
                'size': int(size),
                'user_agent': user_agent
            })
    return pd.DataFrame(records)

df = parse_logs(all_logs)
```

**Разбор regex:**
```
(\S+)          → IP-адрес (любой текст без пробелов)
 - -           → буквально " - - "
\[([^\]]+)\]   → дата в квадратных скобках
"(\S+)         → HTTP-метод (GET, POST, ...)
([^"]*?)       → путь (всё до следующей кавычки)
HTTP/\d\.\d"   → буквально "HTTP/1.1"
(\d+)          → статус-код (число)
(\d+)          → размер (число)
"[^"]*"        → referrer (пропускаем)
"([^"]*)"      → User-Agent
```

**Результат:**
```
       ip                     timestamp method  ...  status  size      user_agent
0  192.168.1.10  10/Apr/2026:08:15:30 +0300    GET  ...     200  5123  Mozilla/5.0 ...
1  192.168.1.10  10/Apr/2026:08:15:31 +0300    GET  ...     200  1234  Mozilla/5.0 ...
```

---

### ШАГ 3: Обнаружение SQL-инъекций

#### Что такое SQL-инъекция?

Атакующий внедряет SQL-код в URL-параметры или формы, чтобы получить доступ к базе данных.

**Примеры атак:**

| Запрос | Что делает |
|--------|-----------|
| `id=1' OR '1'='1` | Всегда TRUE → возвращает ВСЕ строки |
| `id=1 UNION SELECT username,password FROM users` | Извлекает логины и пароли |
| `id=1; DROP TABLE users--` | Удаляет таблицу |
| `id=1 AND 1=1` | Проверка: если SQL работает |
| `q=' UNION SELECT NULL,NULL,NULL--` | Подбор числа столбцов |

#### Паттерны для обнаружения

```python
sqli_patterns = [
    r"(?i)(union\s+select)",           # UNION SELECT
    r"(?i)(or\s+'?1'?\s*=\s*'?1)",     # OR '1'='1', OR 1=1
    r"(?i)(drop\s+table)",             # DROP TABLE
    r"(?i)(and\s+\d+\s*=\s*\d+)",      # AND 1=1
    r"(?i)(select\s+.*\s+from\s+)",    # SELECT ... FROM
    r"(?i)(--\s*$)",                   # SQL-комментарий --
    r"['\"]?\s*;\s*(drop|select|...)", # ;DROP, ;SELECT
    r"%27",                            # URL-encoded '
    r"%3D",                            # URL-encoded =
]

def detect_sqli(path):
    # Декодируем URL-encoded символы
    decoded = path.replace('%27', "'").replace('%3D', '=')
                        .replace('%3C', '<').replace('%3E', '>')
    for pattern in sqli_patterns:
        if re.search(pattern, decoded):
            return True
    return False

df['is_sqli'] = df['path'].apply(detect_sqli)
sqli_attacks = df[df['is_sqli']]
```

**`(?i)`** — без учёта регистра (работает и для `UNION SELECT`, и для `union select`).
**`\s+`** — один или более пробелов (атакующий может вставить `UNION  SELECT` с двумя пробелами).

---

### ШАГ 4: Обнаружение XSS

#### Что такое XSS?

**XSS (Cross-Site Scripting)** — атакующий внедряет JavaScript в страницу, чтобы выполнить код в браузере жертвы.

**Примеры атак:**

| Запрос | Что делает |
|--------|-----------|
| `<script>alert('XSS')</script>` | Выводит popup |
| `<img src=x onerror=alert(1)>` | Выполняет код при загрузке картинки |
| `<svg onload=alert(document.cookie)>` | Крадёт cookie |
| `javascript:alert(1)` | Выполняет JS через протокол |

#### Паттерны

```python
xss_patterns = [
    r"(?i)(<script)",               # <script>
    r"(?i)(<img\s+src\s*=)",        # <img src=
    r"(?i)(onerror\s*=)",           # onerror=
    r"(?i)(onload\s*=)",            # onload=
    r"(?i)(<svg)",                  # <svg>
    r"(?i)(alert\s*\()",            # alert()
    r"(?i)(javascript\s*:)",        # javascript:
    r"%3Cscript",                   # URL-encoded <script
    r"%3Cimg",                      # URL-encoded <img
    r"%3Csvg",                      # URL-encoded <svg
]

def detect_xss(path):
    for pattern in xss_patterns:
        if re.search(pattern, path, re.IGNORECASE):
            return True
    return False
```

**Последствия XSS:**
- Кража cookie и сессий
- Перенаправление на фишинговый сайт
- Выполнение действий от имени пользователя

---

### ШАГ 5: Обнаружение сканирования

#### Что такое сканирование?

Атакующий перебирает URL-адреса, чтобы найти уязвимые эндпоинты: админки, конфиги, бэкапы.

**Подозрительные пути:**

| Путь | Что там | Опасность |
|------|---------|-----------|
| `/admin` | Панель администратора | Подбор пароля |
| `/wp-admin` | WordPress админка | Эксплуатация CMS |
| `/phpmyadmin` | Управление БД | SQL-атаки |
| `/.env` | Переменные окружения | Утечка API-ключей |
| `/.git/config` | Git-конфиг | Утечка кода |
| `/backup.sql` | Бэкап БД | Полная утечка данных |
| `/config.php` | Конфиг | Утечка паролей БД |
| `/server-status` | Статус сервера | Информация для атаки |

**Подозрительные User-Agent:**
- `Nmap` — сканер портов
- `Nikto` — сканер веб-уязвимостей
- `sqlmap` — автоматические SQL-инъекции
- `DirBuster`, `gobuster`, `dirsearch` — сканеры директорий

```python
suspicious_paths = [
    r"(?i)(/admin)", r"(?i)(/wp-admin)", r"(?i)(/phpmyadmin)",
    r"(?i)(/\.env)", r"(?i)(/\.git)", r"(?i)(/backup)",
    r"(?i)(/config)", r"(?i)(/server-status)",
]

suspicious_ua = [
    r"(?i)(nmap)", r"(?i)(nikto)", r"(?i)(sqlmap)",
    r"(?i)(dirbuster)", r"(?i)(gobuster)", r"(?i)(dirsearch)",
]

def detect_scan(row):
    for pattern in suspicious_paths:
        if re.search(pattern, row['path']):
            return True
    for pattern in suspicious_ua:
        if re.search(pattern, row['user_agent']):
            return True
    return False

df['is_scan'] = df.apply(detect_scan, axis=1)
```

---

### ШАГ 6: Обнаружение Brute-force

#### Что такое Brute-force?

Атакующий перебирает пароли, отправляя много запросов `POST /login` с разными паролями.

**Как обнаружить:**

```python
# Все попытки входа
login_attempts = df[(df['method'] == 'POST') & (df['path'] == '/login')]

# Группировка по IP
brute_check = login_attempts.groupby('ip').agg({
    'status': ['count', lambda x: (x == 401).sum(), lambda x: (x == 200).sum()]
})
brute_check.columns = ['total', 'failed', 'success']
brute_check['fail_rate'] = brute_check['failed'] / brute_check['total']

# Brute-force: много попыток + высокий процент неудач
brute_ips = brute_check[(brute_check['total'] >= 5) & (brute_check['fail_rate'] > 0.8)]
```

**Признаки brute-force:**
1. **Много попыток** — `total >= 5` (5+ запросов `/login`)
2. **Высокий процент неудач** — `fail_rate > 0.8` (80%+ с кодом 401)
3. **Один IP** — все запросы с одного адреса
4. **Подозрительный User-Agent** — `python-requests`, `curl`, скрипты

**Пример из логов:**
```
10.0.0.80 - - [10/Apr/2026:13:00:00] "POST /login" 401  ← пароль неверный
10.0.0.80 - - [10/Apr/2026:13:00:01] "POST /login" 401  ← ещё
10.0.0.80 - - [10/Apr/2026:13:00:01] "POST /login" 401  ← ещё
... (10 раз)
10.0.0.80 - - [10/Apr/2026:13:00:05] "POST /login" 200  ← подобрал!

User-Agent: python-requests/2.31.0  ← скрипт, не браузер
```

---

### ШАГ 7: Сводный отчёт

```python
# Классификация каждого запроса
df['attack_type'] = 'normal'
df.loc[df['is_sqli'], 'attack_type'] = 'SQL-инъекция'
df.loc[df['is_xss'], 'attack_type'] = 'XSS'
df.loc[df['is_scan'], 'attack_type'] = 'Сканирование'
df.loc[df['is_brute'], 'attack_type'] = 'Brute-force'

# Распределение
attack_summary = df['attack_type'].value_counts()
```

**Пример результата:**
```
normal           10  (25.0%)
SQL-инъекция      6  (15.0%)
XSS               4  (10.0%)
Сканирование     12  (30.0%)
Brute-force      10  (25.0%)
```

---

### ШАГ 9: Рекомендации

```
═══════════════════════════════════════════
       ОТЧЁТ ПО АНАЛИЗУ ЛОГОВ
═══════════════════════════════════════════

📊 ОБЩАЯ СТАТИСТИКА:
  • Всего запросов:       42
  • Атакующих запросов:   32 (76.2%)
  • Уникальных атакующих: 4

🔍 ОБНАРУЖЕННЫЕ АТАКИ:
  • SQL-инъекция: 6 запросов от 1 IP
    - 10.0.0.50
  • XSS: 4 запросов от 1 IP
    - 10.0.0.60
  • Сканирование: 12 запросов от 1 IP
    - 10.0.0.70
  • Brute-force: 10 запросов от 1 IP
    - 10.0.0.80

🛡️ РЕКОМЕНДАЦИИ:
  1. Заблокировать IP-адреса атакующих
  2. Настроить WAF-правила для SQLi и XSS
  3. Включить rate limiting на /login
  4. Добавить CAPTCHA после N попыток входа
  5. Убрать чувствительные эндпоинты (/.env, /.git)
  6. Настроить логирование и мониторинг
═══════════════════════════════════════════
```

---

## 🛡️ Шпаргалка: меры защиты

| Атака | Мера защиты | Как работает |
|-------|------------|-------------|
| **SQL-инъекция** | Prepared Statements | SQL-код и данные разделяются |
| **SQL-инъекция** | WAF (Web Application Firewall) | Фильтрует запросы по паттернам |
| **SQL-инъекция** | Экранирование ввода | `'` → `\'` |
| **XSS** | Output Encoding | `<` → `&lt;` в HTML |
| **XSS** | Content Security Policy (CSP) | Запрещает inline-скрипты |
| **XSS** | Sanitization | Удаляет теги `<script>` |
| **Brute-force** | Rate Limiting | Максимум 5 попыток/мин |
| **Brute-force** | CAPTCHA | После 3 неудачных попыток |
| **Brute-force** | Блокировка IP | После N попыток — бан на 1 час |
| **Сканирование** | Убрать эндпоинты | Нет `/.env` — нечего найти |
| **Сканирование** | robots.txt | Запретить индексацию |
| **Все** | Логирование + мониторинг | Быстрое обнаружение |

---

## 📖 OWASP Top 10 (основные уязвимости)

| # | Уязвимость | Описание |
|---|-----------|----------|
| 1 | **Injection** | SQL, NoSQL, OS-команды |
| 2 | **Broken Authentication** | Слабые пароли, утечка сессий |
| 3 | **Sensitive Data Exposure** | Передача данных без шифрования |
| 4 | **XML External Entities (XXE)** | Чтение файлов через XML |
| 5 | **Broken Access Control** | IDOR — доступ к чужим данным |
| 6 | **Security Misconfiguration** | Дефолтные пароли, открытые порты |
| 7 | **XSS** | Внедрение скриптов |
| 8 | **Insecure Deserialization** | RCE через сериализованные объекты |
| 9 | **Using Components with Known Vulnerabilities** | Устаревшие библиотеки |
| 10 | **Insufficient Logging & Monitoring** | Атаки не замечены |

---

## 🔧 Инструменты (из шпаргалки)

| Инструмент | Для чего | Пример команды |
|-----------|----------|---------------|
| **DevTools (F12)** | Анализ запросов, cookies | Network tab → Headers |
| **Burp Suite** | Перехват и модификация запросов | Proxy → Intercept |
| **sqlmap** | Автоматические SQL-инъекции | `sqlmap -u "http://site/page?id=1"` |
| **Nmap** | Сканирование портов | `nmap -sV 192.168.1.1` |
| **Nikto** | Сканирование веб-уязвимостей | `nikto -h http://site` |
| **DirBuster / gobuster** | Сканирование директорий | `gobuster dir -u http://site -w wordlist.txt` |
| **dirsearch** | Сканирование директорий | `python3 dirsearch.py -u http://site` |

---

## 🚀 Запуск

```bash
python "C:\itChalenge\cybersecurity\log_analysis.py"
```

## 📦 Зависимости

```bash
pip install pandas numpy matplotlib seaborn
```
