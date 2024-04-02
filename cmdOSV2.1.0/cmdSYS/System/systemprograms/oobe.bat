@echo off
:Register
cls
echo Enter Product Verification ID
set /p UserInput=Verification ID: 
if "%UserInput%"=="CMD-SDRT3-OEM-U4KF3G" goto verify
if "%UserInput%"=="CMD-AFX9D-OEM-8DDSOE" goto verify
( 
    echo Invalid Verification ID!
    timeout /t 2 >nul
    goto Register
)

:verify
reg add "HKEY_CURRENT_USER\Software\cmdOS" /v "Registered" /t REG_DWORD /d 1 /f
cls
echo Enter Name (NO SPACES!):
set /p username=
reg add HKEY_CURRENT_USER\Software\cmdOS /v Username /t REG_SZ /d %username% /f
for /f "tokens=2*" %%a in ('reg query HKEY_CURRENT_USER\Software\cmdOS /v Username ^| findstr Username') do set "savedname=%%b"
cls
echo Good Name: %savedname%!
timeout 2 >nul
exit /b