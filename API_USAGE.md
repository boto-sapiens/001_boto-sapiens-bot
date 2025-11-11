# 🔗 Symfony API Usage Guide

## 📋 Конфигурация API

### ✅ Правильное значение SYMFONY_API_URL

```bash
# В .env файле
symfony_api_url=http://127.0.0.1:8000/api/telegram
```

**Формат**: `http://host:port/api/telegram`

### ❌ Неправильные значения

```bash
# НЕПРАВИЛЬНО - заканчивается на /user
symfony_api_url=http://127.0.0.1:8000/api/telegram/user

# НЕПРАВИЛЬНО - заканчивается на /bot  
symfony_api_url=http://127.0.0.1:8000/api/telegram/bot

# НЕПРАВИЛЬНО - без /api/telegram
symfony_api_url=http://127.0.0.1:8000

# НЕПРАВИЛЬНО - с лишними слешами
symfony_api_url=http://127.0.0.1:8000/api/telegram///
```

## 🔍 Проверка API подключения

### 1. Через curl (внешняя проверка)

```bash
# Проверка health endpoint
curl -X GET "http://127.0.0.1:8000/api/telegram/health" \
  -H "Accept: application/json"

# Проверка user endpoint (должен вернуть JSON, даже если 404)
curl -X GET "http://127.0.0.1:8000/api/telegram/user/12345" \
  -H "Accept: application/json"

# Проверка POST user
curl -X POST "http://127.0.0.1:8000/api/telegram/user" \
  -H "Content-Type: application/json" \
  -H "Accept: application/json" \
  -d '{"telegram_id": "12345", "username": "test_user"}'
```

### 2. Через Docker контейнер

```bash
# Войти в контейнер
docker exec -it boto-chronicler bash

# Запустить тест API
python3 -c "
import asyncio
from services.symfony_api import test_symfony_api
asyncio.run(test_symfony_api())
"
```

### 3. Через Python скрипт

```bash
# Запустить тест из корня проекта
python3 services/symfony_api.py
```

## 🚨 Диагностика проблем

### Проблема: 404 ошибки

**Причина**: Неправильный base_url
**Решение**: Проверить SYMFONY_API_URL в .env

```bash
# Проверить текущее значение
docker exec boto-chronicler env | grep SYMFONY_API_URL

# Исправить в .env
echo "symfony_api_url=http://127.0.0.1:8000/api/telegram" >> .env
```

### Проблема: HTML вместо JSON

**Причина**: API не настроен или недоступен
**Решение**: Проверить доступность Symfony API

```bash
# Проверить доступность
curl -I http://127.0.0.1:8000/api/telegram/health

# Должен вернуть:
# HTTP/1.1 200 OK
# Content-Type: application/json
```

### Проблема: Connection refused

**Причина**: Symfony API не запущен
**Решение**: Запустить Symfony API сервер

```bash
# Если Symfony API на том же хосте
cd /path/to/symfony/project
php bin/console server:start

# Или через Docker
docker run -d -p 8000:8000 your-symfony-api
```

## 📊 Мониторинг API

### Логи бота

```bash
# Просмотр логов с фильтром по API
docker logs boto-chronicler | grep "Symfony API"

# Просмотр всех логов
docker logs -f boto-chronicler
```

### Проверка статуса

```bash
# Статус контейнера
docker compose ps

# Проверка переменных окружения
docker exec boto-chronicler env | grep -E "(SYMFONY|API)"
```

## 🔧 Endpoints API

### User Endpoints

| Method | Endpoint | Description |
|--------|----------|-------------|
| GET | `/api/telegram/user/{telegram_id}` | Получить пользователя |
| POST | `/api/telegram/user` | Создать/обновить пользователя |
| PUT | `/api/telegram/user/{telegram_id}` | Обновить профиль |
| GET | `/api/telegram/user/{telegram_id}/bots` | Получить ботов пользователя |

### Bot Endpoints

| Method | Endpoint | Description |
|--------|----------|-------------|
| POST | `/api/telegram/bot` | Добавить бота |
| DELETE | `/api/telegram/bot/{bot_id}` | Удалить бота |

### Health Endpoint

| Method | Endpoint | Description |
|--------|----------|-------------|
| GET | `/api/telegram/health` | Проверка доступности API |

## 🛠 Troubleshooting

### 1. Проверка URL в логах

При запуске бота вы должны увидеть:
```
🔗 Symfony API base_url: http://127.0.0.1:8000/api/telegram
✅ Symfony API base_url format is correct: http://127.0.0.1:8000/api/telegram
```

### 2. Предупреждения о неправильном URL

Если URL неправильный, вы увидите:
```
⚠️  Symfony API base_url ends with '/user' - this may cause issues!
   Expected format: http://host:port/api/telegram
   Current URL: http://127.0.0.1:8000/api/telegram/user
   Please check your SYMFONY_API_URL in .env file
```

### 3. Тестирование подключения

```bash
# Быстрый тест
docker exec boto-chronicler python3 -c "
import asyncio
from services.symfony_api import SymfonyAPI

async def quick_test():
    api = SymfonyAPI('http://127.0.0.1:8000/api/telegram')
    result = await api.test_api_connection()
    print(f'Connection test: {result}')
    await api.close()

asyncio.run(quick_test())
"
```

## 📝 Примеры использования

### Создание пользователя

```python
from services.symfony_api import SymfonyAPI

api = SymfonyAPI("http://127.0.0.1:8000/api/telegram")
result = await api.upsert_user("12345", "username")
print(result)
```

### Добавление бота

```python
result = await api.add_bot("12345", "@mybot", "My bot description")
print(result)
```

### Проверка подключения

```python
# Детальная проверка
connection_test = await api.test_api_connection()
print(f"API Status: {connection_test['status']}")
print(f"Returns JSON: {connection_test['is_json']}")
```
