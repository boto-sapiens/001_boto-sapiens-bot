#!/bin/bash
# Start both aiogram bot and FastAPI webhook server

echo "🚀 Starting ChroniclerBot with Arena integration..."

# Decode OpenAI API key first (shared by both processes)
python3 -c "
import base64, os
key = os.getenv('OPENAI_API_KEY_BASE64', '')
if key:
    decoded = base64.b64decode(key).decode('utf-8')
    print(f'export OPENAI_API_KEY={decoded}')
" > /tmp/openai_key.sh
source /tmp/openai_key.sh
rm /tmp/openai_key.sh

echo "✅ OpenAI API key decoded"

# Start aiogram bot in background
python bot/main.py &
BOT_PID=$!
echo "✅ Aiogram bot started (PID: $BOT_PID)"

# Wait a bit for bot to initialize
sleep 2

# Start FastAPI webhook server
python fastapi_app.py &
FASTAPI_PID=$!
echo "✅ FastAPI webhook server started (PID: $FASTAPI_PID)"

# Wait for both processes
wait -n

# If one exits, kill the other
kill $BOT_PID $FASTAPI_PID 2>/dev/null

