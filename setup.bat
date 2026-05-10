@echo off
REM TalentScout Setup Script for Windows
REM This script helps set up the Hiring Assistant chatbot

echo.
echo ╔════════════════════════════════════════════════════════╗
echo ║     TalentScout - Hiring Assistant Setup Script       ║
echo ║                    (Windows)                          ║
echo ╚════════════════════════════════════════════════════════╝
echo.

REM Check Python installation
echo ✓ Checking Python installation...
python --version >nul 2>&1
if errorlevel 1 (
    echo ❌ Python is not installed or not in PATH.
    echo Please install Python 3.8 or higher from https://www.python.org/
    pause
    exit /b 1
)
for /f "tokens=2" %%i in ('python --version 2^>^&1') do set PYTHON_VERSION=%%i
echo ✅ Python %PYTHON_VERSION% is installed
echo.

REM Create virtual environment
echo 📦 Creating virtual environment...
if not exist "venv" (
    python -m venv venv
    echo ✅ Virtual environment created
) else (
    echo ⚠️  Virtual environment already exists
)
echo.

REM Activate virtual environment
echo 🔄 Activating virtual environment...
call venv\Scripts\activate.bat
echo ✅ Virtual environment activated
echo.

REM Install dependencies
echo 📥 Installing dependencies from requirements.txt...
python -m pip install --quiet --upgrade pip
pip install -r requirements.txt
if errorlevel 1 (
    echo ❌ Failed to install dependencies
    pause
    exit /b 1
)
echo ✅ Dependencies installed
echo.

REM Check for .env file
echo ⚙️  Checking environment configuration...
if not exist ".env" (
    echo 📝 Creating .env file from template...
    if exist ".env.example" (
        copy .env.example .env
    ) else (
        (
            echo # Google Gemini API Configuration (FREE)
            echo GEMINI_API_KEY=your_api_key_here
        ) > .env
    )
    echo ⚠️  Please edit .env file and add your GEMINI_API_KEY
    echo 📖 Get your FREE API key from: https://aistudio.google.com/app/apikey
    echo.
    echo Opening .env file...
    notepad .env
) else (
    echo ✅ .env file already exists
)
echo.

REM Test imports
echo 🧪 Testing imports...
python << EOF
try:
    import streamlit
    print("✅ Streamlit imported successfully")
except ImportError as e:
    print(f"❌ Failed to import Streamlit: {e}")
    exit(1)

try:
    import google.generativeai
    print("✅ Google Generative AI SDK imported successfully")
except ImportError as e:
    print(f"❌ Failed to import Google Generative AI: {e}")
    exit(1)

try:
    from dotenv import load_dotenv
    print("✅ python-dotenv imported successfully")
except ImportError as e:
    print(f"❌ Failed to import python-dotenv: {e}")
    exit(1)

print("\n✅ All imports successful!")
EOF

if errorlevel 1 (
    echo.
    echo ❌ Import test failed. Please check your installation.
    pause
    exit /b 1
)

echo.
echo ╔════════════════════════════════════════════════════════╗
echo ║            Setup Complete! 🎉                         ║
echo ╚════════════════════════════════════════════════════════╝
echo.
echo 📝 Next steps:
echo   1. Make sure you've set GEMINI_API_KEY in .env (FREE from https://aistudio.google.com/app/apikey)
echo   2. Run: streamlit run hiring_assistant.py
echo   3. Open your browser to http://localhost:8501
echo.
echo 📚 For more information, see README.md
echo.
pause