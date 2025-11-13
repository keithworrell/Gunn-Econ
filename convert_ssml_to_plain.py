#!/usr/bin/env python3
"""
Convert SSML files to plain text for edge-tts (which doesn't support SSML).
"""

import re
from pathlib import Path
from tqdm import tqdm


def strip_ssml_to_plain_text(ssml_content):
    """Remove all SSML tags and convert to plain Spanish text."""

    # Remove the outer <speak> wrapper
    content = re.sub(r'<speak[^>]*>', '', ssml_content)
    content = re.sub(r'</speak>', '', content)

    # Remove all SSML tags but keep their content
    # <break> tags - remove entirely
    content = re.sub(r'<break[^>]*/?>', '', content)

    # <emphasis> tags - keep content only
    content = re.sub(r'<emphasis[^>]*>(.*?)</emphasis>', r'\1', content)

    # <prosody> tags - keep content only
    content = re.sub(r'<prosody[^>]*>(.*?)</prosody>', r'\1', content)

    # Any other remaining tags
    content = re.sub(r'<[^>]+>', '', content)

    # Clean up excessive whitespace
    content = re.sub(r'\n\s*\n\s*\n+', '\n\n', content)
    content = re.sub(r'[ \t]+', ' ', content)

    # Trim leading/trailing whitespace
    content = content.strip()

    return content


def process_all_ssml_files():
    """Convert all SSML files to plain text."""
    input_dir = Path("economics-spanish/tts-prepared")
    output_dir = Path("economics-spanish/tts-plain-text")
    output_dir.mkdir(exist_ok=True)

    ssml_files = sorted(input_dir.glob("*.ssml"))

    print("Converting SSML to Plain Text for edge-tts")
    print("=" * 70)
    print(f"Found {len(ssml_files)} SSML files to convert\n")

    for ssml_file in tqdm(ssml_files, desc="Converting"):
        # Read SSML
        ssml_content = ssml_file.read_text(encoding='utf-8')

        # Convert to plain text
        plain_text = strip_ssml_to_plain_text(ssml_content)

        # Save as .txt file
        output_file = output_dir / ssml_file.name.replace('.ssml', '.txt')
        output_file.write_text(plain_text, encoding='utf-8')

    print("\n" + "=" * 70)
    print("Conversion Complete!")
    print(f"Converted: {len(ssml_files)}/{len(ssml_files)} files")
    print(f"Output directory: {output_dir}")
    print("\nNext step: Update generate_audio.py to use .txt files instead of .ssml")


if __name__ == "__main__":
    process_all_ssml_files()
