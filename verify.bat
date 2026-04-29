@echo off
REM Quick verification script for DataDivas Streamlit app setup (Windows)

echo.
echo 🔍 DataDivas Streamlit App Verification
echo ======================================== 
echo.

REM Check Python version
echo ✓ Checking Python version...
python --version
echo.

REM Check if requirements.txt exists
echo ✓ Checking requirements.txt...
if exist requirements.txt (
    echo   ✅ requirements.txt found
    type requirements.txt
) else (
    echo   ❌ requirements.txt not found
    exit /b 1
)
echo.

REM Check if streamlit_app.py exists
echo ✓ Checking streamlit_app.py...
if exist streamlit_app.py (
    echo   ✅ streamlit_app.py found
) else (
    echo   ❌ streamlit_app.py not found
    exit /b 1
)
echo.

REM Check datadivas package
echo ✓ Checking datadivas package...
if exist datadivas\__init__.py (
    echo   ✅ datadivas\__init__.py found
) else (
    echo   ❌ datadivas package not found
    exit /b 1
)
echo.

REM Check assignment.py
echo ✓ Checking datadivas/assignment.py...
if exist datadivas\assignment.py (
    echo   ✅ datadivas\assignment.py found
) else (
    echo   ❌ datadivas\assignment.py not found
    exit /b 1
)
echo.

REM Suggest next steps
echo 📝 Next Steps:
echo 1. Install dependencies:
echo    pip install -r requirements.txt
echo.
echo 2. Run locally:
echo    streamlit run streamlit_app.py
echo.
echo 3. Deploy to Streamlit Cloud:
echo    - Push to GitHub
echo    - Go to https://share.streamlit.io
echo    - Select your repository and streamlit_app.py
echo.
echo ✅ Setup verification complete!
echo.
pause
