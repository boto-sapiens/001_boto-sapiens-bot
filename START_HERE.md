# 🚀 Быстрый старт boto-sapiens

## ⚡ Запуск за 3 шага

### 1️⃣ Установка
```bash
./setup.sh
```

### 2️⃣ Настройка
```bash
# Закодируйте ваш OpenAI ключ
python3 encode_key.py

# Отредактируйте .env (добавьте токены)
nano .env
```

### 3️⃣ Запуск
```bash
./run.sh
```

---

## 📋 Управление ботом

```bash
# Запустить бота
./run.sh

# Остановить бота
./stop.sh

# Проверить статус
./status.sh

# Протестировать конфигурацию
python3 test_config.py

# Закодировать OpenAI ключ
python3 encode_key.py
```

---

## 📝 Что нужно для запуска?

### Обязательно:

1. **Telegram Bot Token**
   - Получите у [@BotFather](https://t.me/BotFather)
   - Команда: `/newbot`

2. **OpenAI API Key**
   - Получите на [platform.openai.com](https://platform.openai.com)
   - Закодируйте в Base64: `python3 encode_key.py`

3. **PostgreSQL Database**
   - Docker: `docker run -d --name boto-postgres -e POSTGRES_DB=boto_sapiens -e POSTGRES_USER=boto -e POSTGRES_PASSWORD=mypass -p 5432:5432 postgres:15-alpine`
   - Или локально: `sudo apt install postgresql && createdb boto_sapiens`

### Опционально:

- Настройка времени отчётов (`REPORT_TIME` в .env)
- Настройка timezone (`TIMEZONE` в .env)
- Уровень логирования (`LOG_LEVEL` в .env)

---

## ✅ Проверка работы

После запуска `./run.sh` вы должны увидеть:

```
🧬 Starting boto-sapiens...
✅ OpenAI API key successfully decoded from Base64
✅ Database initialized successfully
✅ Scheduler started
✅ Bot startup completed successfully
📡 Starting polling...
```

Проверьте в Telegram:
1. Найдите вашего бота
2. Отправьте `/start`
3. Следуйте инструкциям

---

## 🐛 Что-то не работает?

### Быстрая диагностика:
```bash
# Проверьте конфигурацию
python3 test_config.py

# Проверьте статус
./status.sh

# Посмотрите логи
tail -f logs/bot.log
```

### Частые проблемы:

**"No module named 'bot'"**
→ Используйте `./run.sh` вместо прямого запуска

**"Invalid Base64 encoding"**
→ Перекодируйте ключ: `python3 encode_key.py`

**"Connection refused" (PostgreSQL)**
→ Проверьте, что PostgreSQL запущен и `DATABASE_URL` правильный

**"Invalid bot token"**
→ Проверьте `BOT_TOKEN` в .env

---

## 📚 Документация

- 📖 [README.md](README.md) - Полная документация
- 🚀 [QUICKSTART.md](QUICKSTART.md) - Детальное руководство
- 🛠️ [SCRIPTS.md](SCRIPTS.md) - Описание всех скриптов
- 🏗️ [ARCHITECTURE.md](ARCHITECTURE.md) - Архитектура проекта
- 🔄 [MIGRATION_BASE64.md](MIGRATION_BASE64.md) - Миграция на Base64

---

## 💡 Полезные команды

```bash
# Посмотреть логи в реальном времени
tail -f logs/bot.log

# Найти процесс бота
ps aux | grep "python3 bot/main.py"

# Перезапустить бота
./stop.sh && ./run.sh

# Обновить зависимости
source venv/bin/activate && pip install -r requirements.txt --upgrade

# Проверить версии
pip list | grep -E "aiogram|openai|sqlalchemy"
```

---

## 🎯 Что дальше?

1. Добавьте информацию о себе: `/profile`
2. Добавьте ботов: `/add_bot`
3. Дождитесь ежедневного отчёта (настроено на 09:00 UTC)
4. Изучите [ARCHITECTURE.md](ARCHITECTURE.md) для кастомизации

---

**🧬 boto-sapiens готов к работе!**

Если нужна помощь - смотрите полную документацию в [README.md](README.md)

