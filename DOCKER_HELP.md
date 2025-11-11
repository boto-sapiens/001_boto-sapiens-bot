# 🐳 Docker Commands for boto-chronicler

## 🚀 Quick Start Commands

### Development
```bash
# Запуск в DEV режиме
./run_dev.sh

# Или вручную
docker compose up -d
```

### Production
```bash
# Запуск в PROD режиме
./run_prod.sh
```

## 📋 Основные команды

### Управление контейнером
```bash
# Запуск в фоне
docker compose up -d

# Остановка
docker compose down

# Перезапуск
docker compose restart

# Перезапуск с пересборкой
docker compose up -d --build

# Остановка и удаление volumes
docker compose down -v
```

### Просмотр логов
```bash
# Просмотр логов в реальном времени
docker logs -f boto-chronicler

# Последние 100 строк логов
docker logs --tail 100 boto-chronicler

# Логи за последний час
docker logs --since 1h boto-chronicler
```

### Мониторинг
```bash
# Статус контейнера
docker compose ps

# Детальная информация о контейнере
docker inspect boto-chronicler

# Использование ресурсов
docker stats boto-chronicler

# Процессы внутри контейнера
docker exec boto-chronicler ps aux
```

### Отладка
```bash
# Войти в контейнер
docker exec -it boto-chronicler bash

# Выполнить команду в контейнере
docker exec boto-chronicler python -c "print('Hello from container')"

# Просмотр переменных окружения
docker exec boto-chronicler env
```

## 🔧 Обслуживание

### Обновление образа
```bash
# Получить последние изменения из Git
git pull

# Пересобрать и перезапустить
docker compose down
docker compose build --no-cache
docker compose up -d
```

### Очистка
```bash
# Удалить неиспользуемые образы
docker image prune

# Удалить все неиспользуемые ресурсы
docker system prune

# Удалить конкретный образ
docker rmi boto-chronicler:latest
```

### Backup и восстановление
```bash
# Создать backup логов
tar -czf logs_backup_$(date +%Y%m%d_%H%M%S).tar.gz logs/

# Очистить старые логи (старше 7 дней)
find logs/ -name "*.log" -mtime +7 -delete
```

## 🚨 Troubleshooting

### Контейнер не запускается
```bash
# Проверить логи
docker logs boto-chronicler

# Проверить конфигурацию
docker compose config

# Проверить переменные окружения
docker exec boto-chronicler env | grep -E "(BOT_TOKEN|OPENAI|DATABASE)"
```

### Проблемы с сетью
```bash
# Проверить сетевые подключения
docker network ls
docker network inspect boto-chronicler_default

# Проверить порты
docker port boto-chronicler
```

### Проблемы с volumes
```bash
# Проверить mounted volumes
docker inspect boto-chronicler | grep -A 10 "Mounts"

# Проверить права доступа к папке logs
ls -la logs/
```

## 📊 Мониторинг производительности

### Системные ресурсы
```bash
# Использование CPU и памяти
docker stats boto-chronicler --no-stream

# Детальная статистика
docker exec boto-chronicler cat /proc/meminfo
docker exec boto-chronicler cat /proc/cpuinfo
```

### Логирование
```bash
# Размер логов
du -sh logs/

# Количество строк в логах
wc -l logs/*.log

# Поиск ошибок
grep -i error logs/bot.log
grep -i exception logs/bot.log
```

## 🔄 Автоматизация

### Cron задачи для мониторинга
```bash
# Добавить в crontab для проверки статуса каждые 5 минут
*/5 * * * * cd /path/to/boto-chronicler && docker compose ps | grep -q "Up" || ./run_prod.sh

# Еженедельная очистка логов
0 2 * * 0 cd /path/to/boto-chronicler && find logs/ -name "*.log" -mtime +7 -delete
```

### Health check скрипт
```bash
#!/bin/bash
# health_check.sh
if ! docker compose ps | grep -q "Up"; then
    echo "Container is down, restarting..."
    ./run_prod.sh
fi
```

## 📝 Полезные алиасы

Добавьте в `~/.bashrc` или `~/.zshrc`:
```bash
alias boto-logs='docker logs -f boto-chronicler'
alias boto-status='docker compose ps'
alias boto-restart='docker compose restart'
alias boto-stop='docker compose down'
alias boto-start='./run_prod.sh'
```
