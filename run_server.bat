@echo off
REM Batch file to run Django development server
cd /d "%~dp0"
echo Starting Eco Waste Management Django Server...
echo.
echo Creating migrations...
python manage.py makemigrations
echo.
echo Applying migrations...
python manage.py migrate
echo.
echo Starting server at http://127.0.0.1:8000/
echo Press Ctrl+C to stop the server
echo.
python manage.py runserver
pause
