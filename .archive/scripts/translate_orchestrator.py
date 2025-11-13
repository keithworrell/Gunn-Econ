#!/usr/bin/env python3
"""
Translation Orchestrator - Run this from Claude Code
This script generates agent task specifications that Claude Code can execute
"""

import os
import json
from pathlib import Path

INPUT_DIR = "economics-spanish/markdown-english"
OUTPUT_DIR = "economics-spanish/markdown-spanish"
TASK_SPEC_FILE = "economics-spanish/translation-tasks.json"

TRANSLATION_PROMPT_TEMPLATE = """You are translating an Economics U$A transcript for Spanish-speaking high school ELL students.

# Input
Read the English transcript from: {input_file}

# Task

1. **Create an ELL-Optimized Header** with these sections (all in Spanish, markdown formatted):

   - **Resumen del Episodio**: 2-3 sentence overview
   - **Objetivos de Aprendizaje**: 3 bullet points starting with "Al final de este episodio, podrás..."
   - **Vocabulario Clave**:
     - Table with columns: Término Español | English Term | Definición | Ejemplo en Contexto
     - Include 5-8 key economic terms
     - Add a "Cognados Útiles" subsection listing Spanish-English cognates
   - **Conceptos Fundamentales**: 2-3 main concepts, each with:
     - ¿Qué es?
     - ¿Por qué importa?
     - Ejemplo cotidiano
   - **Conexión con Tu Vida**: 1-2 relatable scenarios
   - **Preguntas para Reflexionar**: 2 questions before reading, 2 questions after reading

2. **Translate the Transcript**:
   - Natural, clear Spanish for high school level
   - Maintain all markdown formatting
   - Use standard Spanish economic terminology
   - Keep page break comments like `<!-- Page 2 -->`

3. **Output**: Write the complete markdown (header + transcript) to: {output_file}

Use icons for visual hierarchy: 📚 📖 🎯 🔑 💡 🌎 ❓
"""

def generate_task_specs():
    """Generate task specifications for all markdown files"""

    print("Translation Orchestrator")
    print("=" * 70)

    os.makedirs(OUTPUT_DIR, exist_ok=True)

    # Get all markdown files
    md_files = list(Path(INPUT_DIR).glob("*.md"))

    if not md_files:
        print(f"No markdown files found in {INPUT_DIR}")
        print("Run: python pdf_to_markdown.py first")
        return []

    print(f"Found {len(md_files)} transcripts to translate\n")

    tasks = []

    for md_file in md_files:
        output_filename = md_file.stem + "-spanish.md"
        output_path = os.path.join(OUTPUT_DIR, output_filename)

        task = {
            'name': md_file.stem,
            'input_file': str(md_file),
            'output_file': output_path,
            'prompt': TRANSLATION_PROMPT_TEMPLATE.format(
                input_file=str(md_file),
                output_file=output_path
            )
        }

        tasks.append(task)
        print(f"  ✓ Task prepared: {md_file.name}")

    # Save task specifications
    with open(TASK_SPEC_FILE, 'w', encoding='utf-8') as f:
        json.dump(tasks, f, indent=2, ensure_ascii=False)

    print(f"\n{'='*70}")
    print(f"Task specifications saved to: {TASK_SPEC_FILE}")
    print(f"Total translation tasks: {len(tasks)}")
    print(f"{'='*70}")

    return tasks

def print_instructions(tasks):
    """Print instructions for running via Claude Code"""

    print("\n" + "="*70)
    print("HOW TO RUN TRANSLATIONS")
    print("="*70)

    print("\n📋 Method 1: From Claude Code (Recommended)")
    print("-" * 70)
    print("""
Ask Claude Code to:

"Read translation-tasks.json and launch Task agents in parallel to translate
all transcripts. Launch 5 agents at a time, then launch the next batch."

Claude will:
- Read the task specifications
- Launch multiple Task agents in parallel
- Each agent translates one transcript with ELL header
- Saves output to economics-spanish/markdown-spanish/
""")

    print("\n📋 Method 2: Individual Files")
    print("-" * 70)
    print("""
For each file, ask Claude Code:

"Launch a Task agent to translate [filename]. Read the prompt from
translation-tasks.json entry [number]."
""")

    print("\n📋 Method 3: Manual Copy-Paste")
    print("-" * 70)
    print("""
1. Open translation-tasks.json
2. Copy the 'prompt' field for a task
3. Paste it directly to Claude Code
4. Claude will read the input, translate, and write output
""")

    print("\n" + "="*70)
    print(f"✓ Ready to translate {len(tasks)} transcripts!")
    print("="*70)

def main():
    tasks = generate_task_specs()

    if tasks:
        print_instructions(tasks)
        print("\n💡 Tip: Parallel translation with 5 agents takes ~10-15 minutes total")
    else:
        print("\n❌ No tasks generated. Check that markdown files exist.")

if __name__ == "__main__":
    main()
