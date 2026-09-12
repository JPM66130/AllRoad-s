@echo off
cd /d "%~dp0"
set PYTHONPATH=api;.
if exist "api\.venv\Scripts\python.exe" (
  "api\.venv\Scripts\python.exe" -m pytest -q -m data_route
) else (
  python -m pytest -q -m data_route
)
pause
