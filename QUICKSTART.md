# 🚀 Быстрый старт boto-sapiens

## Шаг 1: Получите необходимые токены

### Telegram Bot Token
1. Откройте [@BotFather](https://t.me/BotFather) в Telegram
2. Отправьте `/newbot`
3. Следуйте инструкциям и сохраните токен

### OpenAI API Key
1. Зарегистрируйтесь на [platform.openai.com](https://platform.openai.com)
2. Перейдите в API Keys
3. Создайте новый ключ и сохраните его

## Шаг 2: Настройте PostgreSQL

### Локальная установка (Ubuntu/Debian)
```bash
sudo apt update
sudo apt install postgresql postgresql-contrib
sudo systemctl start postgresql
sudo -u postgres createdb boto_sapiens
sudo -u postgres psql -c "CREATE USER youruser WITH PASSWORD 'yourpassword';"
sudo -u postgres psql -c "GRANT ALL PRIVILEGES ON DATABASE boto_sapiens TO youruser;"
```

### Docker (рекомендуется)
```bash
docker run -d \
  --name boto-postgres \
  -e POSTGRES_DB=boto_sapiens \
  -e POSTGRES_USER=boto \
  -e POSTGRES_PASSWORD=yourpassword \
  -p 5432:5432 \
  postgres:15-alpine
```

## Шаг 3: Установите проект

### Автоматическая установка (рекомендуется)
```bash
./setup.sh
```

### Ручная установка
```bash
# Создать виртуальное окружение
python3 -m venv venv
source venv/bin/activate

# Установить зависимости
pip install -r requirements.txt

# Создать .env файл
cp env.example .env

# Создать папку для логов
mkdir -p logs
```

## Шаг 4: Настройте .env

### 🔐 Важно: Кодирование OpenAI ключа в Base64

Для безопасности, OpenAI API ключ хранится в Base64-кодировке. Закодируйте ваш ключ:

```bash
# Linux/Mac
echo -n "sk-your-actual-openai-key" | base64

# Пример вывода:
# c2stWW91cmFjdHVhbG9wZW5haWtleQ==
```

Или используйте Python:
```bash
python3 -c "import base64; print(base64.b64encode(b'sk-your-actual-openai-key').decode())"
```

Отредактируйте файл `.env`:

```env
BOT_TOKEN=1234567890:ABCdefGHIjklMNOpqrsTUVwxyz
DATABASE_URL=postgresql+asyncpg://boto:yourpassword@localhost:5432/boto_sapiens
OPENAI_API_KEY_BASE64=c2stWW91cmFjdHVhbG9wZW5haWtleQ==
REPORT_TIME=09:00
TIMEZONE=UTC
LOG_LEVEL=INFO
```

## Шаг 5: Запустите бота

```bash
source venv/bin/activate  # если ещё не активировано
python bot/main.py
```

Вы должны увидеть:
```
2024-01-01 12:00:00 | INFO     | Initializing database...
2024-01-01 12:00:00 | SUCCESS  | Database initialized successfully
2024-01-01 12:00:00 | INFO     | Scheduler configured: Daily report at 09:00 UTC
2024-01-01 12:00:00 | SUCCESS  | Bot startup completed successfully
2024-01-01 12:00:00 | INFO     | Starting polling...
```

## Шаг 6: Протестируйте бота

1. Откройте вашего бота в Telegram
2. Отправьте `/start`
3. Следуйте инструкциям для заполнения профиля
4. Добавьте информацию о своих ботах

## 🐛 Решение проблем

### Ошибка подключения к БД
- Проверьте, что PostgreSQL запущен: `sudo systemctl status postgresql`
- Проверьте правильность DATABASE_URL в .env
- Убедитесь, что база данных создана

### Ошибка OpenAI API
- Проверьте правильность API ключа
- Убедитесь, что у вас есть кредиты на аккаунте OpenAI
- Проверьте интернет-соединение

### Ошибка Telegram Bot Token
- Убедитесь, что токен правильный
- Проверьте, что бот не запущен в другом месте
- Убедитесь, что токен не содержит пробелов

## 📊 Мониторинг

### Логи
Все логи сохраняются в `logs/bot.log` с ротацией каждый день.

```bash
# Смотреть последние логи
tail -f logs/bot.log

# Поиск ошибок
grep ERROR logs/bot.log
```

### База данных
```bash
# Подключиться к БД
psql -U boto -d boto_sapiens

# Посмотреть пользователей
SELECT * FROM users;

# Посмотреть ботов
SELECT * FROM bot_info;
```

## 🔄 Обновление

```bash
git pull
source venv/bin/activate
pip install -r requirements.txt --upgrade
```

## 🎯 Следующие шаги

- Настройте время отправки отчётов в `.env` (REPORT_TIME)
- Добавьте webhook вместо polling для продакшена
- Настройте Docker для деплоя
- Добавьте мониторинг (Prometheus/Grafana)

---

Если возникли проблемы - смотрите README.md для подробной информации.

