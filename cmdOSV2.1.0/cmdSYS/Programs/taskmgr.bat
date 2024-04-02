@echo off
:taskmgr
setlocal EnableDelayedExpansion
cls
echo ==========================================
echo             Task Manager (Terminates by PID - Process Identification.)
echo ==========================================
tasklist /fo table /nh

echo.
set /p choice=Enter PID to end process (X to exit): 
if /i "%choice%"=="X" (
    exit /b
)

set "pidExists="
for /f "tokens=2 delims=," %%a in ('tasklist /fo csv /nh') do (
    if "%%~a"=="%choice%" (
        set "pidExists=1"
    )
)
if defined pidExists (
    taskkill /F /PID %choice%
    pause
    goto taskmgr
) else (
    echo.
    echo Process with PID %choice% does not exist.
    pause
    goto taskmgr
)