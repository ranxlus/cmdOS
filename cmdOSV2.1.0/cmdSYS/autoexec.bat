@echo off
color
cls
echo This is a Simple AutoExec File. Edit it and make things happen on startup.
pause>nul
rem DONT EDIT BELOW THIS LINE
setlocal
for /F "tokens=1,* delims==" %%A in (cmdSYS\config.cOS) do (
    set "%%A=%%B"
)
if "%matrixtheme%"=="1" (
    color 2
) else if "%bsodtheme%"=="1" (
    color 1f
) else if "%nighttheme%"=="1" (
    color 9
) else (
    color
)
exit /b