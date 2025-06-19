@echo off
echo Running car scraping manually (50 cities)...
echo This will take 1-2 hours to complete.
echo.

cd /d "%~dp0"
dagster job execute -f definitions.py -j car_scraping_pipeline

echo.
echo Scraping complete! Check for the new CSV file.
pause
