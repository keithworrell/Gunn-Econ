#!/usr/bin/env python3
"""
Markdown to PDF Converter
Converts Spanish markdown transcripts with ELL headers into formatted PDFs
"""

import os
from pathlib import Path
from reportlab.lib.pagesizes import letter
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.units import inch
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, PageBreak, Table, TableStyle
from reportlab.lib.enums import TA_LEFT, TA_CENTER, TA_JUSTIFY
from reportlab.lib import colors
from tqdm import tqdm

INPUT_DIR = "economics-spanish/markdown-spanish"
OUTPUT_DIR = "economics-spanish/spanish-transcripts"

def markdown_to_pdf(md_file, output_file):
    """Convert a markdown file to a formatted PDF"""

    # Read markdown
    with open(md_file, 'r', encoding='utf-8') as f:
        md_content = f.read()

    # Create PDF
    doc = SimpleDocTemplate(
        output_file,
        pagesize=letter,
        rightMargin=0.75*inch,
        leftMargin=0.75*inch,
        topMargin=0.75*inch,
        bottomMargin=0.75*inch,
    )

    # Styles
    styles = getSampleStyleSheet()

    # Custom styles for Spanish text
    title_style = ParagraphStyle(
        'Title',
        parent=styles['Heading1'],
        fontSize=18,
        textColor=colors.HexColor('#1a1a1a'),
        spaceAfter=20,
        spaceBefore=10,
        alignment=TA_CENTER,
        fontName='Helvetica-Bold'
    )

    h2_style = ParagraphStyle(
        'Heading2',
        parent=styles['Heading2'],
        fontSize=14,
        textColor=colors.HexColor('#2c3e50'),
        spaceAfter=12,
        spaceBefore=16,
        fontName='Helvetica-Bold'
    )

    h3_style = ParagraphStyle(
        'Heading3',
        parent=styles['Heading3'],
        fontSize=12,
        textColor=colors.HexColor('#34495e'),
        spaceAfter=8,
        spaceBefore=12,
        fontName='Helvetica-Bold'
    )

    body_style = ParagraphStyle(
        'Body',
        parent=styles['BodyText'],
        fontSize=11,
        textColor=colors.HexColor('#2c3e50'),
        alignment=TA_JUSTIFY,
        spaceAfter=10,
        leading=14,
        fontName='Helvetica'
    )

    bullet_style = ParagraphStyle(
        'Bullet',
        parent=body_style,
        leftIndent=20,
        bulletIndent=10,
        spaceAfter=6,
    )

    # Build story
    story = []

    # Parse markdown into sections
    lines = md_content.split('\n')
    i = 0

    while i < len(lines):
        line = lines[i].strip()

        # Skip empty lines at start
        if not line:
            i += 1
            continue

        # Main title (# )
        if line.startswith('# '):
            title_text = line[2:].strip()
            story.append(Paragraph(title_text, title_style))
            story.append(Spacer(1, 0.2*inch))

        # H2 (## )
        elif line.startswith('## '):
            h2_text = line[3:].strip()
            story.append(Spacer(1, 0.15*inch))
            story.append(Paragraph(h2_text, h2_style))

        # H3 (### )
        elif line.startswith('### '):
            h3_text = line[4:].strip()
            story.append(Paragraph(h3_text, h3_style))

        # Horizontal rule
        elif line.startswith('---'):
            story.append(Spacer(1, 0.1*inch))

        # Bullet points
        elif line.startswith('- ') or line.startswith('* '):
            bullet_text = line[2:].strip()
            story.append(Paragraph(f"• {bullet_text}", bullet_style))

        # Tables (simplified - just format as text for now)
        elif line.startswith('|'):
            # Collect table rows
            table_lines = []
            while i < len(lines) and lines[i].strip().startswith('|'):
                table_lines.append(lines[i].strip())
                i += 1
            i -= 1  # Back up one

            # Format table as indented text
            for table_line in table_lines:
                if '---' not in table_line:  # Skip separator row
                    cells = [cell.strip() for cell in table_line.split('|')[1:-1]]
                    formatted_row = ' | '.join(cells)
                    story.append(Paragraph(formatted_row, bullet_style))

        # Page breaks
        elif line.startswith('<!-- Page'):
            story.append(PageBreak())

        # Regular paragraphs
        elif line and not line.startswith('<!--'):
            # Remove markdown bold/italic for PDF
            clean_text = line.replace('**', '').replace('*', '')
            story.append(Paragraph(clean_text, body_style))

        i += 1

    # Build PDF
    doc.build(story)

def process_all_markdown():
    """Convert all Spanish markdown files to PDFs"""

    print("Markdown to PDF Converter")
    print("=" * 70)

    os.makedirs(OUTPUT_DIR, exist_ok=True)

    # Get all markdown files
    md_files = list(Path(INPUT_DIR).glob("*.md"))

    if not md_files:
        print(f"No markdown files found in {INPUT_DIR}")
        print("Run translation first!")
        return

    print(f"Found {len(md_files)} markdown files to convert\n")

    success_count = 0

    for md_file in tqdm(md_files, desc="Converting"):
        try:
            output_filename = md_file.stem + ".pdf"
            output_path = os.path.join(OUTPUT_DIR, output_filename)

            markdown_to_pdf(md_file, output_path)

            success_count += 1
            print(f"  ✓ {output_filename}")

        except Exception as e:
            print(f"  ✗ {md_file.name}: {e}")
            import traceback
            traceback.print_exc()

    print("\n" + "=" * 70)
    print(f"Conversion Complete!")
    print(f"Successfully converted: {success_count}/{len(md_files)} files")
    print(f"Output directory: {OUTPUT_DIR}")

if __name__ == "__main__":
    process_all_markdown()
