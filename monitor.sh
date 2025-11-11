#!/bin/bash
# boto-chronicler monitoring script

# Colors for output
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
RED='\033[0;31m'
BLUE='\033[0;34m'
NC='\033[0m' # No Color

echo -e "${GREEN}📊 boto-chronicler Monitoring Dashboard${NC}"
echo "=========================================="
echo ""

# Change to script directory
cd "$(dirname "$0")"

# Container status
echo -e "${BLUE}🐳 Container Status:${NC}"
if docker compose ps | grep -q "Up"; then
    echo -e "  ${GREEN}✅ Container is running${NC}"
    docker compose ps
else
    echo -e "  ${RED}❌ Container is not running${NC}"
fi
echo ""

# Resource usage
echo -e "${BLUE}💻 Resource Usage:${NC}"
if docker compose ps | grep -q "Up"; then
    docker stats boto-chronicler --no-stream --format "table {{.Container}}\t{{.CPUPerc}}\t{{.MemUsage}}\t{{.NetIO}}\t{{.BlockIO}}"
else
    echo -e "  ${YELLOW}⚠️  Container is not running${NC}"
fi
echo ""

# Logs summary
echo -e "${BLUE}📋 Recent Logs (last 10 lines):${NC}"
if docker compose ps | grep -q "Up"; then
    docker logs --tail 10 boto-chronicler
else
    echo -e "  ${YELLOW}⚠️  Container is not running${NC}"
fi
echo ""

# Environment files
echo -e "${BLUE}⚙️  Environment Files:${NC}"
if [ -f ".env" ]; then
    echo -e "  ${GREEN}✓${NC} .env (DEV)"
else
    echo -e "  ${RED}✗${NC} .env (DEV)"
fi

if [ -f ".env.prod" ]; then
    echo -e "  ${GREEN}✓${NC} .env.prod (PROD)"
else
    echo -e "  ${RED}✗${NC} .env.prod (PROD)"
fi
echo ""

# Log files
echo -e "${BLUE}📁 Log Files:${NC}"
if [ -d "logs" ]; then
    echo -e "  ${GREEN}✓${NC} logs/ directory exists"
    if [ -f "logs/bot.log" ]; then
        LOG_SIZE=$(du -h logs/bot.log | cut -f1)
        echo -e "  ${GREEN}✓${NC} bot.log (${LOG_SIZE})"
    else
        echo -e "  ${YELLOW}⚠️  bot.log not found${NC}"
    fi
else
    echo -e "  ${RED}✗${NC} logs/ directory not found"
fi
echo ""

# Quick actions
echo -e "${BLUE}🔧 Quick Actions:${NC}"
echo "  View logs:     docker logs -f boto-chronicler"
echo "  Restart:       docker compose restart"
echo "  Stop:         docker compose down"
echo "  Start DEV:    ./run_dev.sh"
echo "  Start PROD:   ./run_prod.sh"
echo "  Switch env:   ./switch_env.sh"
echo ""

# Health check
echo -e "${BLUE}🏥 Health Check:${NC}"
if docker compose ps | grep -q "Up"; then
    # Try to execute a simple command in the container
    if docker exec boto-chronicler python -c "print('OK')" >/dev/null 2>&1; then
        echo -e "  ${GREEN}✅ Container is healthy${NC}"
    else
        echo -e "  ${RED}❌ Container is not responding${NC}"
    fi
else
    echo -e "  ${RED}❌ Container is not running${NC}"
fi
