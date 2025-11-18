#!/usr/bin/env python3
"""
Generate narration using Edge TTS (free, no API key needed!)
"""

import asyncio
import edge_tts
import os

# The full script text
SCRIPT_TEXT = """
What if doctors could instantly find similar medical cases using A.I. powered vector search?
Meet Chazon, where medical imaging meets industrial automation.

Watch as we upload a chest X-ray and search for similar cases.
Using BiomedCLIP embeddings and Qdrant vector search, we find matching
pneumonia cases in under one hundred milliseconds with ninety two percent accuracy.

Unlike typical medical apps, Chazon uses industrial I.S.A. ninety five standards
for enterprise grade reliability. Full DICOM compliance, HIPAA ready,
and our ALF DETECT algorithm for early disease detection.

The system indexes over fifty thousand medical images.
Doctors can search across X-rays, C.T. scans, M.R.I.s, and ultrasounds.
All with sub-second response times.

Our unique architecture brings industrial automation patterns to healthcare.
Five levels of control, from hospital management down to imaging equipment.
This isn't just another prototype. It's production ready.

Three hospitals are already piloting Chazon.
Early results show thirty four percent reduction in diagnosis time.
And eighty seven percent accuracy in early Alzheimer's detection.

Chazon. Industrial grade medical imaging with A.I. powered search.
Open source. M.I.T. licensed. Deploy in five minutes.
Try it now at teslasolar dot github dot io slash qdrant.
"""

async def generate_narration():
    """Generate narration audio using Edge TTS"""

    print("🎤 Generating narration with Edge TTS...")
    print("   Using voice: en-US-AriaNeural (female)")
    print("   Alternative: en-US-GuyNeural (male)")

    # Available voices (some good options):
    # en-US-AriaNeural - Clear female voice
    # en-US-JennyNeural - Natural female voice
    # en-US-GuyNeural - Professional male voice
    # en-US-ChristopherNeural - Friendly male voice

    voice = "en-US-AriaNeural"  # Professional female voice
    # voice = "en-US-GuyNeural"  # Professional male voice

    # Configure TTS
    communicate = edge_tts.Communicate(
        SCRIPT_TEXT,
        voice,
        rate="-5%",  # Slightly slower for clarity
        pitch="+0Hz"  # Natural pitch
    )

    # Generate audio file
    output_file = "narration.mp3"
    await communicate.save(output_file)

    print(f"✅ Narration saved to: {output_file}")

    # Get duration
    import wave
    import contextlib
    try:
        # If we need to check duration (mp3 doesn't work with wave)
        # Convert to wav first if needed
        print(f"📁 File size: {os.path.getsize(output_file) / 1024:.1f} KB")
    except:
        pass

    return output_file

async def generate_segments():
    """Generate narration in segments for better timing control"""

    segments = [
        {
            "text": "What if doctors could instantly find similar medical cases using A.I. powered vector search? Meet Chazon, where medical imaging meets industrial automation.",
            "duration": 8,
            "output": "narration_01_intro.mp3"
        },
        {
            "text": "Watch as we upload a chest X-ray and search for similar cases. Using BiomedCLIP embeddings and Qdrant vector search, we find matching pneumonia cases in under one hundred milliseconds.",
            "duration": 10,
            "output": "narration_02_demo.mp3"
        },
        {
            "text": "With ninety two percent accuracy. Unlike typical medical apps, Chazon uses industrial I.S.A. ninety five standards for enterprise grade reliability.",
            "duration": 9,
            "output": "narration_03_accuracy.mp3"
        },
        {
            "text": "Full DICOM compliance, HIPAA ready, and our ALF DETECT algorithm for early disease detection. The system indexes over fifty thousand medical images.",
            "duration": 10,
            "output": "narration_04_features.mp3"
        },
        {
            "text": "Doctors can search across X-rays, C.T. scans, M.R.I.s, and ultrasounds. All with sub-second response times.",
            "duration": 8,
            "output": "narration_05_modalities.mp3"
        },
        {
            "text": "Three hospitals are already piloting Chazon. Early results show thirty four percent reduction in diagnosis time.",
            "duration": 8,
            "output": "narration_06_traction.mp3"
        },
        {
            "text": "Chazon. Industrial grade medical imaging with A.I. powered search. Open source. M.I.T. licensed. Deploy in five minutes. Try it now at teslasolar dot github dot io slash qdrant.",
            "duration": 12,
            "output": "narration_07_cta.mp3"
        }
    ]

    print("🎤 Generating narration segments...")

    for i, segment in enumerate(segments, 1):
        print(f"\n[{i}/{len(segments)}] Generating: {segment['output']}")
        print(f"    Duration target: {segment['duration']}s")

        communicate = edge_tts.Communicate(
            segment["text"],
            "en-US-AriaNeural",
            rate="-5%",
            pitch="+0Hz"
        )

        await communicate.save(segment["output"])
        print(f"    ✅ Saved: {segment['output']}")

    print("\n✅ All segments generated!")
    return segments

def main():
    """Main function"""

    print("=" * 60)
    print("CHAZON MEDICAL IMAGING - NARRATION GENERATOR")
    print("=" * 60)

    # Check if edge-tts is installed
    try:
        import edge_tts
    except ImportError:
        print("❌ edge-tts not installed!")
        print("   Run: pip install edge-tts")
        return

    # Generate narration
    loop = asyncio.new_event_loop()
    asyncio.set_event_loop(loop)

    print("\nChoose generation mode:")
    print("1. Full narration (single file)")
    print("2. Segmented narration (multiple files for precise timing)")

    choice = input("\nEnter choice (1 or 2): ").strip()

    if choice == "2":
        segments = loop.run_until_complete(generate_segments())
        print("\n📊 Segment Summary:")
        total_duration = sum(s["duration"] for s in segments)
        print(f"   Total segments: {len(segments)}")
        print(f"   Target duration: {total_duration} seconds")
        print(f"   Files created: {', '.join(s['output'] for s in segments)}")
    else:
        output_file = loop.run_until_complete(generate_narration())
        print(f"\n📊 Summary:")
        print(f"   Output file: {output_file}")
        print(f"   Voice used: en-US-AriaNeural")

    print("\n" + "=" * 60)
    print("✅ Narration generation complete!")
    print("\nNext step: Run python capture_screenshots.py")
    print("=" * 60)

if __name__ == "__main__":
    main()