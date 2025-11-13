#!/usr/bin/env python3
"""
Economics Video Transcript Downloader
Downloads all video transcripts from learner.org economics series
"""

import os
import time
import requests
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from webdriver_manager.chrome import ChromeDriverManager
from bs4 import BeautifulSoup
from tqdm import tqdm

# Constants
SERIES_URL = "https://learner.org/series/economics-ua-21st-century-edition"
OUTPUT_DIR = "economics-spanish/original-transcripts"

def setup_driver():
    """Set up Selenium WebDriver with Chrome"""
    chrome_options = Options()
    chrome_options.add_argument("--headless")  # Run in background
    chrome_options.add_argument("--no-sandbox")
    chrome_options.add_argument("--disable-dev-shm-usage")
    chrome_options.add_argument("--disable-gpu")
    chrome_options.add_argument("--window-size=1920,1080")
    chrome_options.add_argument("user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36")

    service = Service(ChromeDriverManager().install())
    driver = webdriver.Chrome(service=service, options=chrome_options)
    return driver

def get_video_links(driver):
    """Extract all video links from the series page"""
    print(f"Loading series page: {SERIES_URL}")
    driver.get(SERIES_URL)

    # Wait for page to load
    time.sleep(3)

    # Try to find video links in the sidebar or main content
    video_links = []

    try:
        # Wait for content to load
        WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.TAG_NAME, "body"))
        )

        # Get page source and parse with BeautifulSoup
        soup = BeautifulSoup(driver.page_source, 'html.parser')

        # Look for video links (adjust selectors based on actual page structure)
        # Try multiple possible selectors
        possible_selectors = [
            'a[href*="/courses/"]',
            'a[href*="/video/"]',
            'a[href*="economics"]',
            '.video-link',
            '.episode-link',
        ]

        for selector in possible_selectors:
            links = soup.select(selector)
            if links:
                print(f"Found {len(links)} links with selector: {selector}")
                for link in links:
                    href = link.get('href')
                    if href:
                        # Convert relative URLs to absolute
                        if href.startswith('/'):
                            href = f"https://learner.org{href}"
                        video_links.append({
                            'title': link.get_text(strip=True),
                            'url': href
                        })
                break

        # Remove duplicates
        seen_urls = set()
        unique_links = []
        for link in video_links:
            if link['url'] not in seen_urls:
                seen_urls.add(link['url'])
                unique_links.append(link)

        return unique_links

    except Exception as e:
        print(f"Error extracting video links: {e}")
        # Save page source for debugging
        with open('page_source_debug.html', 'w', encoding='utf-8') as f:
            f.write(driver.page_source)
        print("Page source saved to page_source_debug.html for inspection")
        return []

def download_transcript(driver, video_url, video_number, video_title):
    """Navigate to video page and download transcript PDF"""
    try:
        print(f"\nProcessing video {video_number}: {video_title}")
        driver.get(video_url)
        time.sleep(2)

        # Look for transcript/PDF download link
        soup = BeautifulSoup(driver.page_source, 'html.parser')

        # Try to find PDF link
        pdf_links = []
        for link in soup.find_all('a', href=True):
            href = link['href']
            link_text = link.get_text(strip=True).lower()

            if 'transcript' in link_text or href.endswith('.pdf'):
                if href.startswith('/'):
                    href = f"https://learner.org{href}"
                pdf_links.append(href)

        if not pdf_links:
            print(f"  No transcript PDF found for: {video_title}")
            return False

        # Download the first PDF found
        pdf_url = pdf_links[0]
        print(f"  Downloading transcript from: {pdf_url}")

        # Download with proper headers
        headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36'
        }
        response = requests.get(pdf_url, headers=headers, timeout=30)
        response.raise_for_status()

        # Save PDF
        filename = f"video-{video_number:02d}-{sanitize_filename(video_title)}.pdf"
        filepath = os.path.join(OUTPUT_DIR, filename)

        with open(filepath, 'wb') as f:
            f.write(response.content)

        print(f"  ✓ Saved: {filename}")
        return True

    except Exception as e:
        print(f"  ✗ Error downloading transcript: {e}")
        return False

def sanitize_filename(filename):
    """Remove invalid characters from filename"""
    invalid_chars = '<>:"/\\|?*'
    for char in invalid_chars:
        filename = filename.replace(char, '')
    return filename[:50]  # Limit length

def main():
    """Main execution function"""
    print("Economics Transcript Downloader")
    print("=" * 50)

    # Create output directory
    os.makedirs(OUTPUT_DIR, exist_ok=True)

    # Set up Selenium driver
    driver = None
    try:
        driver = setup_driver()

        # Get all video links
        video_links = get_video_links(driver)

        if not video_links:
            print("\n⚠ No video links found. Please check the page structure.")
            print("You may need to manually inspect the website and update the selectors.")
            return

        print(f"\nFound {len(video_links)} videos")
        print("\nVideo list:")
        for i, link in enumerate(video_links, 1):
            print(f"  {i}. {link['title']}")

        # Download transcripts
        print("\n" + "=" * 50)
        print("Downloading transcripts...")
        print("=" * 50)

        success_count = 0
        for i, link in enumerate(tqdm(video_links, desc="Progress"), 1):
            if download_transcript(driver, link['url'], i, link['title']):
                success_count += 1
            time.sleep(1)  # Be respectful to the server

        print(f"\n{'=' * 50}")
        print(f"Download complete!")
        print(f"Successfully downloaded: {success_count}/{len(video_links)} transcripts")
        print(f"Saved to: {OUTPUT_DIR}")

    except Exception as e:
        print(f"\nFatal error: {e}")
        import traceback
        traceback.print_exc()

    finally:
        if driver:
            driver.quit()

if __name__ == "__main__":
    main()
