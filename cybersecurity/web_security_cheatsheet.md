# 🔒 ШПАРГАЛКА: Информационная безопасность

## 📋 ОБЗОР ИНСТРУМЕНТОВ НА ОЛИМПИАДЕ

| Инструмент | Для чего | Пример команды |
|------------|----------|----------------|
| **DevTools** | Анализ запросов браузера | F12 → Network |
| **Burp Suite** | Перехват и модификация HTTP | Proxy → Intercept |
| **ZAP (OWASP)** | Сканер уязвимостей | Automated Scan |
| **ffuf** | Сканер директорий | `ffuf -u URL -w wordlist` |
| **dirsearch** | Сканер директорий | `dirsearch -u URL` |
| **gobuster** | Сканер директорий/DNS | `gobuster dir -u URL -w wordlist` |

---

## 🌐 ЧАСТЬ 1: DevTools браузера

### Как открыть:
- **F12** или **Ctrl+Shift+I**
- Правый клик → "Исследовать элемент"

### Вкладки:

#### 1. Elements (Элементы)
- Просмотр и редактирование HTML/CSS
- Поиск скрытых полей форм
- Просмотр JavaScript-обработчиков событий

#### 2. Console (Консоль)
- Выполнение JavaScript
- Просмотр ошибок и логов
- `document.cookie` — посмотреть куки
- `localStorage` — локальное хранилище

#### 3. Network (Сеть) — САМАЯ ВАЖНАЯ!
- Все HTTP-запросы страницы
- Методы: GET, POST, PUT, DELETE
- Заголовки запросов и ответов
- Коды ответа: 200, 301, 403, 404, 500
- Cookies, Headers, Payload

**Что искать:**
```
✅ API-эндпоинты (в XHR/Fetch фильтрах)
✅ Токены авторизации в заголовках
✅ Передача чувствительных данных в URL
✅ Разные HTTP методы
✅ Cookies (HttpOnly, Secure флаги)
✅ Ответы сервера (в т.ч. ошибки)
```

#### 4. Application (Приложение)
- Cookies
- Local Storage
- Session Storage
- IndexedDB

#### 5. Sources (Источники)
- Просмотр JavaScript-файлов
- Точки останова (breakpoints)
- Поиск по скриптам (Ctrl+Shift+F)

---

## 📡 ЧАСТЬ 2: HTTP-протокол

### Структура HTTP-запроса:
```
GET /api/users HTTP/1.1
Host: example.com
Authorization: Bearer <token>
Content-Type: application/json
Cookie: session_id=abc123
```

### Структура HTTP-ответа:
```
HTTP/1.1 200 OK
Content-Type: application/json
Set-Cookie: session=xyz; HttpOnly; Secure

{"status": "success", "data": {...}}
```

### Коды ответов:
| Код | Значение | Описание |
|-----|----------|----------|
| 200 | OK | Успех |
| 201 | Created | Создано |
| 301 | Moved Permanently | Редирект |
| 302 | Found | Временный редирект |
| 400 | Bad Request | Некорректный запрос |
| 401 | Unauthorized | Не авторизован |
| 403 | Forbidden | Доступ запрещён |
| 404 | Not Found | Не найдено |
| 405 | Method Not Allowed | Метод не разрешён |
| 500 | Internal Server Error | Ошибка сервера |

### HTTP-методы:
| Метод | Описание | Безопасен? | Идемпотентен? |
|-------|----------|------------|---------------|
| GET | Получение данных | ✅ | ✅ |
| POST | Создание данных | ❌ | ❌ |
| PUT | Обновление (полное) | ❌ | ✅ |
| PATCH | Обновление (частичное) | ❌ | ❌ |
| DELETE | Удаление | ❌ | ✅ |
| OPTIONS | Доступные методы | ✅ | ✅ |
| HEAD | Как GET, но без тела | ✅ | ✅ |

---

## 🔍 ЧАСТЬ 3: Сканеры директорий

### ffuf

```bash
# Базовое сканирование
ffuf -u http://target.com/FUZZ -w wordlist.txt

# С фильтром по коду ответа
ffuf -u http://target.com/FUZZ -w wordlist.txt -mc 200,301,302

# Исключить ответы определённого размера
ffuf -u http://target.com/FUZZ -w wordlist.txt -fs 0

# С заголовком авторизации
ffuf -u http://target.com/FUZZ -w wordlist.txt -H "Authorization: Bearer TOKEN"

# С рекурсивным поиском
ffuf -u http://target.com/FUZZ -w wordlist.txt -recursion

# С задержкой (чтобы не спамить)
ffuf -u http://target.com/FUZZ -w wordlist.txt -rate 10

# POST-запрос
ffuf -u http://target.com/FUZZ -w wordlist.txt -X POST -d "param=value"

# Сохранить результат
ffuf -u http://target.com/FUZZ -w wordlist.txt -o output.json -of json
```

### dirsearch

```bash
# Базовое сканирование
python3 dirsearch.py -u http://target.com

# С расширенными фильтрами
python3 dirsearch.py -u http://target.com -e php,html,js,json

# С конкретным wordlist
python3 dirsearch.py -u http://target.com -w /path/to/wordlist.txt

# С рекурсией
python3 dirsearch.py -u http://target.com -r

# Рекурсивная глубина
python3 dirsearch.py -u http://target.com -R 3

# С заголовками
python3 dirsearch.py -u http://target.com -H "Authorization: Bearer TOKEN"

# Исключить коды
python3 dirsearch.py -u http://target.com --exclude-status=403,404
```

### gobuster

```bash
# Сканирование директорий
gobuster dir -u http://target.com -w wordlist.txt

# С расширениями
gobuster dir -u http://target.com -w wordlist.txt -x php,html,txt

# С рекурсией
gobuster dir -u http://target.com -w wordlist.txt -r

# DNS-сканирование
gobuster dns -d target.com -w wordlist.txt

# С параметрами
gobuster dir -u http://target.com -w wordlist.txt -t 20 -s "200,204,301,302"
```

### Популярные wordlist-ы:
```
/usr/share/seclists/Discovery/Web-Content/common.txt
/usr/share/seclists/Discovery/Web-Content/big.txt
/usr/share/wordlists/dirb/common.txt
/usr/share/wordlists/dirbuster/directory-list-2.3-medium.txt
```

---

## 🛡️ ЧАСТЬ 4: Распространённые уязвимости

### 1. SQL-инъекция (SQLi)

**Что:** Внедрение SQL-кода через входные данные

**Где искать:**
- Формы входа (логин/пароль)
- Параметры URL (`?id=1`)
- Поля поиска

**Примеры:**
```sql
-- Проверка на уязвимость
' OR '1'='1
' OR 1=1 --
admin' --

-- Извлечение данных
' UNION SELECT username, password FROM users --
' UNION SELECT table_name, NULL FROM information_schema.tables --

-- Определение числа колонок
' ORDER BY 1 --
' ORDER BY 2 --
' ORDER BY 3 --  ← ошибка здесь
```

**Blind SQLi (без вывода на экран):**
```sql
-- Определение длины пароля
' AND LENGTH(password) > 5 --

-- Проверка первого символа
' AND SUBSTRING(password, 1, 1) = 'a' --
```

### 2. XSS (Cross-Site Scripting)

**Что:** Внедрение JavaScript-кода на страницу

**Где искать:**
- Поля ввода (комментарии, поиск)
- Параметры URL, которые выводятся на страницу
- Профили пользователей

**Примеры:**
```html
<!-- Базовый -->
<script>alert('XSS')</script>

<!-- Обход фильтра -->
<img src=x onerror=alert('XSS')>
<svg onload=alert('XSS')>
<body onload=alert('XSS')>

<!-- Без тегов (в атрибутах) -->
" onmouseover="alert('XSS')
' onclick='alert(1)'

<!-- URL-encoded -->
%3Cscript%3Ealert('XSS')%3C/script%3E
```

**Типы XSS:**
- **Reflected**: Вредоносный код приходит в запросе и сразу отражается
- **Stored**: Сохраняется в БД и показывается всем
- **DOM-based**: Обрабатывается только на клиенте (JS)

### 3. IDOR (Insecure Direct Object Reference)

**Что:** Доступ к чужим данным через изменение идентификатора

**Где искать:**
```
/api/users/123/profile → /api/users/124/profile
/api/orders/456 → /api/orders/457
/documents?id=789 → documents?id=790
```

**Как проверить:**
1. Зайти под своим аккаунтом
2. Найти запрос с ID в DevTools/Proxy
3. Изменить ID на другой
4. Если получил чужие данные → уязвимость

### 4. Broken Authentication

**Что:** Проблемы с авторизацией

**Что проверять:**
```
✅ Слабые пароли (admin/admin, test/test)
✅ Нет блокировки после N попыток
✅ JWT токены без подписи
✅ Предсказуемые session ID
✅ Утечка токенов в URL
✅ Отсутствие logout на сервере
```

### 5. Security Misconfiguration

**Что:** Неправильная настройка безопасности

**Что проверять:**
```
✅ /admin без пароля
✅ /api/debug или /api/test доступные
✅ HTTP вместо HTTPS
✅ Открытые файлы .env, .git, .htaccess
✅ Серверные ошибки со стеком (500)
✅ Методы PUT, DELETE на ресурсах
```

---

## 🔧 ЧАСТЬ 5: Burp Suite (основы)

### Настройка:
1. Запустить Burp Suite
2. Proxy → Intercept → Включить
3. Настроить браузер на прокси 127.0.0.1:8080
4. Или использовать встроенный браузер Burp

### Основные вкладки:

#### Proxy → Intercept
- Перехватывает запросы/ответы
- Можно модифицировать на лету
- Forward — отправить, Drop — отбросить

#### Proxy → HTTP history
- История всех запросов
- Фильтры по домену, методу, статусу
- Правый клик → Send to Repeater/Intruder

#### Repeater
- Повторная отправка запросов
- Модификация параметров
- Удобно для ручного тестирования

#### Intruder
- Автоматизация перебора
- Атаки:
  - **Sniper**: Один payload, одна позиция
  - **Battering ram**: Один payload, все позиции
  - **Pitchfork**: Разные payloads, по очереди
  - **Cluster bomb**: Все комбинации (декартово произведение)

### Пример Intruder (подбор пароля):
```
1. Перехватить запрос логина в Proxy
2. Send to Intruder
3. Выбрать позицию: "password":§admin§
4. Загрузить список паролей в Payloads
5. Start Attack
6. Смотреть на длину ответа (разница = успех)
```

---

## 📝 ЧАСТЬ 6: Статический анализ JavaScript

### Что искать в JS-файлах:

#### 1. API-эндпоинты
```javascript
// Искать:
fetch('/api/')
axios.get('/api/')
$.ajax({url: '/api/'})
XMLHttpRequest

// Могут быть скрытые эндпоинты:
fetch('/api/admin/users')  // ← админский эндпоинт
```

#### 2. Хардкоженные секреты
```javascript
// Искать:
apiKey = "AIzaSy..."
secret = "sk-..."
password = "..."
token = "..."
Authorization: "Bearer ..."
```

#### 3. Логика авторизации на клиенте
```javascript
// Плохо: проверка на клиенте
if (user.role === 'admin') {
    showAdminPanel()  // ← можно обойти
}

// Хорошо: проверка на сервере
```

#### 4. Параметры и конфигурация
```javascript
// Может содержать:
const API_URL = 'http://api.internal:8080'
const DEBUG = true
const FEATURE_FLAGS = { beta: true }
```

### Инструменты:
- **DevTools → Sources** — просмотр скриптов
- **Ctrl+Shift+F** — поиск по всем скриптам
- **LinkFinder** (pip install linkfinder):
  ```bash
  python3 linkfinder.py -i script.js -o cli
  ```
- **SecretFinder**:
  ```bash
  python3 SecretFinder.py -i script.js
  ```

---

## 🎯 ЧАСТЬ 7: Типичный workflow на олимпиаде

### Шаг 1: Разведка
```
1. Открыть сайт в браузере
2. DevTools → Network — посмотреть запросы
3. robots.txt, sitemap.xml
4. ffuf/dirsearch — найти скрытые директории
```

### Шаг 2: Анализ
```
1. Изучить JS-файлы на наличие эндпоинтов
2. Проверить API-эндпоинты через Repeater
3. Попробовать разные HTTP-методы (OPTIONS)
```

### Шаг 3: Поиск уязвимостей
```
1. Формы → SQLi, XSS
2. Параметры с ID → IDOR
3. Авторизация → Broken Auth
4. Админ-панели → Misconfiguration
```

### Шаг 4: Эксплуатация
```
1. Документировать каждую найденную уязвимость
2. Скриншоты доказательств
3. Описание: что, где, как, риск
```

---

## ⚠️ ЧАСТЬ 8: Чек-лист проверки

### Web-приложение:
```
□ Все формы на SQLi (логин, поиск, комментарии)
□ Все параметры URL на XSS
□ Все ID-параметры на IDOR
□ JWT-токены (проверить на jwt.io)
□ Cookies (HttpOnly, Secure?)
□ HTTP-методы (OPTIONS)
□ Ошибки сервера (500)
□ Файлы: .env, .git, .htaccess, backup.sql
□ Админ-панели: /admin, /login, /dashboard
□ API-эндпоинты из JS
```

### API:
```
□ Аутентификация (токены, API keys)
□ Авторизация (доступ к чужим ресурсам)
□ Валидация входных данных
□ Rate limiting
□ HTTP-методы (PUT, DELETE там где не надо)
□ Пагинация (утечка данных через meta)
□ Ошибки (стек трейсы в 500)
```

---

## 📚 Полезные ресурсы

- **OWASP Top 10**: https://owasp.org/www-project-top-ten/
- **PortSwigger Academy**: https://portswigger.net/web-security
- **HackTheBox**: https://www.hackthebox.com/
- **TryHackMe**: https://tryhackme.com/
- **PentesterLab**: https://pentesterlab.com/

---

**⚡ Помни: тестируй ТОЛЬКО то, на что есть разрешение!**
