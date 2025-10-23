# 🏗 Архитектура boto-sapiens

## 📂 Структура проекта

```
boto-sapiens/
├── bot/                    # Основной модуль бота
│   ├── __init__.py
│   ├── config.py          # Конфигурация (Pydantic Settings)
│   └── main.py            # Точка входа, инициализация бота
│
├── db/                     # Слой работы с базой данных
│   ├── __init__.py
│   ├── models.py          # SQLAlchemy модели (User, BotInfo)
│   ├── database.py        # Подключение к БД, сессии
│   └── repository.py      # Репозитории для CRUD операций
│
├── handlers/               # Обработчики Telegram команд
│   ├── __init__.py
│   └── user_handlers.py   # Handlers для пользователей
│
├── services/               # Бизнес-логика и внешние сервисы
│   ├── __init__.py
│   └── openai_service.py  # Интеграция с OpenAI API
│
├── scheduler/              # Планировщик задач
│   ├── __init__.py
│   └── daily_report.py    # Ежедневные отчёты (APScheduler)
│
├── logs/                   # Логи приложения
│
├── .env                    # Переменные окружения (не в git)
├── env.example             # Пример .env файла
├── .gitignore             # Git ignore
├── .dockerignore          # Docker ignore
│
├── requirements.txt        # Python зависимости
├── Dockerfile             # Docker образ
├── docker-compose.yml     # Docker Compose конфигурация
├── setup.sh               # Скрипт быстрой установки
│
├── README.md              # Основная документация
├── QUICKSTART.md          # Быстрый старт
└── ARCHITECTURE.md        # Этот файл
```

## 🔄 Поток данных

### 1. Регистрация пользователя
```
User -> /start -> handlers/user_handlers.py
                  -> db/repository.py (UserRepository.create)
                  -> db/models.py (User)
                  -> PostgreSQL
```

### 2. Добавление бота
```
User -> /add_bot -> handlers/user_handlers.py
                    -> FSM (BotRegistrationStates)
                    -> db/repository.py (BotRepository.create)
                    -> db/models.py (BotInfo)
                    -> PostgreSQL
```

### 3. Ежедневный отчёт
```
scheduler/daily_report.py (cron trigger)
-> db/repository.py (UserRepository.get_all_users)
-> services/openai_service.py (generate_species_report)
-> OpenAI API (GPT-4)
-> handlers (broadcast to all users)
```

## 🗄 Модель данных

### User
```python
- id: BigInteger (PK)
- telegram_id: BigInteger (unique, indexed)
- username: String(255)
- full_name: String(255)
- bio: Text
- interests: Text
- created_at: DateTime
- updated_at: DateTime
- bots: Relationship[BotInfo]
```

### BotInfo
```python
- id: BigInteger (PK)
- owner_id: BigInteger (FK -> User.telegram_id)
- bot_name: String(255)
- bot_username: String(255)
- bot_description: Text
- bot_purpose: Text
- created_at: DateTime
- updated_at: DateTime
- owner: Relationship[User]
```

## 🔌 Основные компоненты

### 1. Bot Core (`bot/main.py`)
- Инициализация aiogram Bot и Dispatcher
- Регистрация handlers
- Управление жизненным циклом (startup/shutdown)
- Настройка логирования (loguru)

### 2. Configuration (`bot/config.py`)
- Pydantic Settings для типобезопасной конфигурации
- Загрузка переменных из .env
- Валидация конфигурации при старте

### 3. Database Layer (`db/`)
- **models.py**: Определение моделей SQLAlchemy 2.0
- **database.py**: Async engine, session factory
- **repository.py**: Repository pattern для изоляции бизнес-логики от БД

### 4. Handlers (`handlers/`)
- Router-based архитектура aiogram 3.x
- FSM для multi-step диалогов
- Разделение по доменам (user_handlers, admin_handlers, etc.)

### 5. Services (`services/`)
- Внешние интеграции (OpenAI)
- Бизнес-логика, не связанная с handlers
- Изолированные, тестируемые компоненты

### 6. Scheduler (`scheduler/`)
- APScheduler для периодических задач
- Cron-like конфигурация
- Интеграция с aiogram Bot для отправки сообщений

## 🔐 Безопасность

### Текущая реализация:
- ✅ Секреты в .env (не в git)
- ✅ .gitignore для чувствительных файлов
- ✅ Async PostgreSQL с connection pooling
- ✅ Логирование без чувствительных данных

### TODO для продакшена:
- [ ] Rate limiting для команд
- [ ] Input validation и sanitization
- [ ] HTTPS для webhooks
- [ ] Secrets management (Vault, AWS Secrets Manager)
- [ ] Мониторинг и алерты
- [ ] Backup стратегия для БД

## 🚀 Деплой

### Development (локально)
```bash
./setup.sh
source venv/bin/activate
python bot/main.py
```

### Production (Docker)
```bash
docker-compose up -d
docker-compose logs -f bot
```

### Production (Kubernetes) - TODO
```yaml
# В разработке
```

## 📊 Мониторинг

### Логи
- Формат: structured logging (loguru)
- Ротация: ежедневно, хранение 7 дней
- Уровни: INFO, WARNING, ERROR, CRITICAL

### Метрики (TODO)
- Prometheus metrics
- Grafana dashboards
- Alertmanager для критических ошибок

## 🧪 Тестирование (TODO)

```
tests/
├── unit/
│   ├── test_models.py
│   ├── test_repositories.py
│   └── test_services.py
├── integration/
│   ├── test_handlers.py
│   └── test_scheduler.py
└── e2e/
    └── test_bot_flow.py
```

## 🔄 CI/CD (TODO)

```yaml
# .github/workflows/ci.yml
- Lint (flake8, mypy)
- Tests (pytest)
- Build Docker image
- Deploy to staging
- Deploy to production (manual)
```

## 📈 Масштабирование

### Текущие ограничения:
- Single instance bot (polling)
- In-memory FSM storage
- No distributed scheduler

### Для масштабирования:
1. Переход на webhooks
2. Redis для FSM storage
3. Distributed scheduler (Celery)
4. Load balancing
5. Horizontal scaling

## 🔧 Расширение функциональности

### Добавление новой команды:
1. Создать handler в `handlers/user_handlers.py`
2. Зарегистрировать router в `bot/main.py`
3. Добавить FSM states если нужно multi-step flow
4. Обновить `/help` команду

### Добавление новой модели:
1. Создать model в `db/models.py`
2. Создать repository в `db/repository.py`
3. Создать миграцию (Alembic)
4. Обновить handlers

### Добавление нового сервиса:
1. Создать файл в `services/`
2. Реализовать интеграцию
3. Добавить конфигурацию в `bot/config.py`
4. Использовать в handlers или scheduler

---

**Версия:** 1.0.0  
**Последнее обновление:** 2024-01-01

