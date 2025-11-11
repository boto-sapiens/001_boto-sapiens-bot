#!/bin/bash
# Run ChroniclerBot FastAPI app for arena webhooks

echo "🚀 Starting ChroniclerBot FastAPI webhook server..."

# Check if .env exists
if [ ! -f .env ]; then
    echo "⚠️  .env file not found. Creating from .env.example..."
    cp .env.example .env
    echo "📝 Please edit .env with your configuration and run again."
    exit 1
fi

# Activate virtual environment
source venv/bin/activate

# Run FastAPI app
echo "📡 Starting webhook server on port 8001..."
python fastapi_app.py

