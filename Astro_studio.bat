@echo off
title Astro Studio

echo ==========================
echo      Astro Studio
echo ==========================
echo.

cd /d %~dp0

echo Lancement...

python -m streamlit run app.py

pause