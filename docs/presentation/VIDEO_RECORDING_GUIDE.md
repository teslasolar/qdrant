# 📹 Video Recording Guide

## Important Note
I cannot create actual video files - you'll need to record this yourself. Here's how:

## What You Have

1. **Video Script**: `VIDEO_SCRIPT_UPDATED.md` - Complete 60-second script with narration and visual cues
2. **HTML Slides**: `slides.html` - Professional presentation slides (just created!)
3. **Live Demo**: Your working application at https://teslasolar.github.io/qdrant/

## How to Record the Video

### Option 1: Screen Recording Tools (Recommended)

#### Windows
- **OBS Studio** (Free) - https://obsproject.com/
- **Windows Game Bar** (Built-in) - Press Win+G
- **Camtasia** (Paid, has free trial)

#### Mac
- **QuickTime** (Built-in) - File → New Screen Recording
- **OBS Studio** (Free)
- **ScreenFlow** (Paid)

#### Cross-Platform Web Tools
- **Loom** (Free plan available) - https://www.loom.com/
- **Screencastify** (Chrome extension)
- **RecordCast** - https://www.recordcast.com/

### Option 2: PowerPoint Video (If you prefer PowerPoint)

1. **Convert HTML Slides to PowerPoint:**
   - Open `slides.html` in your browser
   - Press F11 for fullscreen
   - Take screenshots of each slide (Print Screen)
   - Insert into PowerPoint slides
   - OR use an online converter like https://www.ilovepdf.com/html_to_pdf then PDF to PPT

2. **Record in PowerPoint:**
   - Go to Slide Show → Record Slide Show
   - Record your narration for each slide
   - Export as video (File → Export → Create a Video)

### Recording Steps

1. **Preparation:**
   - Have `slides.html` open in one browser tab
   - Have your live demo (index.html) in another tab
   - Open terminal with backend running
   - Test your microphone

2. **Recording Flow (60 seconds):**
   ```
   0:00-0:05 - Show title slide + introduce problem
   0:05-0:20 - Demo medical image upload and search
   0:20-0:40 - Show Qdrant integration (backend terminal)
   0:40-0:50 - Highlight unique ISA-95 architecture
   0:50-1:00 - Results & call to action
   ```

3. **Key Scenes to Capture:**
   - Medical dashboard with X-ray images
   - Qdrant search returning similar cases
   - Terminal showing embedding generation
   - Architecture diagram (from slides)
   - GitHub repository

### Audio Recording Tips

If you want to record audio separately:
- **Audacity** (Free) - https://www.audacityteam.org/
- Record narration following the script
- Combine with screen recording in video editor

### Video Editing (Optional)

Free editors to combine/edit clips:
- **DaVinci Resolve** - Professional free editor
- **OpenShot** - Simple and free
- **Windows Video Editor** - Built into Windows
- **iMovie** - Built into Mac

### Export Settings
- Format: MP4 (H.264)
- Resolution: 1920x1080 (1080p) or 1280x720 (720p)
- Frame rate: 30fps
- Duration: 60 seconds exactly
- File size: Keep under 100MB

### Upload Options
1. **YouTube** (Recommended)
   - Create unlisted video
   - Copy share link

2. **Vimeo**
   - Free account available
   - Professional appearance

3. **Google Drive**
   - Upload MP4
   - Get shareable link

4. **Loom**
   - Records and hosts in one tool

## Quick Alternative: Slides-Only Video

If you're short on time, you can create a simple video using just the slides:

1. Open `slides.html` in fullscreen (F11)
2. Use OBS or screen recorder
3. Navigate through slides while narrating
4. Follow the script timing
5. Export and upload

## Sample Narration Text

Here's the key narration for easy reading:

```
"What if doctors could instantly find similar medical cases using AI-powered vector search?
Meet Chazon - where medical imaging meets industrial automation.

[Show demo]
Watch as we upload a chest X-ray and search for similar cases.
Using BiomedCLIP embeddings and Qdrant vector search, we find matching
pneumonia cases in under 100 milliseconds with 92% accuracy.

[Show architecture]
Unlike typical medical apps, Chazon uses industrial ISA-95 standards
for enterprise-grade reliability. Full DICOM compliance, HIPAA ready,
and our AlF-DETECT algorithm for early disease detection.

[Call to action]
Chazon - Industrial-grade medical imaging with AI-powered search.
Open source, MIT licensed, deploy in 5 minutes.
Try it now at teslasolar.github.io/qdrant."
```

## Checklist Before Submitting

- [ ] Video is exactly 60 seconds
- [ ] Shows real Qdrant integration
- [ ] Demonstrates medical image search
- [ ] Clear audio (no background noise)
- [ ] Uploaded and link works
- [ ] Added link to submission

## Need Help?

The video is the only missing piece for submission! You have:
- ✅ Working code and demo
- ✅ Complete documentation
- ✅ Presentation slides
- ✅ Video script
- ❌ Just need to record the video

Good luck with the recording! 🎬🚀