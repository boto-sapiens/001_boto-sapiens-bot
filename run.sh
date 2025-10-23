#!/bin/bash
# boto-sapiens startup script

# Colors for output
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
RED='\033[0;31m'
NC='\033[0m' # No Color

echo -e "${GREEN}🧬 Starting boto-sapiens...${NC}"

# Change to script directory
cd "$(dirname "$0")"

# Check if virtual environment exists
if [ ! -d "venv" ]; then
    echo -e "${RED}❌ Virtual environment not found!${NC}"
    echo -e "${YELLOW}💡 Run: python3 -m venv venv && source venv/bin/activate && pip install -r requirements.txt${NC}"
    exit 1
fi

# Check if .env exists
if [ ! -f ".env" ]; then
    echo -e "${RED}❌ .env file not found!${NC}"
    echo -e "${YELLOW}💡 Copy env.example to .env and configure it${NC}"
    exit 1
fi

# Activate virtual environment
echo -e "${GREEN}📦 Activating virtual environment...${NC}"
source venv/bin/activate

# Set PYTHONPATH
export PYTHONPATH="${PWD}"

# Run the bot
echo -e "${GREEN}🚀 Launching bot...${NC}"
python3 bot/main.py

# Deactivate on exit
deactivate

