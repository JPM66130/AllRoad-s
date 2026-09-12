@echo off
setlocal
cd /d "%~dp0"
set "ALLROADS_ACCESS_STATE=PRO"
set "ENVIRONMENT=development"

echo.
echo ============================================================
echo       AllRoads V52.7.5 - PONT PC ^<^> TELEPHONE
echo ============================================================
echo.
echo 1. Fermez d'abord une ancienne fenetre noire AllRoads si elle tourne.
echo 2. Le serveur va demarrer dans une nouvelle fenetre.
echo 3. La console de test va s'ouvrir automatiquement sur ce PC.
echo 4. Sur le telephone, ouvrez AllRoads avec l'adresse habituelle.
echo.
if exist ".venv\Scripts\python.exe" (
  start "AllRoads serveur V52.7.5" cmd /k "\"%CD%\.venv\Scripts\python.exe\" -m uvicorn api.main:app --host 0.0.0.0 --port 8000"
) else (
  start "AllRoads serveur V52.7.5" cmd /k "python -m uvicorn api.main:app --host 0.0.0.0 --port 8000"
)
timeout /t 3 /nobreak >nul
start "" "http://127.0.0.1:8000/app/test-console.html"
echo Console PC ouverte.
echo.
echo Adresse(s) possible(s) pour le telephone :
for /f "tokens=2 delims=:" %%A in ('ipconfig ^| findstr /c:"IPv4"') do (
  for /f "tokens=*" %%B in ("%%A") do echo    http://%%B:8000/app
)
echo.
echo Vous pouvez fermer cette fenetre. Gardez la fenetre serveur ouverte.
pause
