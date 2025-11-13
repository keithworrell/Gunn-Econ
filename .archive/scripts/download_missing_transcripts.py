#!/usr/bin/env python3
"""
Download missing Economics USA transcripts by trying alternative URL patterns
"""

import os
import requests
from pathlib import Path
import time

OUTPUT_DIR = "economics-spanish/original-transcripts"
BASE_URL = "https://www.learner.org/wp-content/uploads/2019/02"

# Missing transcripts with alternative slug patterns to try
MISSING_EPISODES = [
    {
        'num': 4,
        'title': "Perfect Competition & Inelastic Demand",
        'slugs': [
            "perfect-competition",
            "competition",
            "inelastic-demand",
            "perfect-competition-and-inelastic-demand",
        ]
    },
    {
        'num': 5,
        'title': "Economic Efficiency",
        'slugs': [
            "efficiency",
        ],
        'video_found': True  # Only need audio
    },
    {
        'num': 13,
        'title': "Public Goods and Responsibilities",
        'slugs': [
            "public-goods",
            "public-goods-and-responsibilities",
            "responsibilities",
        ]
    },
    {
        'num': 17,
        'title': "The Great Depression and the Keynesian Revolution",
        'slugs': [
            "great-depression",
            "keynesian-revolution",
            "depression",
            "great-depression-and-keynesian-revolution",
        ]
    },
    {
        'num': 26,
        'title': "Stabilization Policy",
        'slugs': [
            "stabilization",
        ]
    },
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
        elif response.status_code == 404:
            return False
        else:
            print(f"  [SKIP] {filename} (status {response.status_code})")
            return False

    except Exception as e:
        return False


def main():
    print("=" * 80)
    print("Missing Transcripts Downloader")
    print("=" * 80)
    print(f"Trying alternative URL patterns for {len(MISSING_EPISODES)} episodes")
    print("=" * 80)

    os.makedirs(OUTPUT_DIR, exist_ok=True)

    downloaded = 0
    still_missing = []

    for episode in MISSING_EPISODES:
        num = episode['num']
        title = episode['title']
        slugs = episode['slugs']
        video_found = episode.get('video_found', False)

        print(f"\n[{num:02d}] {title}")

        # Try video transcript
        if not video_found:
            video_success = False
            for slug in slugs:
                video_url = f"{BASE_URL}/economics-usa-{slug}-video-transcript.pdf"
                video_file = f"{num:02d}-{slug}-video.pdf"
                print(f"  Trying: {slug} (video)...")
                if download_pdf(video_url, video_file):
                    downloaded += 1
                    video_success = True
                    break
                time.sleep(0.3)

            if not video_success:
                still_missing.append((num, title, "video"))

        # Try audio transcript
        audio_success = False
        for slug in slugs:
            # Try regular audio transcript
            audio_url = f"{BASE_URL}/economics-usa-{slug}-audio-transcript.pdf"
            audio_file = f"{num:02d}-{slug}-audio.pdf"
            print(f"  Trying: {slug} (audio)...")
            if download_pdf(audio_url, audio_file):
                downloaded += 1
                audio_success = True
                break

            # Try with -supplemental suffix
            audio_url_alt = f"{BASE_URL}/economics-usa-{slug}-audio-transcript-supplemental.pdf"
            if download_pdf(audio_url_alt, audio_file):
                downloaded += 1
                audio_success = True
                break

            time.sleep(0.3)

        if not audio_success:
            still_missing.append((num, title, "audio"))

        time.sleep(0.5)

    # Summary
    print("\n" + "=" * 80)
    print("DOWNLOAD SUMMARY")
    print("=" * 80)
    print(f"Additional transcripts downloaded: {downloaded}")

    if still_missing:
        print(f"\n[WARN] {len(still_missing)} transcripts still missing:")
        for num, title, type in still_missing:
            print(f"  [{num:02d}] {title} ({type})")
        print("\nThese may need manual download from learner.org")
    else:
        print("\n[OK] All missing transcripts found!")

    # List all downloaded files
    downloaded_files = sorted(Path(OUTPUT_DIR).glob("*.pdf"))
    print(f"\n[INFO] Total files in directory: {len(downloaded_files)}")


if __name__ == "__main__":
    main()
