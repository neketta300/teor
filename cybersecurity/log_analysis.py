"""
ЗАДАЧА ПО КИБЕРБЕЗОПАСНОСТИ — Анализ HTTP-логов
==================================================
Тема: Обнаружение атак в логах веб-сервера

УСЛОВИЕ:
Даны логи веб-сервера. Нужно обнаружить подозрительную активность
и классифицировать типы атак.

ТИПЫ АТАК ДЛЯ ОБНАРУЖЕНИЯ:
- SQL-инъекции
- XSS-попытки
- Сканирование директорий
- Brute-force авторизация
- Подозрительные User-Agent

Установка: pip install pandas numpy matplotlib seaborn
"""

import pandas as pd
import numpy as np
import re
import matplotlib.pyplot as plt
import seaborn as sns

# Настройка стиля
sns.set_style("whitegrid")

# ============================================================
# ЧАСТЬ 1: Генерация логов
# ============================================================

print("=" * 60)
print("ЧАСТЬ 1: ГЕНЕРАЦИЯ ЛОГОВ ВЕБ-СЕРВЕРА")
print("=" * 60)

# Формат Apache/Nginx Combined Log:
# IP - - [дата] "METHOD /path HTTP/1.1" статус размер "referrer" "user-agent"

normal_logs = """192.168.1.10 - - [10/Apr/2026:08:15:30 +0300] "GET / HTTP/1.1" 200 5123 "-" "Mozilla/5.0 (Windows NT 10.0; Win64; x64) Chrome/120.0"
192.168.1.10 - - [10/Apr/2026:08:15:31 +0300] "GET /css/style.css HTTP/1.1" 200 1234 "/index.html" "Mozilla/5.0 (Windows NT 10.0; Win64; x64) Chrome/120.0"
192.168.1.10 - - [10/Apr/2026:08:15:31 +0300] "GET /js/app.js HTTP/1.1" 200 8901 "/index.html" "Mozilla/5.0 (Windows NT 10.0; Win64; x64) Chrome/120.0"
192.168.1.11 - - [10/Apr/2026:08:20:15 +0300] "GET /about HTTP/1.1" 200 3456 "-" "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15) Safari/605.1"
192.168.1.11 - - [10/Apr/2026:08:20:20 +0300] "GET /products HTTP/1.1" 200 7890 "-" "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15) Safari/605.1"
192.168.1.11 - - [10/Apr/2026:08:20:25 +0300] "POST /api/cart HTTP/1.1" 201 234 "/products" "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15) Safari/605.1"
192.168.1.12 - - [10/Apr/2026:08:25:00 +0300] "GET /contact HTTP/1.1" 200 2345 "-" "Mozilla/5.0 (X11; Linux x86_64) Firefox/121.0"
192.168.1.12 - - [10/Apr/2026:08:25:05 +0300] "POST /contact/submit HTTP/1.1" 200 123 "/contact" "Mozilla/5.0 (X11; Linux x86_64) Firefox/121.0"
192.168.1.13 - - [10/Apr/2026:09:00:00 +0300] "GET /api/products?page=1 HTTP/1.1" 200 4567 "-" "Mozilla/5.0 (Windows NT 10.0) Chrome/120.0"
192.168.1.13 - - [10/Apr/2026:09:00:05 +0300] "GET /api/products?page=2 HTTP/1.1" 200 4567 "-" "Mozilla/5.0 (Windows NT 10.0) Chrome/120.0"
"""

# SQL-инъекции
sqli_logs = """10.0.0.50 - - [10/Apr/2026:10:15:00 +0300] "GET /products?id=1'+OR+'1'%3D'1 HTTP/1.1" 200 12345 "-" "Mozilla/5.0 (Windows NT 10.0) Chrome/119.0"
10.0.0.50 - - [10/Apr/2026:10:15:05 +0300] "GET /products?id=1+UNION+SELECT+username,password+FROM+users-- HTTP/1.1" 500 234 "-" "Mozilla/5.0 (Windows NT 10.0) Chrome/119.0"
10.0.0.50 - - [10/Apr/2026:10:15:10 +0300] "GET /products?id=1;+DROP+TABLE+users-- HTTP/1.1" 500 123 "-" "Mozilla/5.0 (Windows NT 10.0) Chrome/119.0"
10.0.0.50 - - [10/Apr/2026:10:15:15 +0300] "POST /login HTTP/1.1" 200 890 "-" "Mozilla/5.0 (Windows NT 10.0) Chrome/119.0"
10.0.0.50 - - [10/Apr/2026:10:15:20 +0300] "GET /users?id=1+AND+1%3D1 HTTP/1.1" 200 567 "-" "Mozilla/5.0 (Windows NT 10.0) Chrome/119.0"
10.0.0.50 - - [10/Apr/2026:10:15:25 +0300] "GET /search?q='+UNION+SELECT+NULL,NULL,NULL-- HTTP/1.1" 200 345 "-" "Mozilla/5.0 (Windows NT 10.0) Chrome/119.0"
"""

# XSS-попытки
xss_logs = """10.0.0.60 - - [10/Apr/2026:11:00:00 +0300] "GET /search?q=%3Cscript%3Ealert('XSS')%3C/script%3E HTTP/1.1" 200 4567 "-" "Mozilla/5.0 (Windows NT 10.0) Chrome/118.0"
10.0.0.60 - - [10/Apr/2026:11:00:05 +0300] "GET /comment?text=%3Cimg+src%3Dx+onerror%3Dalert(1)%3E HTTP/1.1" 200 3456 "-" "Mozilla/5.0 (Windows NT 10.0) Chrome/118.0"
10.0.0.60 - - [10/Apr/2026:11:00:10 +0300] "POST /feedback HTTP/1.1" 200 234 "-" "Mozilla/5.0 (Windows NT 10.0) Chrome/118.0"
10.0.0.60 - - [10/Apr/2026:11:00:15 +0300] "GET /profile?name=%3Csvg+onload%3Dalert(document.cookie)%3E HTTP/1.1" 200 5678 "-" "Mozilla/5.0 (Windows NT 10.0) Chrome/118.0"
"""

# Сканирование директорий
scan_logs = """10.0.0.70 - - [10/Apr/2026:12:00:00 +0300] "GET /admin HTTP/1.1" 403 123 "-" "Mozilla/5.0 (compatible; Nmap Scripting Engine)"
10.0.0.70 - - [10/Apr/2026:12:00:01 +0300] "GET /administrator HTTP/1.1" 404 234 "-" "Mozilla/5.0 (compatible; Nmap Scripting Engine)"
10.0.0.70 - - [10/Apr/2026:12:00:01 +0300] "GET /wp-admin HTTP/1.1" 404 234 "-" "Mozilla/5.0 (compatible; Nmap Scripting Engine)"
10.0.0.70 - - [10/Apr/2026:12:00:02 +0300] "GET /phpmyadmin HTTP/1.1" 404 234 "-" "Mozilla/5.0 (compatible; Nmap Scripting Engine)"
10.0.0.70 - - [10/Apr/2026:12:00:02 +0300] "GET /.env HTTP/1.1" 404 234 "-" "Mozilla/5.0 (compatible; Nmap Scripting Engine)"
10.0.0.70 - - [10/Apr/2026:12:00:03 +0300] "GET /.git/config HTTP/1.1" 404 234 "-" "Mozilla/5.0 (compatible; Nmap Scripting Engine)"
10.0.0.70 - - [10/Apr/2026:12:00:03 +0300] "GET /backup.sql HTTP/1.1" 404 234 "-" "Mozilla/5.0 (compatible; Nmap Scripting Engine)"
10.0.0.70 - - [10/Apr/2026:12:00:04 +0300] "GET /api/v1/debug HTTP/1.1" 404 234 "-" "Mozilla/5.0 (compatible; Nmap Scripting Engine)"
10.0.0.70 - - [10/Apr/2026:12:00:04 +0300] "GET /test HTTP/1.1" 404 234 "-" "Mozilla/5.0 (compatible; Nmap Scripting Engine)"
10.0.0.70 - - [10/Apr/2026:12:00:05 +0300] "GET /config.php HTTP/1.1" 404 234 "-" "Mozilla/5.0 (compatible; Nmap Scripting Engine)"
10.0.0.70 - - [10/Apr/2026:12:00:05 +0300] "GET /server-status HTTP/1.1" 403 123 "-" "Mozilla/5.0 (compatible; Nmap Scripting Engine)"
10.0.0.70 - - [10/Apr/2026:12:00:06 +0300] "OPTIONS / HTTP/1.1" 200 0 "-" "Mozilla/5.0 (compatible; Nmap Scripting Engine)"
"""

# Brute-force
brute_logs = """10.0.0.80 - - [10/Apr/2026:13:00:00 +0300] "POST /login HTTP/1.1" 401 89 "-" "python-requests/2.31.0"
10.0.0.80 - - [10/Apr/2026:13:00:01 +0300] "POST /login HTTP/1.1" 401 89 "-" "python-requests/2.31.0"
10.0.0.80 - - [10/Apr/2026:13:00:01 +0300] "POST /login HTTP/1.1" 401 89 "-" "python-requests/2.31.0"
10.0.0.80 - - [10/Apr/2026:13:00:02 +0300] "POST /login HTTP/1.1" 401 89 "-" "python-requests/2.31.0"
10.0.0.80 - - [10/Apr/2026:13:00:02 +0300] "POST /login HTTP/1.1" 401 89 "-" "python-requests/2.31.0"
10.0.0.80 - - [10/Apr/2026:13:00:03 +0300] "POST /login HTTP/1.1" 401 89 "-" "python-requests/2.31.0"
10.0.0.80 - - [10/Apr/2026:13:00:03 +0300] "POST /login HTTP/1.1" 401 89 "-" "python-requests/2.31.0"
10.0.0.80 - - [10/Apr/2026:13:00:04 +0300] "POST /login HTTP/1.1" 401 89 "-" "python-requests/2.31.0"
10.0.0.80 - - [10/Apr/2026:13:00:04 +0300] "POST /login HTTP/1.1" 401 89 "-" "python-requests/2.31.0"
10.0.0.80 - - [10/Apr/2026:13:00:05 +0300] "POST /login HTTP/1.1" 200 567 "-" "python-requests/2.31.0"
"""

# Объединяем все логи
all_logs = normal_logs + sqli_logs + xss_logs + scan_logs + brute_logs

print("Логи сгенерированы")
print(f"Общий размер: {len(all_logs)} байт")

# ============================================================
# ЧАСТЬ 2: Парсинг логов
# ============================================================

print("\n" + "=" * 60)
print("ЧАСТЬ 2: ПАРСИНГ ЛОГОВ")
print("=" * 60)

# Регулярное выражение для парсинга Apache/Nginx логов
log_pattern = r'(\S+) - - \[([^\]]+)\] "(\S+) ([^"]*?) HTTP/\d\.\d" (\d+) (\d+) "[^"]*" "([^"]*)"'

def parse_logs(log_text):
    """Парсинг строки логов в DataFrame"""
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
print(f"Распарсено записей: {len(df)}")
print(f"\nПервые 10 строк:")
print(df.head(10))

# ============================================================
# ЧАСТЬ 3: Обнаружение SQL-инъекций
# ============================================================

print("\n" + "=" * 60)
print("ЧАСТЬ 3: ОБНАРУЖЕНИЕ SQL-ИНЪЕКЦИЙ")
print("=" * 60)

# Паттерны SQL-инъекций
sqli_patterns = [
    r"(?i)(union\s+select)",
    r"(?i)(or\s+'?1'?\s*=\s*'?1)",
    r"(?i)(drop\s+table)",
    r"(?i)(and\s+\d+\s*=\s*\d+)",
    r"(?i)(select\s+.*\s+from\s+)",
    r"(?i)(--\s*$)",
    r"['\"]?\s*;\s*(drop|select|insert|update|delete)",
    r"%27",  # URL-encoded '
    r"%3D",  # URL-encoded =
]

def detect_sqli(path):
    """Проверка пути на SQL-инъекцию"""
    decoded = path.replace('%27', "'").replace('%3D', '=').replace('%3C', '<').replace('%3E', '>')
    for pattern in sqli_patterns:
        if re.search(pattern, decoded):
            return True
    return False

df['is_sqli'] = df['path'].apply(detect_sqli)
sqli_attacks = df[df['is_sqli']]

print(f"\nНайдено SQL-инъекций: {len(sqli_attacks)}")
print(f"IP-адреса атакующих: {sqli_attacks['ip'].unique().tolist()}")
print("\nSQLi-запросы:")
for _, row in sqli_attacks.iterrows():
    print(f"  [{row['ip']}] {row['method']} {row['path'][:80]} → {row['status']}")

# ============================================================
# ЧАСТЬ 4: Обнаружение XSS
# ============================================================

print("\n" + "=" * 60)
print("ЧАСТЬ 4: ОБНАРУЖЕНИЕ XSS-АТАК")
print("=" * 60)

xss_patterns = [
    r"(?i)(<script)",
    r"(?i)(<img\s+src\s*=)",
    r"(?i)(onerror\s*=)",
    r"(?i)(onload\s*=)",
    r"(?i)(<svg)",
    r"(?i)(alert\s*\()",
    r"(?i)(javascript\s*:)",
    r"%3Cscript",  # URL-encoded <script
    r"%3Cimg",     # URL-encoded <img
    r"%3Csvg",     # URL-encoded <svg
]

def detect_xss(path):
    """Проверка пути на XSS"""
    for pattern in xss_patterns:
        if re.search(pattern, path, re.IGNORECASE):
            return True
    return False

df['is_xss'] = df['path'].apply(detect_xss)
xss_attacks = df[df['is_xss']]

print(f"\nНайдено XSS-атак: {len(xss_attacks)}")
print(f"IP-адреса атакующих: {xss_attacks['ip'].unique().tolist()}")
print("\nXSS-запросы:")
for _, row in xss_attacks.iterrows():
    print(f"  [{row['ip']}] {row['method']} {row['path'][:80]}")

# ============================================================
# ЧАСТЬ 5: Обнаружение сканирования
# ============================================================

print("\n" + "=" * 60)
print("ЧАСТЬ 5: ОБНАРУЖЕНИЕ СКАНИРОВАНИЯ ДИРЕКТОРИЙ")
print("=" * 60)

# Подозрительные пути
suspicious_paths = [
    r"(?i)(/admin)",
    r"(?i)(/administrator)",
    r"(?i)(/wp-admin)",
    r"(?i)(/phpmyadmin)",
    r"(?i)(/\.env)",
    r"(?i)(/\.git)",
    r"(?i)(/backup)",
    r"(?i)(/debug)",
    r"(?i)(/config)",
    r"(?i)(/server-status)",
    r"(?i)(/test)",
    r"^OPTIONS\s",  # OPTIONS метод
]

# Подозрительные User-Agent
suspicious_ua = [
    r"(?i)(nmap)",
    r"(?i)(nikto)",
    r"(?i)(sqlmap)",
    r"(?i)(dirbuster)",
    r"(?i)(gobuster)",
    r"(?i)(dirsearch)",
    r"(?i)(scanner)",
]

def detect_scan(row):
    """Проверка на сканирование"""
    for pattern in suspicious_paths:
        if re.search(pattern, row['path']):
            return True
    for pattern in suspicious_ua:
        if re.search(pattern, row['user_agent']):
            return True
    return False

df['is_scan'] = df.apply(detect_scan, axis=1)
scan_requests = df[df['is_scan']]

print(f"\nНайдено запросов сканирования: {len(scan_requests)}")
print(f"IP-адреса сканеров: {scan_requests['ip'].unique().tolist()}")
print("\nСканирование:")
for _, row in scan_requests.iterrows():
    print(f"  [{row['ip']}] {row['method']} {row['path']} → {row['status']} ({row['user_agent'][:40]})")

# ============================================================
# ЧАСТЬ 6: Обнаружение brute-force
# ============================================================

print("\n" + "=" * 60)
print("ЧАСТЬ 6: ОБНАРУЖЕНИЕ BRUTE-FORCE")
print("=" * 60)

# Группировка по IP + путь (POST /login)
login_attempts = df[(df['method'] == 'POST') & (df['path'] == '/login')]
brute_check = login_attempts.groupby('ip').agg({
    'status': ['count', lambda x: (x == 401).sum(), lambda x: (x == 200).sum()]
})
brute_check.columns = ['total', 'failed', 'success']
brute_check['fail_rate'] = brute_check['failed'] / brute_check['total']

# Brute-force: много попыток + высокий процент неудач
brute_ips = brute_check[(brute_check['total'] >= 5) & (brute_check['fail_rate'] > 0.8)]

print(f"\nПотенциальный brute-force:")
print(brute_ips)

# Добавить флаг brute в DataFrame
df['is_brute'] = df['ip'].isin(brute_ips.index) & (df['method'] == 'POST') & (df['path'] == '/login')
brute_requests = df[df['is_brute']]

print(f"\nBrute-force запросов: {len(brute_requests)}")
print(f"IP: {brute_requests['ip'].unique().tolist()}")
print(f"User-Agent: {brute_requests['user_agent'].iloc[0] if len(brute_requests) > 0 else 'N/A'}")

# ============================================================
# ЧАСТЬ 7: Сводный отчёт об атаках
# ============================================================

print("\n" + "=" * 60)
print("ЧАСТЬ 7: СВОДНЫЙ ОТЧЁТ")
print("=" * 60)

# Общая классификация
df['attack_type'] = 'normal'
df.loc[df['is_sqli'], 'attack_type'] = 'SQL-инъекция'
df.loc[df['is_xss'], 'attack_type'] = 'XSS'
df.loc[df['is_scan'], 'attack_type'] = 'Сканирование'
df.loc[df['is_brute'], 'attack_type'] = 'Brute-force'

attack_summary = df['attack_type'].value_counts()
print("\nРаспределение запросов:")
print(attack_summary)

# Атакующие IP
attackers = df[df['attack_type'] != 'normal'].groupby(['ip', 'attack_type']).size().unstack(fill_value=0)
print(f"\nАтакующие IP:")
print(attackers)

# Статус-коды атак
print(f"\nСтатус-коды при атаках:")
attack_status = df[df['attack_type'] != 'normal'].groupby(['attack_type', 'status']).size()
print(attack_status)

# ============================================================
# ЧАСТЬ 8: Визуализация
# ============================================================

print("\n" + "=" * 60)
print("ЧАСТЬ 8: ВИЗУАЛИЗАЦИЯ")
print("=" * 60)

fig, axes = plt.subplots(2, 2, figsize=(14, 10))

# 1. Типы атак
attack_counts = df['attack_type'].value_counts()
colors = ['#2ecc71', '#e74c3c', '#f39c12', '#9b59b6', '#3498db']
axes[0, 0].pie(attack_counts.values, labels=attack_counts.index, autopct='%1.1f%%', 
               colors=colors[:len(attack_counts)], startangle=90)
axes[0, 0].set_title('Распределение типов запросов')

# 2. Атаки по IP
if len(attackers) > 0:
    attackers.sum(axis=1).sort_values(ascending=True).plot(kind='barh', ax=axes[0, 1], color='tomato')
    axes[0, 1].set_title('Число атак по IP')
    axes[0, 1].set_xlabel('Количество запросов')
    axes[0, 1].tick_params(axis='y', labelsize=8)

# 3. Статус-коды при атаках
attack_df = df[df['attack_type'] != 'normal']
if len(attack_df) > 0:
    status_by_type = attack_df.groupby(['attack_type', 'status']).size().unstack(fill_value=0)
    status_by_type.plot(kind='bar', stacked=True, ax=axes[1, 0], colormap='viridis')
    axes[1, 0].set_title('Статус-коды по типам атак')
    axes[1, 0].set_ylabel('Количество')
    axes[1, 0].tick_params(axis='x', rotation=45)

# 4. Timeline (по типу User-Agent)
ua_counts = df['user_agent'].value_counts()
top_ua = ua_counts.head(10)
axes[1, 1].barh(range(len(top_ua)), top_ua.values, color='steelblue')
axes[1, 1].set_yticks(range(len(top_ua)))
axes[1, 1].set_yticklabels([ua[:30] + '...' if len(ua) > 30 else ua for ua in top_ua.index], fontsize=7)
axes[1, 1].set_title('Топ User-Agent')
axes[1, 1].set_xlabel('Количество запросов')

plt.tight_layout()
plt.savefig('C:\\it chalenge\\cybersecurity\\log_analysis.png', dpi=150)
print("График сохранён: log_analysis.png")

# ============================================================
# ЧАСТЬ 9: Отчёт для олимпиады
# ============================================================

print("\n" + "=" * 60)
print("ЧАСТЬ 9: ИТОГОВЫЙ ОТЧЁТ")
print("=" * 60)

total_requests = len(df)
attack_requests = len(df[df['attack_type'] != 'normal'])
unique_attackers = df[df['attack_type'] != 'normal']['ip'].nunique()

print(f"""
═══════════════════════════════════════════
       ОТЧЁТ ПО АНАЛИЗУ ЛОГОВ
═══════════════════════════════════════════

📊 ОБЩАЯ СТАТИСТИКА:
  • Всего запросов:       {total_requests}
  • Атакующих запросов:   {attack_requests} ({attack_requests/total_requests:.1%})
  • Уникальных атакующих: {unique_attackers}

🔍 ОБНАРУЖЕННЫЕ АТАКИ:
""")

for attack_type in df['attack_type'].unique():
    if attack_type != 'normal':
        count = (df['attack_type'] == attack_type).sum()
        ips = df[df['attack_type'] == attack_type]['ip'].unique()
        print(f"  • {attack_type}: {count} запросов от {len(ips)} IP")
        for ip in ips:
            print(f"    - {ip}")

print(f"""
🛡️ РЕКОМЕНДАЦИИ:
  1. Заблокировать IP-адреса атакующих
  2. Настроить WAF-правила для SQLi и XSS
  3. Включить rate limiting на /login
  4. Добавить CAPTCHA после N попыток входа
  5. Убрать чувствительные эндпоинты (/.env, /.git)
  6. Настроить логирование и мониторинг

═══════════════════════════════════════════
""")

print("=" * 60)
print("ЗАДАЧА ВЫПОЛНЕНА!")
print("=" * 60)
