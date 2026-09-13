rem Référence historique J235 : V52.9.235 ; v=52.9.235&launch=test-terrain-realisable
@echo off
setlocal EnableExtensions EnableDelayedExpansion
chcp 65001 >nul
cd /d "%~dp0"
title JEPALYS J240 - V1 VIRAGE SERRE - TEST GLOBAL
cls
rem J226 - nettoyage fantomes camera : autorite unique Leaflet, sans prototype/masque.
rem Le verrou commercial par defaut reste TEST (Voiture + Bus) hors de ce lanceur.
set "ALLROADS_ACCESS_STATE=PRO"
set "ENVIRONMENT=development"
echo ==============================================================
echo       JEPALYS J240 - V1 VIRAGE SERRE - TEST GLOBAL
echo ==============================================================
echo.
echo Verification du port 8000...
powershell -NoProfile -ExecutionPolicy Bypass -Command "$c=Get-NetTCPConnection -LocalPort 8000 -State Listen -ErrorAction SilentlyContinue; if($c){$pid0=$c[0].OwningProcess; $p=Get-CimInstance Win32_Process -Filter ('ProcessId='+$pid0) -ErrorAction SilentlyContinue; if($p -and $p.CommandLine -match 'uvicorn.+main:app'){Write-Host ('Ancien serveur JEPALYS detecte PID '+$pid0+' : arret propre.'); Stop-Process -Id $pid0 -Force; Start-Sleep -Milliseconds 700; exit 0}else{Write-Host ('ERREUR : port 8000 utilise par un autre programme PID '+$pid0); exit 2}}"
if errorlevel 2 (
  echo.
  echo JEPALYS N'A PAS DEMARRE.
  pause
  exit /b 2
)

echo.
echo Recherche ADB et selection du WP35...
set "ADB="
where adb >nul 2>nul && set "ADB=adb"
if not defined ADB if exist "%USERPROFILE%\Downloads\scrcpy-win64-v4.1\scrcpy-win64-v4.1\adb.exe" set "ADB=%USERPROFILE%\Downloads\scrcpy-win64-v4.1\scrcpy-win64-v4.1\adb.exe"
set "ADB_SERIAL="
if defined ADB (
  for /f "tokens=1,2" %%A in ('"%ADB%" devices 2^>nul') do (
    if "%%B"=="device" echo %%A| findstr /R "^[0-9][0-9]*\.[0-9][0-9]*\.[0-9][0-9]*\.[0-9][0-9]*:[0-9][0-9]*$" >nul && if not defined ADB_SERIAL set "ADB_SERIAL=%%A"
  )
  if not defined ADB_SERIAL for /f "tokens=1,2" %%A in ('"%ADB%" devices 2^>nul') do if "%%B"=="device" if not defined ADB_SERIAL set "ADB_SERIAL=%%A"
  if defined ADB_SERIAL (
    echo WP35 cible ADB : !ADB_SERIAL!
    "%ADB%" -s "!ADB_SERIAL!" reverse --remove tcp:8000 >nul 2>nul
    "%ADB%" -s "!ADB_SERIAL!" reverse tcp:8000 tcp:8000 >nul 2>nul
    if errorlevel 1 (
      echo ATTENTION : tunnel ADB non cree pour !ADB_SERIAL!.
    ) else (
      echo Tunnel WP35 OK : http://localhost:8000/app/
      start "" powershell -NoProfile -WindowStyle Hidden -Command "Start-Sleep -Seconds 4; try { $v=(Invoke-RestMethod -Uri 'http://127.0.0.1:8000/version' -TimeoutSec 3).version; if($v -eq 'V52.9.102'){ $url='http://localhost:8000/app/?v=52.9.240&launch=test-global-j240'; $pkgs=(& '%ADB%' -s '!ADB_SERIAL!' shell pm list packages 2>$null) -join [Environment]::NewLine; if($pkgs -match 'package:com.android.chrome'){ & '%ADB%' -s '!ADB_SERIAL!' shell am force-stop com.android.chrome | Out-Null; & '%ADB%' -s '!ADB_SERIAL!' shell am start -a android.intent.action.VIEW -d $url -p com.android.chrome | Out-Null } else { & '%ADB%' -s '!ADB_SERIAL!' shell am start -a android.intent.action.VIEW -d $url | Out-Null } } } catch {}"
    )
  ) else (
    echo ATTENTION : aucun appareil ADB actif. Ouvrez le debogage sans fil du WP35.
  )
) else (
  echo ATTENTION : adb.exe introuvable. Le serveur demarrera sans ouverture WP35 automatique.
)

echo.
echo Version moteur attendue : V52.9.102
echo JEPALYS J240 : test global accueil + conduite + POI + affichage auto
echo Verification : http://localhost:8000/version
echo.
cd api
python -m uvicorn main:app --host 0.0.0.0 --port 8000
pause
