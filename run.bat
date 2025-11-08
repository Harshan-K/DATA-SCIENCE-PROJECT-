@echo off
echo Starting Accident Detection Web Application...
echo.

REM Check if virtual environment exists
if not exist "venv" (
    echo Creating virtual environment...
    python -m venv venv
)

REM Activate virtual environment
echo Activating virtual environment...
call venv\Scripts\activate.bat

REM Install requirements
echo Installing requirements...
pip install -r requirements.txt

REM Start the application
echo.
echo Starting web server on http://localhost:5000
echo Press Ctrl+C to stop the server
echo.
python app.py

pause