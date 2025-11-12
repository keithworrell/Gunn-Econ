#!/usr/bin/env python3
"""
Economics Transcript Pipeline - Main Orchestration Script
Runs the complete pipeline: download -> translate -> generate audio
"""

import sys
import subprocess
import argparse
from pathlib import Path

def run_step(script_name, description):
    """Run a pipeline step and handle errors"""
    print(f"\n{'='*70}")
    print(f"STEP: {description}")
    print(f"{'='*70}\n")

    try:
        result = subprocess.run(
            [sys.executable, script_name],
            check=True,
            text=True
        )
        print(f"\n✓ {description} completed successfully\n")
        return True
    except subprocess.CalledProcessError as e:
        print(f"\n✗ {description} failed with error code {e.returncode}\n")
        return False
    except FileNotFoundError:
        print(f"\n✗ Script not found: {script_name}\n")
        return False

def check_dependencies():
    """Check if required packages are installed"""
    print("Checking dependencies...")

    required_packages = [
        'selenium',
        'beautifulsoup4',
        'requests',
        'pdfplumber',
        'deep_translator',
        'reportlab',
        'edge_tts',
        'tqdm'
    ]

    missing_packages = []

    for package in required_packages:
        try:
            __import__(package.replace('-', '_'))
        except ImportError:
            missing_packages.append(package)

    if missing_packages:
        print(f"\n⚠ Missing packages: {', '.join(missing_packages)}")
        print("\nPlease install dependencies first:")
        print("  pip install -r requirements.txt\n")
        return False

    print("✓ All dependencies installed\n")
    return True

def main():
    parser = argparse.ArgumentParser(
        description='Economics Transcript Processing Pipeline',
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  # Run complete pipeline
  python run_pipeline.py --all

  # Run only download step
  python run_pipeline.py --download

  # Run translation and audio generation
  python run_pipeline.py --translate --audio

  # Skip dependency check
  python run_pipeline.py --all --skip-check
        """
    )

    parser.add_argument('--all', action='store_true',
                       help='Run all steps (download, translate, audio)')
    parser.add_argument('--download', action='store_true',
                       help='Download transcripts only')
    parser.add_argument('--translate', action='store_true',
                       help='Translate transcripts only')
    parser.add_argument('--audio', action='store_true',
                       help='Generate audio only')
    parser.add_argument('--skip-check', action='store_true',
                       help='Skip dependency check')

    args = parser.parse_args()

    # If no flags, show help
    if not (args.all or args.download or args.translate or args.audio):
        parser.print_help()
        return

    print("="*70)
    print("ECONOMICS TRANSCRIPT PROCESSING PIPELINE")
    print("="*70)
    print()

    # Check dependencies
    if not args.skip_check:
        if not check_dependencies():
            sys.exit(1)

    # Determine which steps to run
    run_download = args.all or args.download
    run_translate = args.all or args.translate
    run_audio = args.all or args.audio

    # Execute pipeline
    steps_completed = 0
    steps_total = sum([run_download, run_translate, run_audio])

    if run_download:
        if run_step('download_transcripts.py', 'Download Transcripts'):
            steps_completed += 1
        else:
            print("⚠ Download step failed. Check errors above.")
            if not args.translate and not args.audio:
                sys.exit(1)

    if run_translate:
        # Check if we have transcripts to translate
        transcript_dir = Path('economics-spanish/original-transcripts')
        if not transcript_dir.exists() or not list(transcript_dir.glob('*.pdf')):
            print("\n⚠ No transcripts found to translate.")
            print("Please run with --download first.\n")
            sys.exit(1)

        if run_step('translate_transcripts.py', 'Translate to Spanish'):
            steps_completed += 1
        else:
            print("⚠ Translation step failed. Check errors above.")
            if not args.audio:
                sys.exit(1)

    if run_audio:
        # Check if we have Spanish transcripts
        spanish_dir = Path('economics-spanish/spanish-transcripts')
        if not spanish_dir.exists() or not list(spanish_dir.glob('*.pdf')):
            print("\n⚠ No Spanish transcripts found for audio generation.")
            print("Please run with --translate first.\n")
            sys.exit(1)

        if run_step('generate_audio.py', 'Generate Audio Files'):
            steps_completed += 1
        else:
            print("⚠ Audio generation step failed. Check errors above.")

    # Final summary
    print("\n" + "="*70)
    print("PIPELINE COMPLETE")
    print("="*70)
    print(f"Completed: {steps_completed}/{steps_total} steps")
    print("\nOutput directories:")
    print("  📄 Original transcripts: economics-spanish/original-transcripts/")
    print("  📄 Spanish transcripts:  economics-spanish/spanish-transcripts/")
    print("  🔊 Audio files:          economics-spanish/audio-files/")
    print()

if __name__ == "__main__":
    main()
