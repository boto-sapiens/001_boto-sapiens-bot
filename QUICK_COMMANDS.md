# ⚡ Quick Commands for boto-chronicler

## 🚀 Запуск
```bash
# DEV режим
./run_dev.sh

# PROD режим  
./run_prod.sh

# Переключение режимов
./switch_env.sh
```

## 📊 Мониторинг
```bash
# Статус и мониторинг
./monitor.sh

# Логи в реальном времени
docker logs -f boto-chronicler

# Статус контейнера
docker compose ps
```

## 🔧 Управление
```bash
# Перезапуск
docker compose restart

# Остановка
docker compose down

# Пересборка и запуск
docker compose up -d --build
```

## 🐛 Отладка
```bash
# Войти в контейнер
docker exec -it boto-chronicler bash

# Переменные окружения
docker exec boto-chronicler env

# Использование ресурсов
docker stats boto-chronicler
```

## 📁 Файлы
- `./run_dev.sh` - Запуск в DEV режиме
- `./run_prod.sh` - Запуск в PROD режиме  
- `./switch_env.sh` - Переключение режимов
- `./monitor.sh` - Мониторинг и статус
- `DOCKER_HELP.md` - Подробная справка
- `docker/README_DOCKER.md` - Полное руководство по Docker
