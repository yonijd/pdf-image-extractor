@echo off
chcp 65001 >nul
title Extractor PDF Images - Menu

:MENU
cls
echo ========================================
echo    EXTRACTOR DE IMAGENES PDF
echo ========================================
echo.
echo   [1] Sin filtro
echo   [2] 100x100 px
echo   [3] 150x150 px
echo   [4] 200x200 px
echo   [5] 250x250 px
echo   [6] 300x300 px
echo   [7] 60 KB
echo   [8] 100 KB (predeterminado)
echo   [9] 150 KB
echo  [10] 200 KB
echo  [0] Salir
echo.
set /p opcion="Seleccione una opcion: "

if "%opcion%"=="0" exit
if "%opcion%"=="1" set FILTRO=1 & goto EJECUTAR
if "%opcion%"=="2" set FILTRO=2 & goto EJECUTAR
if "%opcion%"=="3" set FILTRO=3 & goto EJECUTAR
if "%opcion%"=="4" set FILTRO=4 & goto EJECUTAR
if "%opcion%"=="5" set FILTRO=5 & goto EJECUTAR
if "%opcion%"=="6" set FILTRO=6 & goto EJECUTAR
if "%opcion%"=="7" set FILTRO=7 & goto EJECUTAR
if "%opcion%"=="8" set FILTRO=8 & goto EJECUTAR
if "%opcion%"=="9" set FILTRO=9 & goto EJECUTAR
if "%opcion%"=="10" set FILTRO=10 & goto EJECUTAR

echo Opcion invalida
timeout /t 2 >nul
goto MENU

:EJECUTAR
cls
echo.
echo Ejecutando con filtro %FILTRO%...
echo.
powershell -Command "$file = 'extract_pdf_images.py'; (Get-Content $file) -replace 'FILTRO = \d+', 'FILTRO = %FILTRO%' | Set-Content $file; python $file"
echo.
echo Proceso completado
echo.
pause
goto MENU