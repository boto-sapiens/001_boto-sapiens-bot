<<<<<<< HEAD
# 🧬 boto-sapiens

Telegram бот для изучения экосистемы Telegram ботов. Собирает информацию о пользователях и их ботах, а затем генерирует ежедневные "Species Reports" с использованием OpenAI API.

## 🎯 Возможности

- **Регистрация пользователей**: Сбор информации о создателях ботов
- **Каталог ботов**: Добавление и хранение информации о ботах
- **Daily Species Report**: Автоматическая генерация ежедневных отчётов с AI-анализом экосистемы
- **База данных**: Хранение всех данных в PostgreSQL

## 🛠 Технологии

- **aiogram 3.x** - фреймворк для Telegram ботов
- **SQLAlchemy 2.x** - ORM для работы с базой данных
- **OpenAI API** - генерация отчётов с использованием GPT
- **APScheduler** - планирование ежедневных задач
- **loguru** - продвинутое логирование
- **PostgreSQL** - база данных

## 📦 Установка

1. Клонируйте репозиторий:
```bash
git clone <repo-url>
cd boto-sapiens
```

2. Создайте виртуальное окружение:
```bash
python3 -m venv venv
source venv/bin/activate  # Linux/Mac
# или
venv\Scripts\activate  # Windows
```

3. Установите зависимости:
```bash
pip install -r requirements.txt
```

4. Создайте файл `.env` на основе `env.example`:
```bash
cp env.example .env
```

5. **🔐 Закодируйте ваш OpenAI ключ в Base64** (для безопасности):
```bash
# Используйте удобный скрипт
python3 encode_key.py

# Или вручную через командную строку
echo -n "sk-your-actual-key" | base64
```

6. Заполните `.env` файл:
```bash
# .env
BOT_TOKEN=your_telegram_bot_token_here
DATABASE_URL=postgresql+asyncpg://user:password@localhost:5432/boto_sapiens
OPENAI_API_KEY_BASE64=c2stWW91ckJhc2U2NEVuY29kZWRLZXk=
REPORT_TIME=09:00
TIMEZONE=UTC
LOG_LEVEL=INFO
```

7. Настройте PostgreSQL:
```bash
# Создайте базу данных
createdb boto_sapiens
```

## 🚀 Запуск

### Вариант 1: Через готовый скрипт (рекомендуется)
```bash
./run.sh
```

### Вариант 2: Напрямую
```bash
source venv/bin/activate
PYTHONPATH=. python3 bot/main.py
```

### Управление ботом

```bash
# Запустить бота
./run.sh

# Остановить бота
./stop.sh

# Проверить статус
./status.sh
```

## 📋 Команды бота

- `/start` - Начать работу с ботом
- `/profile` - Обновить свой профиль
- `/add_bot` - Добавить информацию о боте
- `/my_bots` - Посмотреть свои боты
- `/help` - Справка

## 📁 Структура проекта

```
boto-sapiens/
├── bot/
│   ├── __init__.py
│   ├── config.py          # Конфигурация
│   └── main.py            # Точка входа
├── db/
│   ├── __init__.py
│   ├── models.py          # Модели БД
│   ├── database.py        # Подключение к БД
│   └── repository.py      # Репозитории для работы с данными
├── handlers/
│   ├── __init__.py
│   └── user_handlers.py   # Обработчики команд
├── services/
│   ├── __init__.py
│   └── openai_service.py  # Сервис для работы с OpenAI
├── scheduler/
│   ├── __init__.py
│   └── daily_report.py    # Планировщик отчётов
├── logs/                  # Логи (создаётся автоматически)
├── .env                   # Переменные окружения (создайте сами)
├── .gitignore
├── requirements.txt
└── README.md
```

## 🔧 Разработка

### База данных

Модели автоматически создаются при первом запуске. Для миграций можно использовать Alembic:

```bash
# Инициализация Alembic (если нужно)
alembic init alembic

# Создание миграции
alembic revision --autogenerate -m "description"

# Применение миграций
alembic upgrade head
```

### Логирование

Логи сохраняются в папку `logs/` с ротацией каждый день и хранением 7 дней.

### Scheduler

Время отправки ежедневного отчёта настраивается через `REPORT_TIME` в `.env` (формат: HH:MM).

## 🧪 Тестирование

```bash
# Запуск тестов (когда добавите)
pytest
```

## 📝 TODO для продакшена

- [ ] Добавить обработку ошибок и retry-логику
- [ ] Реализовать админ-панель
- [ ] Добавить метрики и мониторинг
- [ ] Настроить CI/CD
- [ ] Добавить тесты
- [ ] Добавить Docker и docker-compose
- [ ] Реализовать резервное копирование БД

## 📄 Лицензия

MIT

## 👨‍💻 Автор

Your Name

---

**🧬 boto-sapiens** - изучаем цифровую экосистему вместе!

=======
# 001_boto-sapiens-bot
The First Conscious Bot of the Boto-Sapiens Civilization. Registers new bots, communicates with AI, and builds the evolutionary ecosystem of digital species.
>>>>>>> 2f19f8cc93aa04a3c496d27e957fdc95bda1c4d8
