#!/usr/bin/env python3
"""
Alternative Transcript Downloader - Uses requests library instead of Selenium
For environments where Chrome/Chromium is not available
"""

import os
import requests
from bs4 import BeautifulSoup
from tqdm import tqdm
import time

# Constants
SERIES_URL = "https://learner.org/series/economics-ua-21st-century-edition"
OUTPUT_DIR = "economics-spanish/original-transcripts"

# Known video URLs (manually extracted from the series page)
# Users can update this list by visiting the series page
VIDEO_URLS = [
    # Example format - users should populate this
    # "https://learner.org/courses/economics-usa-21st-century-edition/what-sets-prices/",
    # "https://learner.org/courses/economics-usa-21st-century-edition/supply-and-demand/",
]

def get_session():
    """Create a requests session with browser-like headers"""
    session = requests.Session()
    session.headers.update({
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36',
        'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8',
        'Accept-Language': 'en-US,en;q=0.5',
        'Accept-Encoding': 'gzip, deflate, br',
        'DNT': '1',
        'Connection': 'keep-alive',
        'Upgrade-Insecure-Requests': '1'
    })
    return session

def discover_video_urls(session):
    """Try to discover video URLs from the series page"""
    print(f"Attempting to fetch series page: {SERIES_URL}")

    try:
        response = session.get(SERIES_URL, timeout=30)
        response.raise_for_status()

        soup = BeautifulSoup(response.content, 'html.parser')

        # Save page for inspection
        with open('series_page.html', 'w', encoding='utf-8') as f:
            f.write(soup.prettify())
        print("  ✓ Series page saved to series_page.html")

        # Try to find video links
        video_links = []
        for link in soup.find_all('a', href=True):
            href = link['href']
            if 'courses' in href or 'video' in href:
                if href.startswith('/'):
                    href = f"https://learner.org{href}"
                if href not in video_links:
                    video_links.append(href)

        return video_links

    except requests.exceptions.RequestException as e:
        print(f"  ✗ Error fetching series page: {e}")
        return []

def download_transcript_from_url(session, video_url, video_number):
    """Download transcript from a specific video URL"""
    try:
        print(f"\nFetching video page {video_number}: {video_url}")
        response = session.get(video_url, timeout=30)
        response.raise_for_status()

        soup = BeautifulSoup(response.content, 'html.parser')

        # Look for PDF links
        pdf_url = None
        for link in soup.find_all('a', href=True):
            href = link['href']
            link_text = link.get_text(strip=True).lower()

            if 'transcript' in link_text and '.pdf' in href:
                if href.startswith('/'):
                    href = f"https://learner.org{href}"
                pdf_url = href
                break

        if not pdf_url:
            # Try finding any PDF
            for link in soup.find_all('a', href=True):
                if link['href'].endswith('.pdf'):
                    pdf_url = link['href']
                    if pdf_url.startswith('/'):
                        pdf_url = f"https://learner.org{pdf_url}"
                    break

        if not pdf_url:
            print(f"  ✗ No PDF transcript found")
            return False

        # Download PDF
        print(f"  Downloading: {pdf_url}")
        pdf_response = session.get(pdf_url, timeout=30)
        pdf_response.raise_for_status()

        # Save PDF
        filename = f"video-{video_number:02d}.pdf"
        filepath = os.path.join(OUTPUT_DIR, filename)

        with open(filepath, 'wb') as f:
            f.write(pdf_response.content)

        print(f"  ✓ Saved: {filename}")
        return True

    except Exception as e:
        print(f"  ✗ Error: {e}")
        return False

def main():
    print("Alternative Transcript Downloader (requests-based)")
    print("=" * 60)

    os.makedirs(OUTPUT_DIR, exist_ok=True)
    session = get_session()

    # Try to discover video URLs
    if not VIDEO_URLS:
        print("\nAttempting to discover video URLs...")
        discovered_urls = discover_video_urls(session)

        if discovered_urls:
            print(f"\nFound {len(discovered_urls)} potential video URLs:")
            for i, url in enumerate(discovered_urls, 1):
                print(f"  {i}. {url}")

            print("\nPlease inspect series_page.html and update VIDEO_URLS in this script.")
            print("Then run again to download transcripts.")
            return
        else:
            print("\n⚠ Could not automatically discover video URLs.")
            print("Please manually add video URLs to the VIDEO_URLS list in this script.")
            return

    # Download transcripts
    print(f"\nDownloading {len(VIDEO_URLS)} transcripts...")
    success_count = 0

    for i, url in enumerate(VIDEO_URLS, 1):
        if download_transcript_from_url(session, url, i):
            success_count += 1
        time.sleep(2)  # Be respectful

    print(f"\n{'='*60}")
    print(f"Complete! Downloaded {success_count}/{len(VIDEO_URLS)} transcripts")
    print(f"Saved to: {OUTPUT_DIR}")

if __name__ == "__main__":
    main()
