# 🛠️ Скрипты управления boto-sapiens

## 📋 Доступные скрипты

### 🚀 `run.sh` - Запуск бота

Основной скрипт для запуска бота.

**Что делает:**
- Проверяет наличие виртуального окружения
- Проверяет наличие .env файла
- Активирует виртуальное окружение
- Устанавливает PYTHONPATH
- Запускает бота

**Использование:**
```bash
./run.sh
```

**Вывод при успехе:**
```
🧬 Starting boto-sapiens...
📦 Activating virtual environment...
🚀 Launching bot...
✅ OpenAI API key successfully decoded from Base64
✅ Bot startup completed successfully
📡 Starting polling...
```

---

### 🛑 `stop.sh` - Остановка бота

Останавливает работающий бот.

**Что делает:**
- Находит процессы бота
- Отправляет SIGTERM (мягкая остановка)
- Если не помогло, отправляет SIGKILL (принудительная остановка)

**Использование:**
```bash
./stop.sh
```

---

### 🔍 `status.sh` - Проверка статуса

Показывает информацию о состоянии бота.

**Что показывает:**
- Запущен ли бот (PID, CPU, память)
- Последние 5 записей из логов
- Наличие .env файла
- Наличие виртуального окружения

**Использование:**
```bash
./status.sh
```

**Пример вывода:**
```
🔍 Checking boto-sapiens status...

✅ Bot is running:
   PID: 12345 | CPU: 2.5% | MEM: 1.8% | Started: 10:30

📋 Last 5 log entries:
2024-01-01 10:30:04 | SUCCESS | Bot startup completed
...

✅ .env file exists
✅ Virtual environment exists
```

---

### 🔐 `encode_key.py` - Кодирование OpenAI ключа

Интерактивный скрипт для кодирования API ключа в Base64.

**Использование:**
```bash
python3 encode_key.py
```

**Интерактивный режим:**
```bash
python3 encode_key.py
# Введите ваш OpenAI API ключ (начинается с sk-):
# > sk-your-key
```

**С аргументом:**
```bash
python3 encode_key.py "sk-your-key"
```

---

### 🧪 `test_config.py` - Тестирование конфигурации

Проверяет правильность настройки бота.

**Что проверяет:**
- Base64 кодирование/декодирование
- Наличие и формат .env файла
- Загрузку конфигурации
- Валидацию всех параметров

**Использование:**
```bash
python3 test_config.py
```

**Успешный вывод:**
```
✅ Base64 encoding/decoding works!
✅ .env file has OPENAI_API_KEY_BASE64
✅ Configuration loaded successfully!
✅ All tests passed!
```

---

### ⚙️ `setup.sh` - Быстрая установка

Автоматическая установка и настройка проекта.

**Что делает:**
- Создает виртуальное окружение
- Устанавливает зависимости
- Создает .env из примера
- Создает директорию для логов

**Использование:**
```bash
./setup.sh
```

---

## 📝 Типичные сценарии использования

### Первый запуск

```bash
# 1. Установка
./setup.sh

# 2. Настройка .env (отредактируйте файл)
nano .env

# 3. Кодирование OpenAI ключа
python3 encode_key.py

# 4. Проверка конфигурации
python3 test_config.py

# 5. Запуск бота
./run.sh
```

### Ежедневное использование

```bash
# Запустить бота
./run.sh

# В другом терминале проверить статус
./status.sh

# Остановить бота
./stop.sh
```

### Отладка проблем

```bash
# Проверить конфигурацию
python3 test_config.py

# Проверить статус
./status.sh

# Посмотреть логи
tail -f logs/bot.log

# Перезапустить бота
./stop.sh && ./run.sh
```

---

## 🐛 Устранение неполадок

### Ошибка: "No module named 'bot'"

**Проблема:** PYTHONPATH не установлен

**Решение:** Используйте `./run.sh` вместо прямого запуска

### Ошибка: "Permission denied"

**Проблема:** Скрипты не исполняемые

**Решение:**
```bash
chmod +x run.sh stop.sh status.sh setup.sh
```

### Бот не останавливается

**Решение:**
```bash
# Найдите PID вручную
ps aux | grep "python3 bot/main.py"

# Убейте процесс
kill -9 <PID>
```

### Ошибка конфигурации

**Решение:**
```bash
# Проверьте конфигурацию
python3 test_config.py

# Пересоздайте .env
cp env.example .env
# Отредактируйте .env
```

---

## 💡 Советы

1. **Всегда используйте `./run.sh`** для запуска - он делает все правильно
2. **Проверяйте статус** с помощью `./status.sh` перед остановкой
3. **Тестируйте конфигурацию** после изменения .env
4. **Следите за логами** в `logs/bot.log`
5. **Делайте backup** .env перед изменениями

---

## 🔄 Автозапуск (systemd)

Для запуска бота как сервиса создайте файл `/etc/systemd/system/boto-sapiens.service`:

```ini
[Unit]
Description=boto-sapiens Telegram Bot
After=network.target postgresql.service

[Service]
Type=simple
User=your-user
WorkingDirectory=/path/to/boto-sapiens
ExecStart=/path/to/boto-sapiens/run.sh
Restart=always
RestartSec=10

[Install]
WantedBy=multi-user.target
```

Затем:
```bash
sudo systemctl daemon-reload
sudo systemctl enable boto-sapiens
sudo systemctl start boto-sapiens
sudo systemctl status boto-sapiens
```

---

**🧬 boto-sapiens** - Удобное управление ботом!

