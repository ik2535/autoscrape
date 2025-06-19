@echo off
echo Starting Dagster daemon for scheduled car scraping...
echo.
echo This will run car scraping daily at 2 AM automatically.
echo Press Ctrl+C to stop the daemon.
echo.

cd /d "%~dp0"
dagster-daemon run -f definitions.py
