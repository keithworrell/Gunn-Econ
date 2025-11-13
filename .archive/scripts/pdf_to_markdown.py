#!/usr/bin/env python3
"""
PDF to Markdown Converter
Extracts text from Economics USA transcripts and converts to clean markdown
"""

import os
import pdfplumber
from pathlib import Path
from tqdm import tqdm

INPUT_DIR = "economics-spanish/original-transcripts"
OUTPUT_DIR = "economics-spanish/markdown-english"

def extract_pdf_to_markdown(pdf_path):
    """Extract PDF text and convert to markdown format"""

    markdown_content = []

    try:
        with pdfplumber.open(pdf_path) as pdf:
            for page_num, page in enumerate(pdf.pages, 1):
                text = page.extract_text()

                if text:
                    # Split into lines
                    lines = text.split('\n')

                    for line in lines:
                        line = line.strip()
                        if not line:
                            markdown_content.append("")
                            continue

                        # Detect headers (all caps, short lines)
                        if line.isupper() and len(line) < 100 and not line.isdigit():
                            # Main title
                            if len(line.split()) <= 5:
                                markdown_content.append(f"# {line.title()}")
                            else:
                                markdown_content.append(f"## {line.title()}")
                            markdown_content.append("")

                        # Detect section headers (title case, short lines)
                        elif len(line) < 100 and line[0].isupper() and line.count(' ') < 8:
                            # Check if likely a header vs regular sentence
                            if not line.endswith('.') and not line.endswith(','):
                                markdown_content.append(f"### {line}")
                                markdown_content.append("")
                            else:
                                markdown_content.append(line)

                        # Regular paragraph text
                        else:
                            markdown_content.append(line)

                    # Add page break indicator (as comment)
                    if page_num < len(pdf.pages):
                        markdown_content.append("")
                        markdown_content.append(f"<!-- Page {page_num + 1} -->")
                        markdown_content.append("")

        return '\n'.join(markdown_content)

    except Exception as e:
        print(f"Error processing PDF: {e}")
        return None

def clean_markdown(content):
    """Clean up markdown formatting"""
    lines = content.split('\n')
    cleaned = []
    prev_empty = False

    for line in lines:
        # Remove excessive blank lines
        if not line.strip():
            if not prev_empty:
                cleaned.append("")
                prev_empty = True
        else:
            cleaned.append(line)
            prev_empty = False

    return '\n'.join(cleaned)

def process_all_pdfs():
    """Process all PDFs in the input directory"""
    print("PDF to Markdown Converter")
    print("=" * 70)

    os.makedirs(OUTPUT_DIR, exist_ok=True)

    # Get all PDF files
    pdf_files = list(Path(INPUT_DIR).glob("*.pdf"))

    if not pdf_files:
        print(f"No PDF files found in {INPUT_DIR}")
        return

    print(f"Found {len(pdf_files)} PDF files to convert\n")

    success_count = 0

    for pdf_file in tqdm(pdf_files, desc="Converting"):
        try:
            # Extract to markdown
            markdown_content = extract_pdf_to_markdown(pdf_file)

            if markdown_content:
                # Clean up
                markdown_content = clean_markdown(markdown_content)

                # Save markdown file
                output_filename = pdf_file.stem + ".md"
                output_path = os.path.join(OUTPUT_DIR, output_filename)

                with open(output_path, 'w', encoding='utf-8') as f:
                    f.write(markdown_content)

                success_count += 1
                print(f"  ✓ {output_filename}")

        except Exception as e:
            print(f"  ✗ {pdf_file.name}: {e}")

    print("\n" + "=" * 70)
    print(f"Conversion Complete!")
    print(f"Successfully converted: {success_count}/{len(pdf_files)} files")
    print(f"Output directory: {OUTPUT_DIR}")

if __name__ == "__main__":
    process_all_pdfs()
