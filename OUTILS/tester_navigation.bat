@echo off
setlocal
cd /d "%~dp0"
echo ==============================================
echo   AllRoads - Test groupe Navigation / Bus
echo ==============================================
echo.
if exist "api\.venv\Scripts\python.exe" (
  "api\.venv\Scripts\python.exe" -m pytest -m navigation -q
) else (
  python -m pytest -m navigation -q
)
echo.
if errorlevel 1 (
  echo RESULTAT : ECHEC - copier le message affiche et le transmettre dans ChatGPT.
) else (
  echo RESULTAT : OK - bloc Navigation / Bus valide.
)
echo.
pause
