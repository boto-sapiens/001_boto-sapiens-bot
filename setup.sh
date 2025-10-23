#!/bin/bash

echo "🧬 Setting up boto-sapiens..."

# Create virtual environment
echo "📦 Creating virtual environment..."
python3 -m venv venv

# Activate virtual environment
echo "🔧 Activating virtual environment..."
source venv/bin/activate

# Install dependencies
echo "📥 Installing dependencies..."
pip install --upgrade pip
pip install -r requirements.txt

# Create logs directory
echo "📁 Creating logs directory..."
mkdir -p logs

# Copy .env.example to .env if not exists
if [ ! -f .env ]; then
    echo "⚙️ Creating .env file..."
    cp env.example .env
    echo "⚠️  Please edit .env file with your credentials!"
else
    echo "✅ .env file already exists"
fi

echo ""
echo "✅ Setup complete!"
echo ""
echo "Next steps:"
echo "1. Edit .env file with your credentials"
echo "2. Setup PostgreSQL database"
echo "3. Run: python bot/main.py"
echo ""
echo "🧬 boto-sapiens is ready!"

