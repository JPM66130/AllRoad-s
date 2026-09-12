@echo off
setlocal
cd /d "%~dp0"

echo.
echo ============================================================
echo        AllRoad's V52.6 - DEMO MOBILE + CARTOGRAPHIE + PONT PC/TELEPHONE
echo ============================================================
echo.
echo Mode developpeur local : 8 profils deverrouilles.
echo Cette ouverture ne modifie pas le futur mode TEST / abonnement.
echo.
set "ALLROADS_ACCESS_STATE=PRO"
echo 1. Connectez le PC et le telephone au meme Wi-Fi.
echo 2. Autorisez Python dans le pare-feu Windows si Windows le demande.
echo 3. Sur le telephone, ouvrez l'adresse affichee ci-dessous.
echo.
for /f "tokens=2 delims=:" %%A in ('ipconfig ^| findstr /c:"IPv4"') do (
  for /f "tokens=*" %%B in ("%%A") do (
    echo    http://%%B:8000/app
  )
)
echo.
echo Si plusieurs adresses apparaissent, essayez celle du reseau Wi-Fi.
echo.
echo Console PC : http://localhost:8000/test-console
echo.
echo Pour arreter la demo : fermez cette fenetre ou faites Ctrl+C.
echo.
if exist ".venv\Scripts\python.exe" (
  ".venv\Scripts\python.exe" -m uvicorn api.main:app --host 0.0.0.0 --port 8000
) else (
  python -m uvicorn api.main:app --host 0.0.0.0 --port 8000
)
pause
