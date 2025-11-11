#!/bin/bash
# boto-chronicler environment switcher

# Colors for output
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
RED='\033[0;31m'
BLUE='\033[0;34m'
NC='\033[0m' # No Color

echo -e "${GREEN}🔄 boto-chronicler Environment Switcher${NC}"
echo ""

# Change to script directory
cd "$(dirname "$0")"

# Check current environment
if [ -f ".env.prod" ] && docker compose ps | grep -q "Up"; then
    CURRENT_ENV="PROD"
else
    CURRENT_ENV="DEV"
fi

echo -e "${BLUE}Current environment: ${CURRENT_ENV}${NC}"
echo ""

# Show menu
echo -e "${YELLOW}Select environment:${NC}"
echo "1) Development (DEV)"
echo "2) Production (PROD)"
echo "3) Show current status"
echo "4) Exit"
echo ""

read -p "Enter your choice (1-4): " choice

case $choice in
    1)
        echo -e "${BLUE}🛑 Stopping current environment...${NC}"
        docker compose down --remove-orphans
        
        echo -e "${BLUE}🚀 Starting DEV environment...${NC}"
        ./run_dev.sh
        ;;
    2)
        echo -e "${BLUE}🛑 Stopping current environment...${NC}"
        docker compose down --remove-orphans
        
        if [ ! -f ".env.prod" ]; then
            echo -e "${RED}❌ .env.prod file not found!${NC}"
            echo -e "${YELLOW}💡 Creating .env.prod from template...${NC}"
            cp env.prod.example .env.prod
            echo -e "${YELLOW}⚠️  Please edit .env.prod with your production settings${NC}"
            exit 1
        fi
        
        echo -e "${BLUE}🚀 Starting PROD environment...${NC}"
        ./run_prod.sh
        ;;
    3)
        echo -e "${GREEN}📊 Current Status:${NC}"
        docker compose ps
        echo ""
        echo -e "${GREEN}📋 Environment Files:${NC}"
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
        ;;
    4)
        echo -e "${GREEN}👋 Goodbye!${NC}"
        exit 0
        ;;
    *)
        echo -e "${RED}❌ Invalid choice. Please select 1-4.${NC}"
        exit 1
        ;;
esac
