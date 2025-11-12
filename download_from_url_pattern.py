#!/usr/bin/env python3
"""
Download Economics USA Transcripts using known URL pattern
Based on: https://www.learner.org/wp-content/uploads/2019/02/economics-usa-markets-audio-transcript.pdf

URL Pattern: /wp-content/uploads/YYYY/MM/economics-usa-{topic}-audio-transcript.pdf
"""

import os
import requests
from pathlib import Path
import time
from tqdm import tqdm

OUTPUT_DIR = "economics-spanish/original-transcripts"

# Known Economics USA episodes (28 total in the series)
# Topic slugs derived from typical course structure
ECONOMICS_USA_TOPICS = [
    # Microeconomics
    "supply-demand",
    "markets",
    "competition",
    "market-structures",
    "monopoly",
    "oligopoly",
    "market-power",
    "labor-markets",
    "income-distribution",
    "poverty",
    "externalities",
    "public-goods",
    "government-regulation",
    "antitrust",

    # Macroeconomics
    "resources-scarcity",
    "economic-growth",
    "productivity",
    "unemployment",
    "inflation",
    "business-cycles",
    "aggregate-supply-demand",
    "monetary-policy",
    "fiscal-policy",
    "federal-budget",
    "federal-deficits",
    "national-debt",

    # International
    "international-trade",
    "comparative-advantage",
    "exchange-rates",
    "balance-payments",
    "developing-economies",
    "globalization",
]

# Possible date folders (transcripts were uploaded in 2019)
DATE_FOLDERS = [
    "2019/01", "2019/02", "2019/03", "2019/04", "2019/05", "2019/06",
    "2019/07", "2019/08", "2019/09", "2019/10", "2019/11", "2019/12",
]

def download_transcript(topic, date_folder, video_number):
    """Try to download a transcript PDF"""
    base_url = "https://www.learner.org/wp-content/uploads"

    # Try different filename patterns
    patterns = [
        f"{base_url}/{date_folder}/economics-usa-{topic}-audio-transcript.pdf",
        f"{base_url}/{date_folder}/economics-usa-{topic}-transcript.pdf",
        f"{base_url}/{date_folder}/EconomicsUSA-{topic}-transcript.pdf",
    ]

    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36'
    }

    for url in patterns:
        try:
            response = requests.get(url, headers=headers, timeout=30)

            if response.status_code == 200 and len(response.content) > 1000:
                # Save file
                filename = f"video-{video_number:02d}-{topic}.pdf"
                filepath = os.path.join(OUTPUT_DIR, filename)

                with open(filepath, 'wb') as f:
                    f.write(response.content)

                print(f"  ✓ Downloaded: {filename} ({len(response.content)} bytes)")
                return True

        except Exception as e:
            continue

    return False

def main():
    print("Economics USA Transcript Downloader")
    print("=" * 70)
    print("Using known URL pattern from learner.org")
    print("=" * 70)

    os.makedirs(OUTPUT_DIR, exist_ok=True)

    downloaded = []
    failed = []

    # Try each topic
    for i, topic in enumerate(tqdm(ECONOMICS_USA_TOPICS, desc="Downloading"), 1):
        print(f"\n[{i}/{len(ECONOMICS_USA_TOPICS)}] Trying: {topic}")

        success = False

        # Try each date folder
        for date_folder in DATE_FOLDERS:
            if download_transcript(topic, date_folder, i):
                downloaded.append(topic)
                success = True
                break
            time.sleep(0.5)  # Be respectful

        if not success:
            print(f"  ✗ Not found: {topic}")
            failed.append(topic)

    # Summary
    print("\n" + "=" * 70)
    print("Download Complete!")
    print("=" * 70)
    print(f"Successfully downloaded: {len(downloaded)} transcripts")
    print(f"Not found: {len(failed)} transcripts")

    if downloaded:
        print("\n✓ Downloaded:")
        for topic in downloaded:
            print(f"  - {topic}")

    if failed:
        print("\n✗ Not found (may need manual download):")
        for topic in failed:
            print(f"  - {topic}")

    print(f"\nFiles saved to: {OUTPUT_DIR}")

    if len(downloaded) < 20:
        print("\n⚠ Found fewer than expected (Economics USA has ~28 episodes)")
        print("Some transcripts may use different topic slugs.")
        print("Check the learner.org website manually for remaining episodes.")

if __name__ == "__main__":
    main()
