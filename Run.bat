@echo off
echo Activating virtual environment...
call myenv\Scripts\activate.bat

timeout /t 3 /nobreak >nul

echo Running Streamlit app...
start cmd /k "streamlit run app.py"

timeout /t 3 /nobreak >nul

echo Opening browser to http://127.0.0.1:5000
start http://127.0.0.1:5000
