#!/bin/bash

echo "🔧 Setting up sol-meme-ai..."

# Check Python
if ! command -v python3 &> /dev/null
then
    echo "❌ Python3 is not installed. Please install Python 3.8+."
    exit
fi

# Create virtual environment
echo "📦 Creating virtual environment..."
python3 -m venv venv
source venv/bin/activate

# Upgrade pip
echo "⚙️ Upgrading pip..."
pip install --upgrade pip

# Install dependencies
if [ -f "requirements.txt" ]; then
    echo "📦 Installing dependencies..."
    pip install -r requirements.txt
else
    echo "⚠️ requirements.txt not found. Please add it to the root directory."
    exit
fi

# Success message
echo "✅ Setup complete!"
echo ""
echo "🧠 You can now run the bot: python3 bot/ai_solchain.py"
echo "📊 Or launch the dashboard: streamlit run dashboard/dashboard.py"