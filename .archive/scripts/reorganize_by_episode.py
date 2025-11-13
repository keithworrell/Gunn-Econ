#!/usr/bin/env python3
"""
Reorganize files into episode folders
Each episode folder contains: original video, original audio, spanish video, spanish audio, audio video mp3, audio audio mp3
"""

import os
import shutil
from pathlib import Path

# Define the episodes with their proper titles
EPISODES = [
    (1, "Markets"),
    (2, "The-Firm"),
    (3, "Supply-and-Demand"),
    (5, "Economic-Efficiency"),
    (6, "Monopoly"),
    (7, "Oligopolies"),
    (8, "Pollution-and-Environment"),
    (9, "Labor-and-Management"),
    (10, "Profits-and-Interest"),
    (11, "Reducing-Poverty"),
    (12, "Economic-Growth"),
    (13, "Public-Goods-and-Responsibilities"),
    (14, "Resources-and-Scarcity"),
    (15, "GDP-GNP"),
    (16, "Boom-and-Bust"),
    (17, "The-Great-Depression-and-the-Keynesian-Revolution"),
    (18, "Fiscal-Policy"),
    (19, "Inflation"),
    (20, "The-Banking-System"),
    (21, "The-Federal-Reserve"),
    (22, "Stagflation"),
    (23, "Productivity"),
    (24, "Federal-Deficits"),
    (25, "Monetary-Policy"),
    (26, "Stabilization-Policy"),
    (27, "International-Trade"),
    (28, "Exchange-Rates"),
]

def main():
    print("Reorganizing files by episode...")

    # Get all files from the three directories
    original_files = list(Path("original-transcripts").glob("*.pdf"))
    spanish_files = list(Path("spanish-transcripts").glob("*.pdf"))
    audio_files = list(Path("audio-files").glob("*.mp3"))

    print(f"Found {len(original_files)} original transcripts")
    print(f"Found {len(spanish_files)} Spanish transcripts")
    print(f"Found {len(audio_files)} audio files")

    moved_count = 0

    for num, title in EPISODES:
        # Create episode folder
        folder_name = f"{num:02d}-{title}"
        os.makedirs(folder_name, exist_ok=True)
        print(f"\n{folder_name}:")

        # Move files matching this episode number
        episode_prefix = f"{num:02d}-"

        # Move original transcripts
        for file in original_files:
            if file.name.startswith(episode_prefix):
                dest = Path(folder_name) / file.name
                shutil.move(str(file), str(dest))
                print(f"  Moved: {file.name}")
                moved_count += 1

        # Move Spanish transcripts
        for file in spanish_files:
            if file.name.startswith(episode_prefix):
                dest = Path(folder_name) / file.name
                shutil.move(str(file), str(dest))
                print(f"  Moved: {file.name}")
                moved_count += 1

        # Move audio files
        for file in audio_files:
            if file.name.startswith(episode_prefix):
                dest = Path(folder_name) / file.name
                shutil.move(str(file), str(dest))
                print(f"  Moved: {file.name}")
                moved_count += 1

    # Check for any remaining files
    remaining_original = list(Path("original-transcripts").glob("*.pdf"))
    remaining_spanish = list(Path("spanish-transcripts").glob("*.pdf"))
    remaining_audio = list(Path("audio-files").glob("*.mp3"))

    if remaining_original or remaining_spanish or remaining_audio:
        print("\n\nRemaining files that didn't match:")
        for f in remaining_original:
            print(f"  original-transcripts/{f.name}")
        for f in remaining_spanish:
            print(f"  spanish-transcripts/{f.name}")
        for f in remaining_audio:
            print(f"  audio-files/{f.name}")

    print(f"\n\nTotal files moved: {moved_count}")
    print(f"Created {len(EPISODES)} episode folders")

    # Remove empty directories
    if not list(Path("original-transcripts").glob("*.pdf")):
        print("\nRemoving empty original-transcripts folder...")
        Path("original-transcripts/.gitkeep").unlink(missing_ok=True)
        Path("original-transcripts").rmdir()

    if not list(Path("spanish-transcripts").glob("*.pdf")):
        print("Removing empty spanish-transcripts folder...")
        Path("spanish-transcripts/.gitkeep").unlink(missing_ok=True)
        Path("spanish-transcripts").rmdir()

    if not list(Path("audio-files").glob("*.mp3")):
        print("Removing empty audio-files folder...")
        Path("audio-files/.gitkeep").unlink(missing_ok=True)
        Path("audio-files").rmdir()

    print("\n✓ Reorganization complete!")

if __name__ == "__main__":
    main()
