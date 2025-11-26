@echo off
echo ============================================================
echo AMUCSS Quick Setup Script (Windows)
echo ============================================================
echo.

REM Check if virtual environment exists
if not exist "venv\" (
    echo Creating virtual environment...
    python -m venv venv
    echo Virtual environment created.
    echo.
)

echo Activating virtual environment...
call venv\Scripts\activate.bat
echo.

echo Installing dependencies...
pip install -r requirements.txt
echo.

REM Check if .env exists
if not exist ".env" (
    echo Creating .env file from template...
    copy .env.example .env
    echo.
    echo IMPORTANT: Edit .env file and add your configuration!
    echo.
)

echo Running migrations...
python manage.py makemigrations
python manage.py migrate
echo.

echo Collecting static files...
python manage.py collectstatic --noinput
echo.

echo ============================================================
echo Setup Complete!
echo ============================================================
echo.
echo Next steps:
echo 1. Edit .env file with your configuration
echo 2. Create superuser: python manage.py createsuperuser
echo 3. Run server: python manage.py runserver
echo 4. After testing, run cleanup: python cleanup_old_files.py
echo.
echo See FINAL_SETUP.md for detailed instructions.
echo.
pause
