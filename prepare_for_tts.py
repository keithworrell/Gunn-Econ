#!/usr/bin/env python3
"""
Prepare Spanish transcripts for Text-to-Speech.

Converts markdown formatting to natural speech with SSML tags for optimal
narration quality using Microsoft Edge TTS.
"""

import re
from pathlib import Path
from tqdm import tqdm


def remove_emojis(text):
    """Remove emoji characters from text."""
    emoji_pattern = re.compile(
        "["
        "\U0001F600-\U0001F64F"  # emoticons
        "\U0001F300-\U0001F5FF"  # symbols & pictographs
        "\U0001F680-\U0001F6FF"  # transport & map symbols
        "\U0001F1E0-\U0001F1FF"  # flags
        "\U00002702-\U000027B0"
        "\U000024C2-\U0001F251"
        "]+",
        flags=re.UNICODE,
    )
    return emoji_pattern.sub("", text)


def convert_vocabulary_table_to_speech(match):
    """Convert a vocabulary table to natural speech."""
    table_text = match.group(0)
    lines = table_text.strip().split("\n")
    speech_parts = []

    speech_parts.append('<break time="500ms"/>Vocabulario Clave.<break time="500ms"/>')

    for line in lines:
        # Skip header and separator lines
        if not line.strip() or "---" in line or "Término Español" in line:
            continue

        # Parse table cells
        cells = [cell.strip() for cell in line.split("|") if cell.strip()]

        if len(cells) >= 4:
            spanish_term = re.sub(r"[*_]", "", cells[0])
            english_term = re.sub(r"[*_]", "", cells[1])
            definition = re.sub(r"[*_]", "", cells[2])
            example = re.sub(r"[*_]", "", cells[3])

            speech = (
                f'<break time="300ms"/>{spanish_term}. '
                f'<prosody rate="95%">En inglés: {english_term}</prosody>. '
                f'<break time="200ms"/>Definición: {definition}. '
                f'<break time="200ms"/>Ejemplo: {example}.<break time="500ms"/>'
            )
            speech_parts.append(speech)

    speech_parts.append('<break time="1s"/>')
    return "\n".join(speech_parts)


def escape_xml(text):
    """Escape XML special characters."""
    text = text.replace("&", "&amp;")
    text = text.replace("<", "&lt;")
    text = text.replace(">", "&gt;")
    text = text.replace('"', "&quot;")
    text = text.replace("'", "&apos;")
    return text


def markdown_to_speech(markdown_content):
    """Convert markdown transcript to speech-optimized text with SSML."""
    content = markdown_content

    # Remove page break comments
    content = re.sub(r"<!--.*?-->", "", content)

    # Remove horizontal rule separators (---)
    content = re.sub(r"^---+\s*$", "", content, flags=re.MULTILINE)

    # Convert vocabulary table BEFORE removing emojis (match with or without emoji)
    content = re.sub(
        r"##\s+(?:🔑\s+)?Vocabulario Clave\s*\n\n\|.*?\n\|[-:\s|]+\n(\|.*?\n)+",
        convert_vocabulary_table_to_speech,
        content,
        flags=re.MULTILINE | re.DOTALL,
    )

    # Remove emojis
    content = remove_emojis(content)

    # Remove any remaining table syntax that wasn't caught
    content = re.sub(r"\|[-:\s|]+\|", "", content)

    # Convert headers with emphasis
    content = re.sub(
        r"^#{1,2}\s+(.+?)$",
        lambda m: f'<break time="800ms"/><emphasis level="moderate">{m.group(1).strip()}</emphasis><break time="500ms"/>',
        content,
        flags=re.MULTILINE,
    )

    # Convert ### headers (smaller headers)
    content = re.sub(
        r"^###\s+(.+?)$",
        lambda m: f'<break time="500ms"/><prosody rate="95%">{m.group(1).strip()}</prosody><break time="500ms"/>',
        content,
        flags=re.MULTILINE,
    )

    # Convert bullet points
    content = re.sub(r"^[-•]\s+", "", content, flags=re.MULTILINE)

    # Remove bold/italic formatting
    content = re.sub(r"\*\*(.+?)\*\*", r"\1", content)
    content = re.sub(r"\*(.+?)\*", r"\1", content)
    content = re.sub(r"_(.+?)_", r"\1", content)

    # Add breaks at sentence endings
    content = re.sub(r"([.!?])\s+", r'\1<break time="400ms"/> ', content)

    # Add breaks after paragraphs
    content = re.sub(r"\n\n+", '<break time="600ms"/>\n', content)

    # Clean up multiple breaks
    content = re.sub(r'(<break time="\d+ms"/>[\s\n]*){3,}', '<break time="1s"/>', content)

    # Clean up any leftover empty lines
    content = re.sub(r'\n\s*\n\s*\n+', '\n\n', content)

    # Wrap in SSML speak tag
    ssml = f'<speak version="1.0" xmlns="http://www.w3.org/2001/10/synthesis" xml:lang="es-MX">\n{content}\n</speak>'

    return ssml


def process_all_transcripts():
    """Process all Spanish markdown transcripts for TTS."""
    input_dir = Path("economics-spanish/markdown-spanish")
    output_dir = Path("economics-spanish/tts-prepared")
    output_dir.mkdir(exist_ok=True)

    markdown_files = sorted(input_dir.glob("*-spanish.md"))

    print("Preparing Spanish Transcripts for TTS")
    print("=" * 70)
    print(f"Found {len(markdown_files)} files to process\n")

    for md_file in tqdm(markdown_files, desc="Processing"):
        # Read markdown
        markdown_content = md_file.read_text(encoding="utf-8")

        # Convert to speech-optimized SSML
        speech_text = markdown_to_speech(markdown_content)

        # Save to output directory
        output_file = output_dir / md_file.name.replace(".md", ".ssml")
        output_file.write_text(speech_text, encoding="utf-8")

    print("\n" + "=" * 70)
    print("Preprocessing Complete!")
    print(f"Processed: {len(markdown_files)}/{len(markdown_files)} files")
    print(f"Output directory: {output_dir}")


if __name__ == "__main__":
    process_all_transcripts()
