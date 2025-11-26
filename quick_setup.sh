#!/bin/bash

echo "============================================================"
echo "AMUCSS Quick Setup Script (Linux/Mac)"
echo "============================================================"
echo ""

# Check if virtual environment exists
if [ ! -d "venv" ]; then
    echo "Creating virtual environment..."
    python3 -m venv venv
    echo "Virtual environment created."
    echo ""
fi

echo "Activating virtual environment..."
source venv/bin/activate
echo ""

echo "Installing dependencies..."
pip install -r requirements.txt
echo ""

# Check if .env exists
if [ ! -f ".env" ]; then
    echo "Creating .env file from template..."
    cp .env.example .env
    echo ""
    echo "IMPORTANT: Edit .env file and add your configuration!"
    echo ""
fi

echo "Running migrations..."
python manage.py makemigrations
python manage.py migrate
echo ""

echo "Collecting static files..."
python manage.py collectstatic --noinput
echo ""

echo "============================================================"
echo "Setup Complete!"
echo "============================================================"
echo ""
echo "Next steps:"
echo "1. Edit .env file with your configuration"
echo "2. Create superuser: python manage.py createsuperuser"
echo "3. Run server: python manage.py runserver"
echo "4. After testing, run cleanup: python cleanup_old_files.py"
echo ""
echo "See FINAL_SETUP.md for detailed instructions."
echo ""
