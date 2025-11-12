#!/usr/bin/env python3
"""
Economics Transcript Audio Generator
Converts Spanish transcripts to MP3 audio files using Microsoft Edge TTS
"""

import os
import asyncio
from pathlib import Path
import pdfplumber
import edge_tts
from tqdm import tqdm

# Constants
INPUT_DIR = "economics-spanish/spanish-transcripts"
OUTPUT_DIR = "economics-spanish/audio-files"

# Spanish voice options (Microsoft Edge TTS)
SPANISH_VOICES = {
    'female': 'es-MX-DaliaNeural',  # Mexican Spanish, Female
    'male': 'es-MX-JorgeNeural',    # Mexican Spanish, Male
    'female_spain': 'es-ES-ElviraNeural',  # Spain Spanish, Female
    'male_spain': 'es-ES-AlvaroNeural',    # Spain Spanish, Male
}

# Default voice
DEFAULT_VOICE = SPANISH_VOICES['female']

class AudioGenerator:
    def __init__(self, voice=DEFAULT_VOICE):
        self.voice = voice

    def extract_text_from_pdf(self, pdf_path):
        """Extract all text from Spanish PDF"""
        print(f"  Extracting text from PDF...")

        full_text = []

        try:
            with pdfplumber.open(pdf_path) as pdf:
                for page in pdf.pages:
                    text = page.extract_text()
                    if text:
                        full_text.append(text)

            combined_text = '\n\n'.join(full_text)
            print(f"  ✓ Extracted {len(combined_text)} characters from {len(pdf.pages)} pages")
            return combined_text

        except Exception as e:
            print(f"  ✗ Error extracting text: {e}")
            return ""

    def clean_text_for_tts(self, text):
        """Clean and format text for better TTS output"""
        # Remove page numbers and artifacts
        lines = text.split('\n')
        cleaned_lines = []

        for line in lines:
            line = line.strip()

            # Skip very short lines (likely page numbers)
            if len(line) < 3:
                continue

            # Skip lines that are just numbers
            if line.isdigit():
                continue

            cleaned_lines.append(line)

        # Join with proper spacing
        cleaned_text = '\n\n'.join(cleaned_lines)

        return cleaned_text

    async def generate_audio_async(self, text, output_path):
        """Generate audio file from text using Edge TTS"""
        print(f"  Generating audio with voice: {self.voice}")

        try:
            # Create TTS communicator
            communicate = edge_tts.Communicate(text, self.voice)

            # Generate and save audio
            await communicate.save(output_path)

            print(f"  ✓ Audio file created successfully")
            return True

        except Exception as e:
            print(f"  ✗ Error generating audio: {e}")
            return False

    def generate_audio(self, text, output_path):
        """Synchronous wrapper for audio generation"""
        return asyncio.run(self.generate_audio_async(text, output_path))

    def process_transcript(self, pdf_path):
        """Process a single transcript: extract text and generate audio"""
        filename = os.path.basename(pdf_path)
        print(f"\n{'='*60}")
        print(f"Processing: {filename}")
        print(f"{'='*60}")

        # Extract text
        text = self.extract_text_from_pdf(pdf_path)
        if not text:
            print("  ✗ No text extracted, skipping...")
            return False

        # Clean text
        cleaned_text = self.clean_text_for_tts(text)
        word_count = len(cleaned_text.split())
        estimated_minutes = word_count / 150  # ~150 words per minute
        print(f"  Text length: {len(cleaned_text)} characters, ~{word_count} words")
        print(f"  Estimated audio duration: ~{estimated_minutes:.1f} minutes")

        # Generate audio
        output_filename = filename.replace('.pdf', '.mp3')
        output_path = os.path.join(OUTPUT_DIR, output_filename)

        success = self.generate_audio(cleaned_text, output_path)

        if success:
            # Get file size
            size_mb = os.path.getsize(output_path) / (1024 * 1024)
            print(f"\n✓ Successfully created: {output_filename} ({size_mb:.2f} MB)")
        else:
            print(f"\n✗ Failed to create: {output_filename}")

        return success

async def list_available_voices():
    """List all available Spanish voices"""
    print("Available Spanish Voices:")
    print("=" * 60)

    voices = await edge_tts.list_voices()
    spanish_voices = [v for v in voices if v['Locale'].startswith('es-')]

    for voice in spanish_voices:
        print(f"  {voice['ShortName']}")
        print(f"    Language: {voice['Locale']}")
        print(f"    Gender: {voice['Gender']}")
        print(f"    Name: {voice['FriendlyName']}")
        print()

def main():
    """Main execution function"""
    print("Economics Transcript Audio Generator")
    print("=" * 60)
    print("Converting Spanish transcripts to MP3 audio...")
    print("=" * 60)

    # Create output directory
    os.makedirs(OUTPUT_DIR, exist_ok=True)

    # Get all PDF files
    pdf_files = list(Path(INPUT_DIR).glob("*.pdf"))

    if not pdf_files:
        print(f"\n⚠ No PDF files found in {INPUT_DIR}")
        print("Please run translate_transcripts.py first.")
        return

    print(f"\nFound {len(pdf_files)} PDF files to convert\n")
    print(f"Using voice: {DEFAULT_VOICE}")

    # Ask if user wants to see available voices
    print("\nTip: You can change the voice by editing the DEFAULT_VOICE in this script")
    print("To see all available voices, uncomment the list_voices line below\n")

    # Uncomment to list available voices:
    # asyncio.run(list_available_voices())

    # Process each transcript
    generator = AudioGenerator(voice=DEFAULT_VOICE)
    success_count = 0

    for pdf_file in pdf_files:
        try:
            if generator.process_transcript(str(pdf_file)):
                success_count += 1
        except Exception as e:
            print(f"\n✗ Error processing {pdf_file.name}: {e}")
            import traceback
            traceback.print_exc()

        print()  # Blank line between files

    # Summary
    print("=" * 60)
    print("Audio Generation Complete!")
    print("=" * 60)
    print(f"Successfully converted: {success_count}/{len(pdf_files)} files")
    print(f"Output directory: {OUTPUT_DIR}")

if __name__ == "__main__":
    main()
