@echo off
REM Python ExamDiff Pro - Quick Launcher
REM This batch file provides easy access to common operations

:menu
cls
echo ================================================
echo   PYTHON EXAMDIFF PRO - Quick Launcher
echo ================================================
echo.
echo 1. Launch GUI
echo 2. Compare Two Files
echo 3. Compare Two Directories
echo 4. Run Tests
echo 5. Install Dependencies
echo 6. Generate HTML Report
echo 7. View Help
echo 8. Exit
echo.
set /p choice="Enter your choice (1-8): "

if "%choice%"=="1" goto gui
if "%choice%"=="2" goto files
if "%choice%"=="3" goto dirs
if "%choice%"=="4" goto tests
if "%choice%"=="5" goto install
if "%choice%"=="6" goto report
if "%choice%"=="7" goto help
if "%choice%"=="8" goto exit
goto menu

:gui
echo.
echo Launching GUI...
py -3 main.py
pause
goto menu

:files
echo.
set /p file1="Enter first file path: "
set /p file2="Enter second file path: "
echo.
echo Comparing files...
py -3 main.py "%file1%" "%file2%"
pause
goto menu

:dirs
echo.
set /p dir1="Enter first directory path: "
set /p dir2="Enter second directory path: "
echo.
echo Comparing directories...
py -3 main.py --dir "%dir1%" "%dir2%"
pause
goto menu

:tests
echo.
echo Running tests...
py -3 -m pytest tests/ -v
pause
goto menu

:install
echo.
echo Installing dependencies...
py -3 -m pip install -r requirements.txt
echo.
echo Installation complete!
pause
goto menu

:report
echo.
set /p file1="Enter first file path: "
set /p file2="Enter second file path: "
set /p output="Enter output HTML file name: "
echo.
echo Generating report...
py -3 main.py "%file1%" "%file2%" --html --output "%output%" --no-gui
echo.
echo Report generated: %output%
pause
goto menu

:help
echo.
py -3 main.py --help
echo.
pause
goto menu

:exit
echo.
echo Thank you for using Python ExamDiff Pro!
exit /b 0
