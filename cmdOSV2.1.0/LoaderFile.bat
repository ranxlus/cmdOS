@echo off
title cmdOS
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
cls
if not exist "cmdSYS\System\OScmd__INIT__.cOS" (
cls
title CODE: CRITICAL FILE UNLOCATED
echo [31mcmdOS has encountered a error.[0m
echo CODE: CRITICAL FILE UNLOCATED
pause >nul
cls
(
ECHO ___ 
) > cmdSYS\System\DMP\LOG_%random%%random%%random%.dmp
    powershell -c "(New-Object Media.SoundPlayer 'cmdSYS\System\sfx\cmdOSerror.wav').PlaySync();"
    goto exitp
) else (
    echo SYS-PASS SUCEEDED!
    echo --------------------
    echo [31mPlease don't crack this Version, if you have cmdOS you should have an ID Key. If not, contact ranxlus on Discord.[0m
    timeout 5 > nul
    goto tester
)

:tester
cls
title cmdOS
for /f "tokens=2*" %%a in ('reg query "HKEY_CURRENT_USER\Software\cmdOS" /v "Username" ^| findstr "Username"') do set "savedname=%%b"
reg query "HKEY_CURRENT_USER\Software\cmdOS" /v "Registered" >nul 2>&1
if errorlevel 1 (
    reg add "HKEY_CURRENT_USER\Software\cmdOS" /v "Registered" /t REG_DWORD /d 0 /f
    call cmdSYS\System\systemprograms\oobe.bat
    ) else ( 
        for /f "tokens=3" %%a in ('reg query "HKEY_CURRENT_USER\Software\cmdOS" /v "Registered" ^| findstr /i "Registered"') do (
             if %%a equ 1 (
                    goto Bootingup
                ) else ( 
                    call cmdSYS\System\systemprograms\oobe.bat
             ) 
       ) 
)

:Bootingup
cls
echo RAM: 250MB
echo CPU: Ryzen 2000
echo HDD: 1GB
echo GPU: Internal Graphics
echo Operating System: cmdOSV2 (Codename: OT)
echo Resolution: 640x480
echo Sound: PCK3FDS
echo Network: Wireless NET Technologys
echo USB Ports: 4
timeout 3 >nul
cls
if "%autoexec%"=="1" (
    call cmdSYS\autoexec.bat
)
cls
echo Welcome.
powershell -c "(New-Object Media.SoundPlayer 'cmdSYS\System\sfx\cmdOSstartup.wav').PlaySync();"
:Boot
cls
echo Welcome to cmdOSV2, %savedname% :D
echo.
echo 1 Settings
echo 2 Power Options
echo 3 Programs
set /p UserInput=Input: 
if "%UserInput%"=="1" goto Setting
if "%UserInput%"=="2" goto PowerOption
if "%UserInput%"=="3" goto Programs
else ( 
    cls
    goto Boot 
)

:Programs
cls
echo 1 DOS
echo 2 Music Player
echo 3 Task Manager
echo 4 Desktop
set /p UserInput=Input: 
if "%UserInput%"=="1" goto DOS
if "%UserInput%"=="2" goto Musicplyr
if "%UserInput%"=="3" goto taskmgr
if "%UserInput%"=="4" goto Boot
else (
    cls
    goto Programs
)

:Musicplyr
cls
call cmdSYS\Programs\Player.bat
goto Boot

:DOS
cls
call cmdSYS\System\systemprograms\DOS.bat
goto Boot

:Setting
cls
echo 1 De-Register cmdOS
echo 2 Go back to Desktop
echo 3 Change Name
echo 4 Edit Config
set /p UserInput=Input: 
if "%UserInput%"=="1" goto dever
if "%UserInput%"=="2" goto Boot
if "%UserInput%"=="3" goto NameChanger
if "%UserInput%"=="4" goto Config
else (
    cls
    goto Setting
)

:Config
start notepad "cmdSYS\config.cOS"
goto Setting

:dever
cls
reg delete HKEY_CURRENT_USER\Software\cmdOS /v Username /f
cls
reg add "HKEY_CURRENT_USER\Software\cmdOS" /v "Registered" /t REG_DWORD /d 0 /f
cls
goto exitp

:NameChanger
cls
echo Enter Name (NO SPACES!):
set /p username=
reg add HKEY_CURRENT_USER\Software\cmdOS /v Username /t REG_SZ /d %username% /f
for /f "tokens=2*" %%a in ('reg query HKEY_CURRENT_USER\Software\cmdOS /v Username ^| findstr Username') do set "savedname=%%b"
cls
goto Setting

:taskmgr
call cmdSYS\Programs\taskmgr.bat
goto Boot

:PowerOption
cls
echo 1 Shutdown
echo 2 Reboot
echo 3 Go back to Desktop
set /p UserInput=Input: 
if "%UserInput%"=="1" goto exitp
if "%UserInput%"=="2" goto rebootos
if "%UserInput%"=="3" goto Boot
else (
    cls
    goto PowerOption
)

:exitp
powershell -c "(New-Object Media.SoundPlayer 'cmdSYS\System\sfx\cmdOSshutdown.wav').PlaySync();"
cls
exit

:rebootos
start "" "%0"
exit