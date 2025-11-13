#!/usr/bin/env python3
"""
Process Episode 4 - Complete pipeline for Perfect Competition and Inelastic Demand
"""

import sys
import os
from pathlib import Path
import pdfplumber
from deep_translator import GoogleTranslator
from reportlab.lib.pagesizes import letter
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer
from reportlab.lib.units import inch
import asyncio
import edge_tts

# Setup paths
ROOT_DIR = Path(__file__).parent.parent.parent
EPISODE_FOLDER = ROOT_DIR / "04-Perfect-Competition-and-Inelastic-Demand"
INTERMEDIATE_DIR = ROOT_DIR / ".archive" / "intermediate-files"

# Episode 4 file info
EPISODE_NUM = "04"
EPISODE_SLUG = "perfect-competition-inelastic-demand"

def pdf_to_text(pdf_path):
    """Extract text from PDF"""
    print(f"[INFO] Extracting text from {pdf_path.name}...")
    text_content = []

    with pdfplumber.open(pdf_path) as pdf:
        for page in pdf.pages:
            text = page.extract_text()
            if text:
                text_content.append(text)

    return "\n\n".join(text_content)

def translate_text(text, max_chunk_size=4500):
    """Translate English text to Spanish in chunks"""
    print("[INFO] Translating to Spanish...")

    # Split into sentences to avoid breaking mid-sentence
    sentences = text.replace('\n\n', '\n').split('\n')
    chunks = []
    current_chunk = []
    current_size = 0

    for sentence in sentences:
        sentence_size = len(sentence)
        if current_size + sentence_size > max_chunk_size and current_chunk:
            chunks.append('\n'.join(current_chunk))
            current_chunk = [sentence]
            current_size = sentence_size
        else:
            current_chunk.append(sentence)
            current_size += sentence_size

    if current_chunk:
        chunks.append('\n'.join(current_chunk))

    # Translate each chunk
    translator = GoogleTranslator(source='en', target='es')
    translated_chunks = []

    for i, chunk in enumerate(chunks, 1):
        print(f"  Translating chunk {i}/{len(chunks)}...")
        translated = translator.translate(chunk)
        translated_chunks.append(translated)

    return '\n\n'.join(translated_chunks)

def text_to_pdf(text, output_path, title=""):
    """Convert text to PDF"""
    print(f"[INFO] Creating PDF: {output_path.name}...")

    doc = SimpleDocTemplate(
        str(output_path),
        pagesize=letter,
        rightMargin=72,
        leftMargin=72,
        topMargin=72,
        bottomMargin=18,
    )

    styles = getSampleStyleSheet()
    styles.add(ParagraphStyle(
        name='CustomBody',
        parent=styles['BodyText'],
        fontSize=11,
        leading=14,
        spaceAfter=12
    ))

    story = []

    # Add title if provided
    if title:
        story.append(Paragraph(title, styles['Title']))
        story.append(Spacer(1, 0.2*inch))

    # Add content paragraphs
    for para in text.split('\n\n'):
        if para.strip():
            story.append(Paragraph(para.strip(), styles['CustomBody']))
            story.append(Spacer(1, 0.1*inch))

    doc.build(story)

async def text_to_speech(text, output_path):
    """Convert text to speech using edge-tts"""
    print(f"[INFO] Generating audio: {output_path.name}...")

    # Clean text for TTS
    clean_text = text.replace('\n\n', '. ').replace('\n', ' ')

    # Use Spanish voice
    voice = "es-ES-ElviraNeural"
    communicate = edge_tts.Communicate(clean_text, voice)
    await communicate.save(str(output_path))

def process_transcript(transcript_type):
    """Process a single transcript (video or audio)"""
    print(f"\n{'='*70}")
    print(f"Processing {transcript_type} transcript for Episode 4")
    print(f"{'='*70}\n")

    # File paths
    english_pdf = EPISODE_FOLDER / f"{EPISODE_NUM}-{EPISODE_SLUG}-{transcript_type}.pdf"
    spanish_pdf = EPISODE_FOLDER / f"{EPISODE_NUM}-{EPISODE_SLUG}-{transcript_type}-spanish.pdf"
    spanish_mp3 = EPISODE_FOLDER / f"{EPISODE_NUM}-{EPISODE_SLUG}-{transcript_type}-spanish-spanish.mp3"

    # Step 1: Extract English text from PDF
    english_text = pdf_to_text(english_pdf)

    # Step 2: Translate to Spanish
    spanish_text = translate_text(english_text)

    # Step 3: Create Spanish PDF
    text_to_pdf(spanish_text, spanish_pdf, f"Economics USA - Episode 4 - {transcript_type.title()} (Español)")

    # Step 4: Generate Spanish audio
    asyncio.run(text_to_speech(spanish_text, spanish_mp3))

    print(f"\n[OK] Completed {transcript_type} transcript processing\n")

def main():
    print("""
======================================================================
Episode 4 Processing Pipeline
Perfect Competition and Inelastic Demand
======================================================================
""")

    # Verify Episode 4 folder exists
    if not EPISODE_FOLDER.exists():
        print(f"[FAIL] Episode 4 folder not found: {EPISODE_FOLDER}")
        sys.exit(1)

    # Process video transcript
    try:
        process_transcript("video")
    except Exception as e:
        print(f"[FAIL] Error processing video transcript: {e}")
        import traceback
        traceback.print_exc()
        sys.exit(1)

    # Process audio transcript
    try:
        process_transcript("audio")
    except Exception as e:
        print(f"[FAIL] Error processing audio transcript: {e}")
        import traceback
        traceback.print_exc()
        sys.exit(1)

    print("""
======================================================================
Episode 4 Processing Complete!
======================================================================

Generated files:
- 04-perfect-competition-inelastic-demand-video-spanish.pdf
- 04-perfect-competition-inelastic-demand-audio-spanish.pdf
- 04-perfect-competition-inelastic-demand-video-spanish-spanish.mp3
- 04-perfect-competition-inelastic-demand-audio-spanish-spanish.mp3
""")

if __name__ == "__main__":
    main()
