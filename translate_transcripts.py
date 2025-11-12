#!/usr/bin/env python3
"""
Economics Transcript Translator
Translates PDF transcripts from English to Spanish while preserving formatting
"""

import os
import time
from pathlib import Path
import pdfplumber
from deep_translator import GoogleTranslator
from reportlab.lib.pagesizes import letter
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.units import inch
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, PageBreak
from reportlab.lib.enums import TA_LEFT, TA_CENTER, TA_JUSTIFY
from tqdm import tqdm

# Constants
INPUT_DIR = "economics-spanish/original-transcripts"
OUTPUT_DIR = "economics-spanish/spanish-transcripts"

class TranscriptTranslator:
    def __init__(self):
        self.translator = GoogleTranslator(source='en', target='es')

    def extract_text_from_pdf(self, pdf_path):
        """Extract text from PDF while preserving structure"""
        print(f"  Extracting text from PDF...")

        text_blocks = []

        try:
            with pdfplumber.open(pdf_path) as pdf:
                for page_num, page in enumerate(pdf.pages, 1):
                    # Extract text
                    text = page.extract_text()

                    if text:
                        # Split into paragraphs (separated by blank lines)
                        paragraphs = text.split('\n\n')
                        for para in paragraphs:
                            para = para.strip()
                            if para:
                                # Detect if it's likely a header (short, all caps, etc.)
                                is_header = (
                                    len(para) < 100 and
                                    (para.isupper() or para.count('\n') == 0)
                                )

                                text_blocks.append({
                                    'text': para.replace('\n', ' '),
                                    'type': 'header' if is_header else 'paragraph',
                                    'page': page_num
                                })

            print(f"  ✓ Extracted {len(text_blocks)} text blocks from {len(pdf.pages)} pages")
            return text_blocks

        except Exception as e:
            print(f"  ✗ Error extracting text: {e}")
            return []

    def translate_text_blocks(self, text_blocks):
        """Translate text blocks to Spanish"""
        print(f"  Translating {len(text_blocks)} text blocks to Spanish...")

        translated_blocks = []

        for i, block in enumerate(tqdm(text_blocks, desc="  Translating", leave=False)):
            try:
                # Translate in chunks if text is too long
                text = block['text']
                if len(text) > 4500:  # Google Translator limit
                    # Split into sentences and translate in batches
                    sentences = text.split('. ')
                    translated_sentences = []

                    for sentence in sentences:
                        if sentence.strip():
                            translated = self.translator.translate(sentence)
                            translated_sentences.append(translated)
                            time.sleep(0.1)  # Rate limiting

                    translated_text = '. '.join(translated_sentences)
                else:
                    translated_text = self.translator.translate(text)
                    time.sleep(0.1)  # Rate limiting

                translated_blocks.append({
                    'text': translated_text,
                    'type': block['type'],
                    'page': block['page']
                })

            except Exception as e:
                print(f"\n  ⚠ Translation error for block {i+1}: {e}")
                # Keep original text if translation fails
                translated_blocks.append(block)

        print(f"  ✓ Translation complete")
        return translated_blocks

    def create_pdf(self, text_blocks, output_path, original_filename):
        """Generate a new PDF with translated text"""
        print(f"  Generating Spanish PDF...")

        try:
            # Create PDF document
            doc = SimpleDocTemplate(
                output_path,
                pagesize=letter,
                rightMargin=72,
                leftMargin=72,
                topMargin=72,
                bottomMargin=18,
            )

            # Define styles
            styles = getSampleStyleSheet()

            # Custom styles
            title_style = ParagraphStyle(
                'CustomTitle',
                parent=styles['Heading1'],
                fontSize=16,
                textColor='#000000',
                spaceAfter=30,
                alignment=TA_CENTER,
            )

            header_style = ParagraphStyle(
                'CustomHeader',
                parent=styles['Heading2'],
                fontSize=12,
                textColor='#000000',
                spaceAfter=12,
                spaceBefore=12,
                alignment=TA_LEFT,
            )

            body_style = ParagraphStyle(
                'CustomBody',
                parent=styles['BodyText'],
                fontSize=10,
                textColor='#000000',
                alignment=TA_JUSTIFY,
                spaceAfter=12,
            )

            # Build content
            story = []

            # Add title
            title_text = f"Transcripción en Español<br/>{original_filename}"
            story.append(Paragraph(title_text, title_style))
            story.append(Spacer(1, 0.2*inch))

            # Add text blocks
            current_page = 1
            for block in text_blocks:
                # Add page break if needed
                if block['page'] > current_page and len(story) > 2:
                    story.append(PageBreak())
                    current_page = block['page']

                # Add paragraph
                if block['type'] == 'header':
                    story.append(Paragraph(block['text'], header_style))
                else:
                    story.append(Paragraph(block['text'], body_style))

            # Build PDF
            doc.build(story)
            print(f"  ✓ PDF created successfully")
            return True

        except Exception as e:
            print(f"  ✗ Error creating PDF: {e}")
            import traceback
            traceback.print_exc()
            return False

    def process_transcript(self, pdf_path):
        """Process a single transcript: extract, translate, and create new PDF"""
        filename = os.path.basename(pdf_path)
        print(f"\n{'='*60}")
        print(f"Processing: {filename}")
        print(f"{'='*60}")

        # Extract text
        text_blocks = self.extract_text_from_pdf(pdf_path)
        if not text_blocks:
            print("  ✗ No text extracted, skipping...")
            return False

        # Translate
        translated_blocks = self.translate_text_blocks(text_blocks)

        # Generate Spanish PDF
        output_filename = filename.replace('.pdf', '-spanish.pdf')
        output_path = os.path.join(OUTPUT_DIR, output_filename)

        success = self.create_pdf(translated_blocks, output_path, filename)

        if success:
            print(f"\n✓ Successfully created: {output_filename}")
        else:
            print(f"\n✗ Failed to create: {output_filename}")

        return success

def main():
    """Main execution function"""
    print("Economics Transcript Translator")
    print("=" * 60)
    print("Translating English transcripts to Spanish...")
    print("=" * 60)

    # Create output directory
    os.makedirs(OUTPUT_DIR, exist_ok=True)

    # Get all PDF files
    pdf_files = list(Path(INPUT_DIR).glob("*.pdf"))

    if not pdf_files:
        print(f"\n⚠ No PDF files found in {INPUT_DIR}")
        print("Please run download_transcripts.py first.")
        return

    print(f"\nFound {len(pdf_files)} PDF files to translate\n")

    # Process each transcript
    translator = TranscriptTranslator()
    success_count = 0

    for pdf_file in pdf_files:
        try:
            if translator.process_transcript(str(pdf_file)):
                success_count += 1
        except Exception as e:
            print(f"\n✗ Error processing {pdf_file.name}: {e}")
            import traceback
            traceback.print_exc()

        print()  # Blank line between files

    # Summary
    print("=" * 60)
    print("Translation Complete!")
    print("=" * 60)
    print(f"Successfully translated: {success_count}/{len(pdf_files)} files")
    print(f"Output directory: {OUTPUT_DIR}")

if __name__ == "__main__":
    main()
