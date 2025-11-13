#!/usr/bin/env python3
"""
Download transcripts using Playwright
More robust than Selenium for sites with anti-bot protection
"""

import os
import asyncio
import time
from pathlib import Path
from playwright.async_api import async_playwright
from tqdm import tqdm

# Constants
SERIES_URL = "https://learner.org/series/economics-ua-21st-century-edition"
OUTPUT_DIR = "economics-spanish/original-transcripts"

async def download_transcripts():
    """Download all transcripts using Playwright"""
    print("Economics Transcript Downloader (Playwright)")
    print("=" * 60)

    os.makedirs(OUTPUT_DIR, exist_ok=True)

    async with async_playwright() as p:
        # Launch browser
        print("\nLaunching browser...")
        browser = await p.chromium.launch(
            headless=True,
            args=[
                '--no-sandbox',
                '--disable-setuid-sandbox',
                '--disable-dev-shm-usage',
                '--disable-blink-features=AutomationControlled',
                '--disable-web-security',
                '--disable-features=IsolateOrigins,site-per-process'
            ]
        )

        context = await browser.new_context(
            user_agent='Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36',
            ignore_https_errors=True
        )

        page = await context.new_page()

        # Navigate to series page
        print(f"Loading series page: {SERIES_URL}")
        try:
            await page.goto(SERIES_URL, wait_until='domcontentloaded', timeout=60000)
            print("✓ Page loaded")
        except Exception as e:
            print(f"✗ Error loading page: {e}")
            print("Trying without waiting for network idle...")
            try:
                await page.goto(SERIES_URL, timeout=60000)
                print("✓ Page loaded (basic)")
            except Exception as e2:
                print(f"✗ Still failed: {e2}")
                await browser.close()
                return

        # Wait a bit for dynamic content
        await page.wait_for_timeout(2000)

        # Save page content for debugging
        content = await page.content()
        with open('playwright_page_source.html', 'w', encoding='utf-8') as f:
            f.write(content)
        print("✓ Page source saved to playwright_page_source.html")

        # Try to find video links
        print("\nSearching for video links...")

        # Try multiple selectors
        video_links = []

        # Method 1: Find links with specific patterns
        all_links = await page.locator('a').all()
        print(f"Found {len(all_links)} total links on page")

        for link in all_links:
            try:
                href = await link.get_attribute('href')
                text = await link.inner_text()

                if href and ('courses' in href or 'video' in href or 'watch' in href):
                    # Make absolute URL
                    if href.startswith('/'):
                        href = f"https://learner.org{href}"

                    if href not in [v['url'] for v in video_links]:
                        video_links.append({
                            'title': text.strip()[:100],
                            'url': href
                        })
            except:
                continue

        if not video_links:
            print("⚠ No video links found automatically")
            print("Page structure may have changed. Check playwright_page_source.html")

            # Try to extract manually visible links for user
            print("\nAll links found on page:")
            for i, link in enumerate(all_links[:30], 1):  # Show first 30
                try:
                    href = await link.get_attribute('href')
                    text = await link.inner_text()
                    if href and text.strip():
                        print(f"  {i}. [{text.strip()[:50]}] -> {href}")
                except:
                    pass

            await browser.close()
            return

        print(f"\n✓ Found {len(video_links)} video links")
        for i, link in enumerate(video_links, 1):
            print(f"  {i}. {link['title']}")

        # Download transcripts
        print("\n" + "=" * 60)
        print("Downloading transcripts...")
        print("=" * 60)

        success_count = 0

        for i, video in enumerate(tqdm(video_links, desc="Progress"), 1):
            try:
                print(f"\n[{i}/{len(video_links)}] Processing: {video['title']}")
                print(f"  URL: {video['url']}")

                # Navigate to video page
                await page.goto(video['url'], wait_until='networkidle', timeout=30000)
                await page.wait_for_timeout(1000)

                # Look for transcript/PDF link
                pdf_links = await page.locator('a[href$=".pdf"]').all()

                if not pdf_links:
                    # Try finding by text content
                    transcript_links = await page.locator('a:has-text("transcript")').all()
                    transcript_links += await page.locator('a:has-text("Transcript")').all()
                    transcript_links += await page.locator('a:has-text("PDF")').all()

                    for link in transcript_links:
                        href = await link.get_attribute('href')
                        if href and '.pdf' in href.lower():
                            pdf_links.append(link)
                            break

                if not pdf_links:
                    print(f"  ✗ No transcript PDF found")
                    continue

                # Get PDF URL
                pdf_href = await pdf_links[0].get_attribute('href')
                if pdf_href.startswith('/'):
                    pdf_href = f"https://learner.org{pdf_href}"

                print(f"  Found PDF: {pdf_href}")

                # Download PDF
                async with page.expect_download() as download_info:
                    await pdf_links[0].click()

                download = await download_info.value

                # Save file
                safe_title = "".join(c for c in video['title'] if c.isalnum() or c in (' ', '-', '_')).strip()
                safe_title = safe_title.replace(' ', '-')[:50]
                filename = f"video-{i:02d}-{safe_title}.pdf"
                filepath = os.path.join(OUTPUT_DIR, filename)

                await download.save_as(filepath)
                print(f"  ✓ Saved: {filename}")
                success_count += 1

                # Be respectful - wait between requests
                await page.wait_for_timeout(2000)

            except Exception as e:
                print(f"  ✗ Error: {e}")
                continue

        # Summary
        print("\n" + "=" * 60)
        print("Download Complete!")
        print("=" * 60)
        print(f"Successfully downloaded: {success_count}/{len(video_links)} transcripts")
        print(f"Saved to: {OUTPUT_DIR}")

        await browser.close()

def main():
    asyncio.run(download_transcripts())

if __name__ == "__main__":
    main()
