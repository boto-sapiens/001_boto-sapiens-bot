# 🐳 Docker Guide for boto-chronicler

## 🚀 Быстрый старт

### Development Environment
```bash
# 1. Настройте .env файл
cp env.example .env
nano .env  # Отредактируйте настройки

# 2. Запустите в DEV режиме
./run_dev.sh
```

### Production Environment
```bash
# 1. Настройте .env.prod файл
cp env.prod.example .env.prod
nano .env.prod  # Отредактируйте настройки

# 2. Запустите в PROD режиме
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

## 🔧 Переключение между DEV и PROD

### DEV → PROD
```bash
# 1. Остановите DEV контейнер
docker compose down

# 2. Создайте/обновите .env.prod
cp env.prod.example .env.prod
nano .env.prod

# 3. Запустите в PROD режиме
./run_prod.sh
```

### PROD → DEV
```bash
# 1. Остановите PROD контейнер
docker compose down

# 2. Убедитесь что .env настроен
nano .env

# 3. Запустите в DEV режиме
./run_dev.sh
```

## 🚨 Автоматический перезапуск

### Настройка restart policy
В `docker-compose.yml` уже настроено:
```yaml
restart: unless-stopped
```

Это означает:
- ✅ Автоматический перезапуск при сбоях
- ✅ Перезапуск при перезагрузке системы
- ❌ НЕ перезапускается при ручной остановке

### Мониторинг перезапусков
```bash
# Проверить количество перезапусков
docker inspect boto-chronicler | grep -i restart

# Просмотр событий контейнера
docker events --filter container=boto-chronicler
```

## 📊 Мониторинг и отладка

### Health Check
```bash
# Проверить здоровье контейнера
docker inspect boto-chronicler | grep -A 10 Health

# Ручная проверка
docker exec boto-chronicler python -c "print('Container is healthy')"
```

### Отладка проблем
```bash
# Войти в контейнер для отладки
docker exec -it boto-chronicler bash

# Проверить переменные окружения
docker exec boto-chronicler env

# Проверить файловую систему
docker exec boto-chronicler ls -la /app

# Проверить логи приложения
docker exec boto-chronicler tail -f /app/logs/bot.log
```

## 🔄 Обновление и деплой

### Полный цикл обновления
```bash
# 1. Получить последние изменения
git pull

# 2. Остановить текущий контейнер
docker compose down

# 3. Пересобрать образ
docker compose build --no-cache

# 4. Запустить обновленный контейнер
./run_prod.sh  # или ./run_dev.sh

# 5. Проверить статус
docker compose ps
docker logs -f boto-chronicler
```

### Hot reload (только для DEV)
```bash
# Для разработки можно использовать volume mounting
# Это позволит видеть изменения кода без пересборки
docker compose -f docker-compose.dev.yml up -d
```

## 🧹 Очистка и обслуживание

### Очистка неиспользуемых ресурсов
```bash
# Удалить неиспользуемые образы
docker image prune

# Удалить все неиспользуемые ресурсы
docker system prune

# Удалить конкретный образ
docker rmi boto-chronicler:latest
```

### Backup логов
```bash
# Создать backup логов
tar -czf logs_backup_$(date +%Y%m%d_%H%M%S).tar.gz logs/

# Очистить старые логи (старше 7 дней)
find logs/ -name "*.log" -mtime +7 -delete
```

## 📝 Полезные алиасы

Добавьте в `~/.bashrc` или `~/.zshrc`:
```bash
# boto-chronicler aliases
alias boto-logs='docker logs -f boto-chronicler'
alias boto-status='docker compose ps'
alias boto-restart='docker compose restart'
alias boto-stop='docker compose down'
alias boto-start-dev='./run_dev.sh'
alias boto-start-prod='./run_prod.sh'
alias boto-shell='docker exec -it boto-chronicler bash'
```

## 🚀 Production Best Practices

### 1. Мониторинг
```bash
# Настройте мониторинг контейнера
# Добавьте в crontab:
*/5 * * * * cd /path/to/boto-chronicler && docker compose ps | grep -q "Up" || ./run_prod.sh
```

### 2. Логирование
```bash
# Настройте ротацию логов
# Добавьте в logrotate:
/path/to/boto-chronicler/logs/*.log {
    daily
    rotate 7
    compress
    delaycompress
    missingok
    notifempty
}
```

### 3. Backup
```bash
# Автоматический backup логов
0 2 * * * cd /path/to/boto-chronicler && tar -czf /backup/logs_$(date +\%Y\%m\%d).tar.gz logs/
```

## ❓ Troubleshooting

### Контейнер не запускается
1. Проверьте логи: `docker logs boto-chronicler`
2. Проверьте конфигурацию: `docker compose config`
3. Проверьте переменные окружения: `docker exec boto-chronicler env`

### Проблемы с сетью
1. Проверьте сетевые подключения: `docker network ls`
2. Проверьте порты: `docker port boto-chronicler`

### Проблемы с volumes
1. Проверьте mounted volumes: `docker inspect boto-chronicler | grep -A 10 "Mounts"`
2. Проверьте права доступа: `ls -la logs/`
