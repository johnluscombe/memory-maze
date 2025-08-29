@ECHO OFF

rem Get start time
for /F "tokens=1-4 delims=:.," %%a in ("%time%") do (
   set /A "start=(((%%a*60)+1%%b %% 100)*60+1%%c %% 100)*100+1%%d %% 100"
)

rem Create (if not already created) and activate virtual environment for PyInstaller
if exist venv (
    echo Found Python virtual environment!
) else (
    echo Python virtual environment not found. Creating...
    python -m venv venv
)

rem Install PyInstaller if not already installed
if exist venv\Scripts\pyinstaller.exe (
    echo Found PyInstaller!
) else (
    echo PyInstaller not found. Installing...
    venv\Scripts\pip.exe install pyinstaller
)

rem Build
echo Building...
venv\Scripts\pyinstaller.exe memory-maze.spec -y
tar  -C dist/memory-maze -a -c -f dist/memory-maze.zip *

rem Get end time
for /F "tokens=1-4 delims=:.," %%a in ("%time%") do (
   set /A "end=(((%%a*60)+1%%b %% 100)*60+1%%c %% 100)*100+1%%d %% 100"
)

rem Get build time
set /A build_time=end-start

rem Show build time
set /A build_time_seconds=build_time/100
echo Build time: %build_time_seconds%s
