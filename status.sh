#!/bin/bash
# Check boto-sapiens bot status

GREEN='\033[0;32m'
RED='\033[0;31m'
YELLOW='\033[1;33m'
NC='\033[0m'

echo -e "${GREEN}🔍 Checking boto-sapiens status...${NC}"
echo ""

# Check if bot is running
BOT_PIDS=$(ps aux | grep "python3 bot/main.py" | grep -v grep)

if [ -z "$BOT_PIDS" ]; then
    echo -e "${RED}❌ Bot is NOT running${NC}"
else
    echo -e "${GREEN}✅ Bot is running:${NC}"
    echo "$BOT_PIDS" | awk '{print "   PID: " $2 " | CPU: " $3 "% | MEM: " $4 "% | Started: " $9}'
fi

echo ""

# Check logs
if [ -f "logs/bot.log" ]; then
    echo -e "${GREEN}📋 Last 5 log entries:${NC}"
    tail -5 logs/bot.log
else
    echo -e "${YELLOW}⚠️  No log file found${NC}"
fi

echo ""

# Check .env
if [ -f ".env" ]; then
    echo -e "${GREEN}✅ .env file exists${NC}"
else
    echo -e "${RED}❌ .env file missing${NC}"
fi

# Check venv
if [ -d "venv" ]; then
    echo -e "${GREEN}✅ Virtual environment exists${NC}"
else
    echo -e "${RED}❌ Virtual environment missing${NC}"
fi

