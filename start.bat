@echo off
echo Starting ASR Benchmark Hub Backend...
echo.

REM Check if virtual environment exists
if not exist "venv\" (
    echo Creating virtual environment...
    python -m venv venv
)

REM Activate virtual environment
echo Activating virtual environment...
call venv\Scripts\activate.bat

REM Install dependencies
echo Installing dependencies...
pip install -r requirements.txt

REM Check if .env file exists
if not exist ".env" (
    echo.
    echo WARNING: .env file not found!
    echo Please copy .env.example to .env and add your Gemini API key
    echo.
    pause
)

REM Start the server
echo.
echo Starting FastAPI server...
echo Server will be available at: http://127.0.0.1:8000
echo API documentation at: http://127.0.0.1:8000/docs
echo.
uvicorn main:app --reload --host 127.0.0.1 --port 8000