#!/usr/bin/env python3
"""
Capture screenshots from slides.html and demo pages
"""

import os
import time
import asyncio
from pathlib import Path

# Try playwright first, fall back to selenium
try:
    from playwright.async_api import async_playwright
    USE_PLAYWRIGHT = True
except ImportError:
    USE_PLAYWRIGHT = False
    print("⚠️ Playwright not available, using Selenium instead")
    from selenium import webdriver
    from selenium.webdriver.chrome.service import Service
    from selenium.webdriver.chrome.options import Options
    from webdriver_manager.chrome import ChromeDriverManager

async def capture_with_playwright():
    """Capture screenshots using Playwright"""

    print("🎬 Using Playwright for screenshots...")

    async with async_playwright() as p:
        browser = await p.chromium.launch(headless=True)
        page = await browser.new_page(viewport={'width': 1920, 'height': 1080})

        # Get the full path to slides.html
        slides_path = Path(__file__).parent / "slides.html"
        slides_url = f"file:///{slides_path.as_posix()}"

        screenshots = []

        # Capture slides
        print("\n📸 Capturing slides...")
        await page.goto(slides_url)
        await page.wait_for_timeout(2000)

        # Navigate through slides and capture each one
        slide_count = 20  # We have 20 slides
        for i in range(slide_count):
            print(f"   Slide {i+1}/{slide_count}...")

            # Take screenshot
            filename = f"slide_{i+1:02d}.png"
            await page.screenshot(path=filename, full_page=False)
            screenshots.append(filename)

            # Go to next slide (simulate right arrow key)
            if i < slide_count - 1:
                await page.keyboard.press('ArrowRight')
                await page.wait_for_timeout(500)

        # Capture live demo pages if available
        print("\n📸 Capturing demo pages...")
        demo_urls = [
            {
                "url": "https://teslasolar.github.io/qdrant/",
                "name": "main_dashboard.png",
                "wait": 3000
            },
            {
                "url": "https://teslasolar.github.io/qdrant/screens/scada.html",
                "name": "scada_interface.png",
                "wait": 3000
            },
            {
                "url": "https://github.com/teslasolar/qdrant",
                "name": "github_repo.png",
                "wait": 2000
            }
        ]

        for demo in demo_urls:
            try:
                print(f"   Capturing {demo['name']}...")
                await page.goto(demo['url'])
                await page.wait_for_timeout(demo['wait'])
                await page.screenshot(path=demo['name'])
                screenshots.append(demo['name'])
            except Exception as e:
                print(f"   ⚠️ Could not capture {demo['name']}: {e}")

        await browser.close()
        return screenshots

def capture_with_selenium():
    """Capture screenshots using Selenium"""

    print("🎬 Using Selenium for screenshots...")

    # Setup Chrome options
    chrome_options = Options()
    chrome_options.add_argument("--headless")
    chrome_options.add_argument("--no-sandbox")
    chrome_options.add_argument("--disable-dev-shm-usage")
    chrome_options.add_argument("--window-size=1920,1080")

    # Setup driver
    try:
        service = Service(ChromeDriverManager().install())
        driver = webdriver.Chrome(service=service, options=chrome_options)
    except Exception as e:
        print(f"❌ Error setting up Chrome driver: {e}")
        print("   Please install Chrome or Chromium browser")
        return []

    screenshots = []

    try:
        # Get the full path to slides.html
        slides_path = Path(__file__).parent / "slides.html"
        slides_url = f"file:///{slides_path.as_posix()}"

        # Capture slides
        print("\n📸 Capturing slides...")
        driver.get(slides_url)
        time.sleep(2)

        # Take initial screenshot
        for i in range(20):  # 20 slides
            print(f"   Slide {i+1}/20...")
            filename = f"slide_{i+1:02d}.png"
            driver.save_screenshot(filename)
            screenshots.append(filename)

            # Click next button or simulate arrow key
            if i < 19:
                try:
                    # Try to find and click the next button
                    next_btn = driver.find_element("id", "nextBtn")
                    next_btn.click()
                except:
                    # If button not found, try JavaScript
                    driver.execute_script("changeSlide(1)")
                time.sleep(0.5)

        # Capture demo pages
        print("\n📸 Capturing demo pages...")
        demo_urls = [
            ("https://teslasolar.github.io/qdrant/", "main_dashboard.png", 3),
            ("https://github.com/teslasolar/qdrant", "github_repo.png", 2)
        ]

        for url, filename, wait in demo_urls:
            try:
                print(f"   Capturing {filename}...")
                driver.get(url)
                time.sleep(wait)
                driver.save_screenshot(filename)
                screenshots.append(filename)
            except Exception as e:
                print(f"   ⚠️ Could not capture {filename}: {e}")

    finally:
        driver.quit()

    return screenshots

def create_title_cards():
    """Create simple title cards using PIL"""

    print("\n🎨 Creating title cards...")

    from PIL import Image, ImageDraw, ImageFont

    cards = [
        {
            "filename": "title_card.png",
            "text": "CHAZON\nMEDICAL IMAGING",
            "subtitle": "AI-Powered Medical Case Matching"
        },
        {
            "filename": "problem_card.png",
            "text": "THE PROBLEM",
            "subtitle": "Hours to find similar cases"
        },
        {
            "filename": "solution_card.png",
            "text": "THE SOLUTION",
            "subtitle": "Qdrant Vector Search"
        },
        {
            "filename": "results_card.png",
            "text": "92% ACCURACY",
            "subtitle": "< 100ms search time"
        },
        {
            "filename": "cta_card.png",
            "text": "TRY IT NOW",
            "subtitle": "github.com/teslasolar/qdrant"
        }
    ]

    created_cards = []

    for card in cards:
        # Create image
        img = Image.new('RGB', (1920, 1080), color=(10, 14, 39))  # Dark blue background
        draw = ImageDraw.Draw(img)

        # Try to use a font, fall back to default
        try:
            title_font = ImageFont.truetype("arial.ttf", 120)
            subtitle_font = ImageFont.truetype("arial.ttf", 60)
        except:
            # Use default font if Arial not available
            title_font = ImageFont.load_default()
            subtitle_font = ImageFont.load_default()

        # Draw text (centered)
        # Title
        title_bbox = draw.textbbox((0, 0), card["text"], font=title_font)
        title_width = title_bbox[2] - title_bbox[0]
        title_height = title_bbox[3] - title_bbox[1]
        title_x = (1920 - title_width) // 2
        title_y = (1080 - title_height) // 2 - 100

        draw.text((title_x, title_y), card["text"], fill=(0, 255, 136), font=title_font, align="center")

        # Subtitle
        if card["subtitle"]:
            subtitle_bbox = draw.textbbox((0, 0), card["subtitle"], font=subtitle_font)
            subtitle_width = subtitle_bbox[2] - subtitle_bbox[0]
            subtitle_x = (1920 - subtitle_width) // 2
            subtitle_y = title_y + title_height + 50

            draw.text((subtitle_x, subtitle_y), card["subtitle"], fill=(0, 204, 255), font=subtitle_font)

        # Save
        img.save(card["filename"])
        created_cards.append(card["filename"])
        print(f"   ✅ Created: {card['filename']}")

    return created_cards

def main():
    """Main function"""

    print("=" * 60)
    print("CHAZON MEDICAL IMAGING - SCREENSHOT CAPTURE")
    print("=" * 60)

    screenshots = []

    # Try to create title cards first
    try:
        title_cards = create_title_cards()
        screenshots.extend(title_cards)
    except Exception as e:
        print(f"⚠️ Could not create title cards: {e}")

    # Capture screenshots
    if USE_PLAYWRIGHT:
        # Use playwright (async)
        loop = asyncio.new_event_loop()
        asyncio.set_event_loop(loop)
        captured = loop.run_until_complete(capture_with_playwright())
        screenshots.extend(captured)
    else:
        # Use selenium (sync)
        captured = capture_with_selenium()
        screenshots.extend(captured)

    print("\n" + "=" * 60)
    print(f"✅ Screenshot capture complete!")
    print(f"\n📊 Summary:")
    print(f"   Total screenshots: {len(screenshots)}")
    print(f"   Files created: {', '.join(screenshots[:5])}...")

    # Create a file list for the video creator
    with open("screenshot_list.txt", "w") as f:
        for screenshot in screenshots:
            f.write(f"{screenshot}\n")

    print(f"   List saved to: screenshot_list.txt")
    print("\nNext step: Run python create_video.py")
    print("=" * 60)

if __name__ == "__main__":
    main()