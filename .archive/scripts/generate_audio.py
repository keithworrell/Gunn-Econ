#!/usr/bin/env python3
"""
Economics Transcript Audio Generator
Converts Spanish transcripts to MP3 audio files using Microsoft Edge TTS with SSML
"""

import os
import asyncio
from pathlib import Path
import edge_tts
from tqdm import tqdm

# Constants
INPUT_DIR = "economics-spanish/tts-plain-text"
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

    async def generate_audio_async(self, text, output_path):
        """Generate audio file from plain text using Edge TTS"""
        try:
            # Create TTS communicator with plain text
            communicate = edge_tts.Communicate(text, self.voice)

            # Generate and save audio
            await communicate.save(output_path)
            return True

        except Exception as e:
            print(f"  ✗ Error generating audio: {e}")
            return False

    def generate_audio(self, text, output_path):
        """Synchronous wrapper for audio generation"""
        return asyncio.run(self.generate_audio_async(text, output_path))

    def process_transcript(self, txt_path):
        """Process a single transcript: read plain text and generate audio"""
        filename = os.path.basename(txt_path)

        # Read plain text
        try:
            with open(txt_path, 'r', encoding='utf-8') as f:
                text = f.read()
        except Exception as e:
            print(f"  ✗ Error reading text file: {e}")
            return False

        # Estimate duration (rough approximation)
        word_count = len(text.split())
        estimated_minutes = word_count / 150  # ~150 words per minute

        # Generate audio
        output_filename = filename.replace('.txt', '-spanish.mp3')
        output_path = os.path.join(OUTPUT_DIR, output_filename)

        success = self.generate_audio(text, output_path)

        if success:
            # Get file size
            size_mb = os.path.getsize(output_path) / (1024 * 1024)
            return {
                'success': True,
                'filename': output_filename,
                'size_mb': size_mb,
                'estimated_minutes': estimated_minutes
            }
        else:
            return {'success': False, 'filename': output_filename}

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
    print("=" * 70)
    print("Converting Spanish transcripts to MP3 audio (plain text)...")
    print("=" * 70)

    # Create output directory
    os.makedirs(OUTPUT_DIR, exist_ok=True)

    # Get all TXT files
    txt_files = sorted(Path(INPUT_DIR).glob("*.txt"))

    if not txt_files:
        print(f"\n⚠ No TXT files found in {INPUT_DIR}")
        print("Please run convert_ssml_to_plain.py first.")
        return

    print(f"\nFound {len(txt_files)} text files to convert")
    print(f"Using voice: {DEFAULT_VOICE}\n")

    # Process each transcript with progress bar
    generator = AudioGenerator(voice=DEFAULT_VOICE)
    results = []

    for txt_file in tqdm(txt_files, desc="Generating audio"):
        try:
            result = generator.process_transcript(str(txt_file))
            if result:
                results.append(result)
        except Exception as e:
            print(f"\n✗ Error processing {txt_file.name}: {e}")
            import traceback
            traceback.print_exc()

    # Summary
    success_count = sum(1 for r in results if r.get('success'))
    total_size_mb = sum(r.get('size_mb', 0) for r in results if r.get('success'))
    total_minutes = sum(r.get('estimated_minutes', 0) for r in results if r.get('success'))

    print("\n" + "=" * 70)
    print("Audio Generation Complete!")
    print("=" * 70)
    print(f"Successfully converted: {success_count}/{len(txt_files)} files")
    print(f"Total size: {total_size_mb:.1f} MB")
    print(f"Estimated total duration: ~{total_minutes:.0f} minutes ({total_minutes/60:.1f} hours)")
    print(f"Output directory: {OUTPUT_DIR}")

if __name__ == "__main__":
    main()
