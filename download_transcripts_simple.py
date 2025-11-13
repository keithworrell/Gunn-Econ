#!/usr/bin/env python3
"""
Simple downloader for Economics USA transcripts using direct PDF URLs
Based on confirmed working URL pattern from learner.org
"""

import os
import requests
from pathlib import Path
import time

OUTPUT_DIR = "economics-spanish/original-transcripts"

# Based on manual verification, all PDFs are at /wp-content/uploads/2019/02/
BASE_URL = "https://www.learner.org/wp-content/uploads/2019/02"

# Complete list of 28 Economics USA episodes with correct URL slugs
# Each episode has TWO transcripts: video and audio
EPISODES = [
    ("markets", "Markets"),
    ("firm", "The Firm"),
    ("supply-demand", "Supply and Demand"),
    ("perfect-competition-inelastic-demand", "Perfect Competition & Inelastic Demand"),
    ("economic-efficiency", "Economic Efficiency"),
    ("monopoly", "Monopoly"),
    ("oligopolies", "Oligopolies"),
    ("pollution-environment", "Pollution & the Environment"),
    ("labor-management", "Labor and Management"),
    ("profits-interest", "Profits and Interest"),
    ("reducing-poverty", "Reducing Poverty"),
    ("economic-growth", "Economic Growth"),
    ("public-goods-responsibilities", "Public Goods and Responsibilities"),
    ("resources-scarcity", "Resources and Scarcity"),
    ("gnp-gdp", "GDP/GNP"),
    ("boom-bust", "Boom and Bust"),
    ("great-depression-keynesian-revolution", "The Great Depression and the Keynesian Revolution"),
    ("fiscal-policy", "Fiscal Policy"),
    ("inflation", "Inflation"),
    ("banking-system", "The Banking System"),
    ("federal-reserve", "The Federal Reserve"),
    ("stagflation", "Stagflation"),
    ("productivity", "Productivity"),
    ("federal-deficits", "Federal Deficits"),
    ("monetary-policy", "Monetary Policy"),
    ("stabilization-policy", "Stabilization Policy"),
    ("international-trade", "International Trade"),
    ("exchange-rates", "Exchange Rates"),
]


def download_pdf(url, filename):
    """Download a PDF file"""
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36'
    }

    try:
        response = requests.get(url, headers=headers, timeout=30)

        if response.status_code == 200 and len(response.content) > 1000:
            filepath = os.path.join(OUTPUT_DIR, filename)
            with open(filepath, 'wb') as f:
                f.write(response.content)
            print(f"  [OK] {filename} ({len(response.content):,} bytes)")
            return True
        else:
            print(f"  [SKIP] {filename} (status {response.status_code})")
            return False

    except Exception as e:
        print(f"  [FAIL] {filename}: {str(e)[:60]}")
        return False


def main():
    print("=" * 80)
    print("Economics USA Transcript Downloader")
    print("=" * 80)
    print(f"Downloading from: {BASE_URL}")
    print(f"Saving to: {OUTPUT_DIR}")
    print("=" * 80)

    # Create output directory
    os.makedirs(OUTPUT_DIR, exist_ok=True)

    downloaded = 0
    failed = []

    # Download both transcripts for each episode
    for i, (slug, title) in enumerate(EPISODES, 1):
        print(f"\n[{i:02d}/28] {title}")
        print(f"     Slug: {slug}")

        # Try video transcript
        video_url = f"{BASE_URL}/economics-usa-{slug}-video-transcript.pdf"
        video_file = f"{i:02d}-{slug}-video.pdf"
        if download_pdf(video_url, video_file):
            downloaded += 1
        else:
            failed.append((i, title, "video"))

        time.sleep(0.5)  # Be respectful

        # Try audio transcript (try both with and without -supplemental suffix)
        audio_url = f"{BASE_URL}/economics-usa-{slug}-audio-transcript.pdf"
        audio_file = f"{i:02d}-{slug}-audio.pdf"
        if download_pdf(audio_url, audio_file):
            downloaded += 1
        else:
            # Try alternative with -supplemental suffix
            audio_url_alt = f"{BASE_URL}/economics-usa-{slug}-audio-transcript-supplemental.pdf"
            if download_pdf(audio_url_alt, audio_file):
                downloaded += 1
            else:
                failed.append((i, title, "audio"))

        time.sleep(0.5)  # Be respectful

    # Summary
    print("\n" + "=" * 80)
    print("DOWNLOAD SUMMARY")
    print("=" * 80)
    print(f"Episodes processed: 28")
    print(f"Transcripts downloaded: {downloaded}/56")
    print(f"Success rate: {(downloaded/56)*100:.1f}%")

    if failed:
        print(f"\n[WARN] {len(failed)} transcripts could not be downloaded:")
        for num, title, type in failed:
            print(f"  [{num:02d}] {title} ({type})")

    print(f"\n[INFO] Files saved to: {OUTPUT_DIR}")

    # List downloaded files
    downloaded_files = sorted(Path(OUTPUT_DIR).glob("*.pdf"))
    print(f"\n[INFO] Total files in directory: {len(downloaded_files)}")

    if downloaded < 56:
        print("\n[TIP] Some transcripts may use different URL slugs.")
        print("      Check the learner.org website manually for missing episodes.")


if __name__ == "__main__":
    main()
