#!/usr/bin/env python3
"""
Create final video from screenshots and narration
"""

import os
import glob
from pathlib import Path
from moviepy.editor import *
from moviepy.video.fx import resize

def create_video():
    """Create video from screenshots and narration"""

    print("=" * 60)
    print("CHAZON MEDICAL IMAGING - VIDEO CREATOR")
    print("=" * 60)

    # Check for narration
    narration_files = glob.glob("narration*.mp3")
    if not narration_files:
        print("❌ No narration found! Run generate_narration.py first")
        return False

    # Check for screenshots
    slide_files = sorted(glob.glob("slide_*.png"))
    if not slide_files:
        print("❌ No screenshots found! Run capture_screenshots.py first")
        return False

    print(f"\n📊 Found assets:")
    print(f"   Narration files: {len(narration_files)}")
    print(f"   Screenshot files: {len(slide_files)}")

    # Load narration
    if len(narration_files) == 1:
        # Single narration file
        print("\n🎵 Loading narration...")
        audio = AudioFileClip(narration_files[0])
        total_duration = audio.duration
        print(f"   Duration: {total_duration:.1f} seconds")
    else:
        # Multiple narration segments
        print("\n🎵 Loading narration segments...")
        audio_clips = []
        for nf in sorted(narration_files):
            if "narration_" in nf:  # Only numbered segments
                audio_clips.append(AudioFileClip(nf))

        if audio_clips:
            audio = concatenate_audioclips(audio_clips)
            total_duration = audio.duration
        else:
            audio = AudioFileClip(narration_files[0])
            total_duration = audio.duration

        print(f"   Total duration: {total_duration:.1f} seconds")

    # Create video timeline
    print("\n🎬 Creating video timeline...")

    # Define the video structure (60 seconds)
    timeline = [
        # Opening title (0-5s)
        {"type": "title", "duration": 5, "file": "title_card.png"},

        # Problem slides (5-15s)
        {"type": "slides", "duration": 10, "files": ["slide_01.png", "slide_02.png"]},

        # Solution demo (15-35s)
        {"type": "demo", "duration": 20, "files": ["slide_03.png", "slide_04.png", "main_dashboard.png"]},

        # Architecture (35-45s)
        {"type": "architecture", "duration": 10, "files": ["slide_05.png", "slide_06.png"]},

        # Results (45-55s)
        {"type": "results", "duration": 10, "files": ["slide_07.png", "slide_08.png"]},

        # Call to action (55-60s)
        {"type": "cta", "duration": 5, "files": ["slide_19.png", "slide_20.png", "github_repo.png"]}
    ]

    # Build video clips
    video_clips = []
    current_time = 0

    for section in timeline:
        print(f"\n   Section: {section['type']} ({section['duration']}s)")

        # Get files for this section
        section_files = []
        for f in section.get('files', [section.get('file', '')]):
            if os.path.exists(f):
                section_files.append(f)
            else:
                # Try to find alternative files
                if "slide_" in f:
                    # Use any available slide
                    alternatives = glob.glob("slide_*.png")
                    if alternatives:
                        section_files.append(alternatives[0])
                        print(f"      Using alternative: {alternatives[0]}")

        if not section_files:
            # Create a text clip if no images available
            print(f"      Creating text clip for {section['type']}")
            clip = TextClip(
                section['type'].upper(),
                fontsize=70,
                color='white',
                bg_color='black',
                size=(1920, 1080),
                method='caption'
            ).set_duration(section['duration'])
        else:
            # Calculate duration per file
            duration_per_file = section['duration'] / len(section_files)

            for file in section_files:
                print(f"      Adding: {file} ({duration_per_file:.1f}s)")

                # Load image
                img_clip = ImageClip(file).set_duration(duration_per_file)

                # Ensure correct size
                img_clip = img_clip.resize((1920, 1080))

                # Add fade in/out for smooth transitions
                if duration_per_file > 1:
                    img_clip = img_clip.crossfadein(0.3).crossfadeout(0.3)

                video_clips.append(img_clip)

        current_time += section['duration']

    # Concatenate all clips
    print("\n🎞️ Concatenating clips...")
    if video_clips:
        final_video = concatenate_videoclips(video_clips, method="compose")
    else:
        # Fallback: create simple slideshow
        print("⚠️ Using fallback slideshow method...")

        if slide_files:
            clips = []
            duration_per_slide = 60 / len(slide_files)  # Distribute 60 seconds

            for slide in slide_files[:20]:  # Max 20 slides
                clip = ImageClip(slide).set_duration(duration_per_slide)
                clip = clip.resize((1920, 1080))
                clips.append(clip)

            final_video = concatenate_videoclips(clips)
        else:
            print("❌ No slides available for video!")
            return False

    # Add audio
    print("\n🎵 Adding audio track...")
    final_video = final_video.set_audio(audio)

    # Adjust video length to match audio
    if final_video.duration > total_duration:
        final_video = final_video.subclip(0, total_duration)
    elif final_video.duration < total_duration:
        # Extend last frame
        last_frame = final_video.get_frame(final_video.duration - 0.1)
        extension = ImageClip(last_frame).set_duration(total_duration - final_video.duration)
        final_video = concatenate_videoclips([final_video, extension])

    # Export video
    output_file = "chazon_demo.mp4"
    print(f"\n💾 Exporting video to {output_file}...")
    print("   This may take a few minutes...")

    try:
        final_video.write_videofile(
            output_file,
            fps=30,
            codec='libx264',
            audio_codec='aac',
            temp_audiofile='temp-audio.m4a',
            remove_temp=True,
            preset='medium',  # Balance between speed and quality
            threads=4
        )

        print(f"\n✅ Video created successfully!")
        print(f"   Output: {output_file}")
        print(f"   Size: {os.path.getsize(output_file) / 1024 / 1024:.1f} MB")
        print(f"   Duration: {final_video.duration:.1f} seconds")

        return True

    except Exception as e:
        print(f"\n❌ Error creating video: {e}")
        print("\nTroubleshooting:")
        print("1. Install ffmpeg: https://ffmpeg.org/download.html")
        print("2. Try simpler export settings")
        print("3. Check that all image files exist")

        # Try simpler export
        try:
            print("\n🔄 Trying simpler export settings...")
            final_video.write_videofile(
                output_file,
                fps=24,
                codec='mpeg4',
                audio_codec='mp3',
                preset='ultrafast'
            )
            print("✅ Video created with basic settings!")
            return True
        except Exception as e2:
            print(f"❌ Simple export also failed: {e2}")
            return False

def create_simple_slideshow():
    """Create a simple slideshow as fallback"""

    print("\n🎬 Creating simple slideshow...")

    slides = sorted(glob.glob("slide_*.png"))
    if not slides:
        print("❌ No slides found!")
        return False

    clips = []
    for slide in slides:
        clip = ImageClip(slide).set_duration(3)  # 3 seconds per slide
        clips.append(clip)

    video = concatenate_videoclips(clips)

    # Add audio if available
    if os.path.exists("narration.mp3"):
        audio = AudioFileClip("narration.mp3")
        video = video.set_audio(audio)

    video.write_videofile("chazon_slideshow.mp4", fps=24)
    print("✅ Slideshow created: chazon_slideshow.mp4")
    return True

def main():
    """Main function"""

    # Try to create full video
    success = create_video()

    if not success:
        print("\n🔄 Trying simple slideshow instead...")
        success = create_simple_slideshow()

    if success:
        print("\n" + "=" * 60)
        print("🎉 SUCCESS! Video is ready for submission!")
        print("\nNext steps:")
        print("1. Review the video: chazon_demo.mp4")
        print("2. Upload to YouTube as unlisted")
        print("3. Add link to your hackathon submission")
        print("=" * 60)
    else:
        print("\n" + "=" * 60)
        print("⚠️ Video creation had issues.")
        print("\nManual fallback:")
        print("1. Use any screen recorder")
        print("2. Open slides.html in browser")
        print("3. Record while clicking through slides")
        print("4. Add narration.mp3 in video editor")
        print("=" * 60)

if __name__ == "__main__":
    main()