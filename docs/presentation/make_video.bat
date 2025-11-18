@echo off
echo ========================================
echo CHAZON VIDEO GENERATOR
echo ========================================
echo.

echo Step 1: Installing dependencies...
python install_video_tools.py
if errorlevel 1 goto error

echo.
echo Step 2: Generating narration...
python generate_narration.py
if errorlevel 1 goto error

echo.
echo Step 3: Capturing screenshots...
python capture_screenshots.py
if errorlevel 1 goto error

echo.
echo Step 4: Creating video...
python create_video.py
if errorlevel 1 goto error

echo.
echo ========================================
echo SUCCESS! Video created: chazon_demo.mp4
echo ========================================
echo.
echo Next steps:
echo 1. Review chazon_demo.mp4
echo 2. Upload to YouTube (unlisted)
echo 3. Add link to hackathon submission
echo.
pause
goto end

:error
echo.
echo ERROR: Step failed!
echo Please check error messages above.
pause

:end