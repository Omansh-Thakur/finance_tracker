#!/bin/bash
# Quick setup script for development environment

echo "========================================"
echo "Finance Tracker - Setup Script"
echo "========================================"

# Check if Python is installed
if ! command -v python3 &> /dev/null; then
    echo "❌ Python 3 is not installed. Please install Python 3.8 or higher."
    exit 1
fi

echo "✓ Python found: $(python3 --version)"

# Create virtual environment
echo ""
echo "Creating virtual environment..."
python3 -m venv venv

# Activate virtual environment
echo "Activating virtual environment..."
source venv/bin/activate  # For macOS/Linux
# For Windows, use: venv\Scripts\activate

# Upgrade pip
echo "Upgrading pip..."
pip install --upgrade pip

# Install requirements
echo ""
echo "Installing dependencies..."
pip install -r requirements.txt

# Copy .env file
if [ ! -f .env ]; then
    echo ""
    echo "Creating .env file from .env.example..."
    cp .env.example .env
    echo "⚠️  Please edit .env file with your configuration"
else
    echo "✓ .env file already exists"
fi

# Run migrations
echo ""
echo "Running migrations..."
python manage.py migrate

# Create superuser prompt
echo ""
echo "========================================"
echo "Setup Complete!"
echo "========================================"
echo ""
echo "Next steps:"
echo "1. Edit .env with your settings (especially database credentials)"
echo "2. Create a superuser: python manage.py createsuperuser"
echo "3. Start development server: python manage.py runserver"
echo "4. Visit http://localhost:8000/ in your browser"
echo ""
echo "To activate the virtual environment in the future:"
echo "  source venv/bin/activate  (macOS/Linux)"
echo "  venv\Scripts\activate      (Windows)"
echo ""
