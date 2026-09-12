@echo off
cd /d "%~dp0"
py -m pytest api\tests\test_chauffeur_block.py -q
pause
