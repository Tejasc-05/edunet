@echo off
REM Batch file to create superuser
cd /d "%~dp0"
echo Creating Django Superuser...
echo.
python manage.py createsuperuser
pause
