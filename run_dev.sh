#!/bin/bash
# boto-chronicler DEV startup script

# Colors for output
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
RED='\033[0;31m'
BLUE='\033[0;34m'
NC='\033[0m' # No Color

echo -e "${GREEN}🧬 Starting boto-chronicler in DEV mode...${NC}"

# Change to script directory
cd "$(dirname "$0")"

# Check if .env exists
if [ ! -f ".env" ]; then
    echo -e "${RED}❌ .env file not found!${NC}"
    echo -e "${YELLOW}💡 Copy env.example to .env and configure it${NC}"
    exit 1
fi

# Stop and remove existing containers
echo -e "${BLUE}🛑 Stopping existing containers...${NC}"
docker compose down --remove-orphans

# Build the image
echo -e "${BLUE}🔨 Building Docker image...${NC}"
docker compose build --no-cache

# Start the container in background
echo -e "${BLUE}🚀 Starting container in background...${NC}"
docker compose up -d

# Wait a moment for container to start
sleep 3

# Check container status
echo -e "${GREEN}📊 Container Status:${NC}"
docker compose ps

echo ""
echo -e "${GREEN}✅ boto-chronicler started in DEV mode!${NC}"
echo ""
echo -e "${YELLOW}📋 Useful commands:${NC}"
echo -e "  ${BLUE}View logs:${NC}        docker logs -f boto-chronicler"
echo -e "  ${BLUE}Stop bot:${NC}         docker compose down"
echo -e "  ${BLUE}Restart:${NC}          docker compose restart"
echo -e "  ${BLUE}Check status:${NC}     docker compose ps"
echo ""
echo -e "${YELLOW}🔍 To view logs in real-time:${NC}"
echo -e "  ${BLUE}docker logs -f boto-chronicler${NC}"
