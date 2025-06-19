@echo off
echo Starting AutoScrape Analytics Dashboard...
echo.
echo Dashboard will open in your browser at http://localhost:8501
echo Press Ctrl+C to stop the dashboard.
echo.

cd /d "%~dp0"
streamlit run src/analytics/dashboard.py
