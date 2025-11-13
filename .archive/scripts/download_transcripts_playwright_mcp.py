#!/usr/bin/env python3
"""
Download ALL Economics USA Transcripts using Playwright
Downloads both video and audio transcripts for all 28 episodes
"""

import os
import asyncio
from pathlib import Path
from playwright.async_api import async_playwright
import time

OUTPUT_DIR = "economics-spanish/original-transcripts"

# Known episode URLs from video_urls.py and web research
EPISODE_URLS = [
    "https://www.learner.org/series/economics-ua-21st-century-edition/resources-and-scarcity/",
    "https://www.learner.org/series/economics-ua-21st-century-edition/supply-and-demand/",
    "https://www.learner.org/series/economics-ua-21st-century-edition/economic-efficiency/",
    "https://www.learner.org/series/economics-ua-21st-century-edition/reducing-poverty/",
    "https://www.learner.org/series/economics-ua-21st-century-edition/federal-deficits/",
    "https://www.learner.org/series/economics-ua-21st-century-edition/international-trade/",
]

async def get_all_episode_urls(page):
    """Navigate to series page and extract all episode URLs"""
    print("Discovering all episode URLs from series page...")

    series_url = "https://www.learner.org/series/economics-ua-21st-century-edition/"

    try:
        await page.goto(series_url, wait_until="networkidle", timeout=30000)
        await asyncio.sleep(2)  # Let page fully load

        # Find all episode links (they typically have the series path in them)
        episode_links = await page.query_selector_all('a[href*="/series/economics-ua-21st-century-edition/"]')

        urls = set()
        for link in episode_links:
            href = await link.get_attribute('href')
            if href and href.endswith('/') and href != series_url:
                # Filter out series homepage, just get episode pages
                if href.count('/') >= 5:  # Episode URLs have more path segments
                    urls.add(href)

        urls_list = sorted(list(urls))
        print(f"[OK] Found {len(urls_list)} episode URLs")

        return urls_list if urls_list else EPISODE_URLS

    except Exception as e:
        print(f"[WARN] Could not auto-discover episodes: {e}")
        print(f"Using fallback list of {len(EPISODE_URLS)} known URLs")
        return EPISODE_URLS


async def download_transcript_from_url(page, pdf_url, output_filename):
    """Download a PDF transcript given its direct URL"""
    try:
        # Navigate to the PDF URL
        response = await page.goto(pdf_url, wait_until="commit", timeout=30000)

        if response and response.status == 200:
            # Get the PDF content
            content = await response.body()

            if len(content) > 1000:  # Valid PDF should be > 1KB
                filepath = os.path.join(OUTPUT_DIR, output_filename)
                with open(filepath, 'wb') as f:
                    f.write(content)

                print(f"  [OK] Downloaded: {output_filename} ({len(content):,} bytes)")
                return True
            else:
                print(f"  [WARN] File too small: {output_filename}")
                return False
        else:
            print(f"  [FAIL] Failed (status {response.status if response else 'unknown'}): {output_filename}")
            return False

    except Exception as e:
        print(f"  [FAIL] Error downloading {output_filename}: {str(e)[:80]}")
        return False


async def extract_transcript_links(page, episode_url):
    """Navigate to episode page and extract transcript PDF links"""
    try:
        await page.goto(episode_url, wait_until="networkidle", timeout=30000)
        await asyncio.sleep(1)  # Let page settle

        # Look for transcript links - they typically contain "transcript" and end in .pdf
        all_links = await page.query_selector_all('a[href$=".pdf"]')

        transcript_links = []
        for link in all_links:
            href = await link.get_attribute('href')
            text = await link.inner_text()

            if href and 'transcript' in href.lower():
                transcript_links.append({
                    'url': href,
                    'text': text.strip(),
                    'type': 'audio' if 'audio' in href.lower() else 'video'
                })

        return transcript_links

    except Exception as e:
        print(f"  [WARN] Error accessing page: {str(e)[:100]}")
        return []


async def download_episode_transcripts(page, episode_url, episode_number):
    """Download both video and audio transcripts for an episode"""

    # Extract topic slug from URL
    topic_slug = episode_url.rstrip('/').split('/')[-1]

    print(f"\n[{episode_number:02d}] {topic_slug}")
    print(f"     {episode_url}")

    # Get transcript links from the page
    transcript_links = await extract_transcript_links(page, episode_url)

    if not transcript_links:
        print(f"  [WARN] No transcript links found on page")

        # Try known URL patterns as fallback
        print(f"  [INFO] Trying known URL patterns...")
        base_pdf_url = "https://www.learner.org/wp-content/uploads/2019/02"

        patterns = [
            (f"{base_pdf_url}/economics-usa-{topic_slug}-video-transcript.pdf", f"{episode_number:02d}-{topic_slug}-video.pdf"),
            (f"{base_pdf_url}/economics-usa-{topic_slug}-audio-transcript.pdf", f"{episode_number:02d}-{topic_slug}-audio.pdf"),
            (f"{base_pdf_url}/economics-usa-{topic_slug}-audio-transcript-supplemental.pdf", f"{episode_number:02d}-{topic_slug}-audio.pdf"),
        ]

        downloaded_count = 0
        for pdf_url, filename in patterns:
            if await download_transcript_from_url(page, pdf_url, filename):
                downloaded_count += 1

        return downloaded_count

    # Download each transcript found on the page
    downloaded_count = 0
    for i, link in enumerate(transcript_links):
        transcript_type = link['type']
        output_filename = f"{episode_number:02d}-{topic_slug}-{transcript_type}.pdf"

        if await download_transcript_from_url(page, link['url'], output_filename):
            downloaded_count += 1

        await asyncio.sleep(0.5)  # Be respectful to server

    return downloaded_count


async def main():
    print("=" * 80)
    print("Economics USA Transcript Downloader (Playwright)")
    print("=" * 80)
    print(f"Output directory: {OUTPUT_DIR}")
    print()

    # Create output directory
    os.makedirs(OUTPUT_DIR, exist_ok=True)

    async with async_playwright() as p:
        # Launch browser (headless for speed, set to False to see it work)
        browser = await p.chromium.launch(headless=True)

        # Create context with realistic headers
        context = await browser.new_context(
            user_agent='Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36',
            viewport={'width': 1920, 'height': 1080}
        )

        page = await context.new_page()

        # Step 1: Get all episode URLs
        episode_urls = await get_all_episode_urls(page)

        print(f"\n[INFO] Starting download of transcripts from {len(episode_urls)} episodes...")
        print("=" * 80)

        # Step 2: Download transcripts from each episode
        total_downloaded = 0
        failed_episodes = []

        for i, episode_url in enumerate(episode_urls, 1):
            try:
                count = await download_episode_transcripts(page, episode_url, i)
                total_downloaded += count

                if count == 0:
                    failed_episodes.append((i, episode_url))

                # Be respectful - small delay between episodes
                await asyncio.sleep(1)

            except Exception as e:
                print(f"  [FAIL] Failed to process episode: {str(e)[:100]}")
                failed_episodes.append((i, episode_url))

        await browser.close()

        # Summary
        print("\n" + "=" * 80)
        print("DOWNLOAD SUMMARY")
        print("=" * 80)
        print(f"Episodes processed: {len(episode_urls)}")
        print(f"Transcripts downloaded: {total_downloaded}")
        print(f"Expected total: {len(episode_urls) * 2} (2 per episode)")
        print(f"Success rate: {total_downloaded}/{len(episode_urls) * 2}")

        if failed_episodes:
            print(f"\n[WARN] {len(failed_episodes)} episodes had issues:")
            for num, url in failed_episodes:
                print(f"  [{num:02d}] {url}")

        print(f"\n[INFO] Files saved to: {OUTPUT_DIR}")

        # List downloaded files
        downloaded_files = sorted(Path(OUTPUT_DIR).glob("*.pdf"))
        if downloaded_files:
            print(f"\n[OK] Downloaded files ({len(downloaded_files)}):")
            for filepath in downloaded_files:
                size = filepath.stat().st_size
                print(f"  - {filepath.name} ({size:,} bytes)")

        if total_downloaded < len(episode_urls) * 2:
            print("\n[TIP] Some transcripts may need manual download from learner.org")
            print("      Check the failed episodes list above and visit those pages directly.")


if __name__ == "__main__":
    asyncio.run(main())
