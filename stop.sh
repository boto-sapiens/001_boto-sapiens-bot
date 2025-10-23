#!/bin/bash
# Stop boto-sapiens bot

GREEN='\033[0;32m'
RED='\033[0;31m'
NC='\033[0m'

echo -e "${GREEN}🛑 Stopping boto-sapiens...${NC}"

# Find and kill bot processes
BOT_PIDS=$(ps aux | grep "python3 bot/main.py" | grep -v grep | awk '{print $2}')

if [ -z "$BOT_PIDS" ]; then
    echo -e "${RED}No running bot processes found${NC}"
    exit 0
fi

for PID in $BOT_PIDS; do
    echo -e "${GREEN}Killing process $PID${NC}"
    kill -15 $PID
done

sleep 2

# Force kill if still running
BOT_PIDS=$(ps aux | grep "python3 bot/main.py" | grep -v grep | awk '{print $2}')
if [ ! -z "$BOT_PIDS" ]; then
    for PID in $BOT_PIDS; do
        echo -e "${RED}Force killing process $PID${NC}"
        kill -9 $PID
    done
fi

echo -e "${GREEN}✅ Bot stopped${NC}"

