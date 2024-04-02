:Music
cls
echo 1 Chilling
echo 2 Old School Bass
echo 3 To Desktop
set /p UserInput=Input: 
if "%UserInput%"=="1" goto num1
if "%UserInput%"=="2" goto num2
if "%UserInput%"=="3" exit /b
(
    cls 
    goto Music
)

:num1
cls
echo Now Playing Chilling.wav
powershell -c "(New-Object Media.SoundPlayer 'cmdSYS\Music\chilling.wav').PlaySync();"
exit /b

:num2
cls
echo Now Playing oldSchoolBass
powershell -c "(New-Object Media.SoundPlayer 'cmdSYS\Music\oldSchoolBass.wav').PlaySync();"
exit /b