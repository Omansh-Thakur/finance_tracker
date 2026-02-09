@echo off
REM Quick setup script for development environment on Windows

echo.
echo ========================================
echo Finance Tracker - Setup Script
echo ========================================
echo.

REM Check if Python is installed
python --version >nul 2>&1
if %ERRORLEVEL% NEQ 0 (
    echo ❌ Python is not installed. Please install Python 3.8 or higher.
    pause
    exit /b 1
)

for /f "tokens=*" %%i in ('python --version') do set PYTHON_VERSION=%%i
echo ✓ Python found: %PYTHON_VERSION%

REM Create virtual environment
echo.
echo Creating virtual environment...
python -m venv venv

REM Activate virtual environment
echo Activating virtual environment...
call venv\Scripts\activate.bat

REM Upgrade pip
echo Upgrading pip...
python -m pip install --upgrade pip

REM Install requirements
echo.
echo Installing dependencies...
pip install -r requirements.txt

REM Copy .env file
if not exist .env (
    echo.
    echo Creating .env file from .env.example...
    copy .env.example .env
    echo ⚠️  Please edit .env file with your configuration
) else (
    echo ✓ .env file already exists
)

REM Run migrations
echo.
echo Running migrations...
python manage.py migrate

REM Create superuser prompt
echo.
echo ========================================
echo Setup Complete!
echo ========================================
echo.
echo Next steps:
echo 1. Edit .env with your settings (especially database credentials)
echo 2. Create a superuser: python manage.py createsuperuser
echo 3. Start development server: python manage.py runserver
echo 4. Visit http://localhost:8000/ in your browser
echo.
echo To activate the virtual environment in the future:
echo   venv\Scripts\activate
echo.
pause
