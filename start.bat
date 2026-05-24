@echo off
echo Starting AI Tutor RAG Application...

start cmd /k "cd /d %~dp0backend && ..\myenv\Scripts\activate && uvicorn main:app --reload --port 8000"

timeout /t 3

start cmd /k "cd /d %~dp0frontend && ..\myenv\Scripts\activate && streamlit run app.py"

echo Both servers starting...
echo Backend: http://localhost:8000
echo Frontend: http://localhost:8501