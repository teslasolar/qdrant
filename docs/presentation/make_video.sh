#!/bin/bash

echo "========================================"
echo "CHAZON VIDEO GENERATOR"
echo "========================================"
echo ""

echo "Step 1: Installing dependencies..."
python3 install_video_tools.py
if [ $? -ne 0 ]; then
    echo "ERROR: Installation failed!"
    exit 1
fi

echo ""
echo "Step 2: Generating narration..."
python3 generate_narration.py
if [ $? -ne 0 ]; then
    echo "ERROR: Narration generation failed!"
    exit 1
fi

echo ""
echo "Step 3: Capturing screenshots..."
python3 capture_screenshots.py
if [ $? -ne 0 ]; then
    echo "ERROR: Screenshot capture failed!"
    exit 1
fi

echo ""
echo "Step 4: Creating video..."
python3 create_video.py
if [ $? -ne 0 ]; then
    echo "ERROR: Video creation failed!"
    exit 1
fi

echo ""
echo "========================================"
echo "SUCCESS! Video created: chazon_demo.mp4"
echo "========================================"
echo ""
echo "Next steps:"
echo "1. Review chazon_demo.mp4"
echo "2. Upload to YouTube (unlisted)"
echo "3. Add link to hackathon submission"
echo ""