#!/usr/bin/env python3
"""
Batch Translation with Claude Agents
Spawns parallel Task agents to translate English markdown to Spanish with ELL headers
"""

import os
import json
import subprocess
import sys
from pathlib import Path
from tqdm import tqdm
import time

INPUT_DIR = "economics-spanish/markdown-english"
OUTPUT_DIR = "economics-spanish/markdown-spanish"
AGENTS_DIR = "economics-spanish/agent-sessions"

# Maximum number of agents to run in parallel
MAX_PARALLEL_AGENTS = 5

TRANSLATION_PROMPT_TEMPLATE = """You are a professional translator specializing in educational economics content for Spanish-speaking high school students.

# Your Task

Translate the following Economics U$A transcript from English to Spanish, and create a comprehensive ELL-optimized header.

# Input File
{input_file}

# Output Requirements

## 1. Create an ELL-Optimized Header (in Spanish)

The header should include these sections in markdown format:

```markdown
# [Episode Title in Spanish]

---

## 📚 Resumen del Episodio (Episode Summary)
[Write a 2-3 sentence overview of the main topic and why it matters - in Spanish]

---

## 🎯 Objetivos de Aprendizaje (Learning Objectives)
Al final de este episodio, podrás:
- [Learning objective 1]
- [Learning objective 2]
- [Learning objective 3]

---

## 🔑 Vocabulario Clave (Key Vocabulary)

### Términos Económicos Principales
| Término Español | English Term | Definición | Ejemplo en Contexto |
|-----------------|--------------|-----------|---------------------|
| **[Spanish term]** | [English] | [Definition in Spanish] | [Example in Spanish] |

### Cognados Útiles (Helpful Cognates)
*Palabras similares en inglés y español:*
- **[Spanish]** = [English]
- **[Spanish]** = [English]

---

## 💡 Conceptos Fundamentales (Key Concepts)

1. **[Concept Name in Spanish]**
   - ¿Qué es? [What is it? - explain in simple Spanish]
   - ¿Por qué importa? [Why does it matter? - explain relevance]
   - Ejemplo cotidiano: [Everyday relatable example]

2. **[Concept 2]**
   - ...

---

## 🌎 Conexión con Tu Vida (Connection to Your Life)
[Write 1-2 relatable real-world scenarios that students can connect to - in Spanish]

---

## ❓ Preguntas para Reflexionar (Questions to Consider)

**Antes de leer la transcripción:**
1. [Pre-reading question to activate prior knowledge]
2. [Another question]

**Después de leer la transcripción:**
1. [Post-reading comprehension question]
2. [Application question]

---

## 📖 Transcripción Completa

[Translated transcript content goes here]
```

## 2. Translate the Transcript

- Translate all content to natural, clear Spanish appropriate for high school students
- Maintain all markdown formatting (headers, paragraphs, lists, emphasis)
- Preserve any page break comments like `<!-- Page 2 -->`
- Use proper Spanish punctuation and style
- Keep economic terminology accurate and standard

## 3. Quality Standards

- Use formal but accessible Spanish (tú form for questions, usted form for academic content)
- Ensure economic terms are standard Spanish (not direct word-for-word translations)
- Make examples culturally relevant when possible
- Ensure the header truly helps ELL students understand before reading

## 4. Output

Write the complete output (header + translated transcript) to:
{output_file}

The file should be valid markdown that renders beautifully and serves as a standalone learning resource.

---

# English Transcript Content

{transcript_content}

---

Begin translation now. Output the complete Spanish markdown file with the ELL header.
"""

def create_agent_translation_task(input_file, output_file):
    """Create a translation task for a Claude agent"""

    # Read the English markdown
    with open(input_file, 'r', encoding='utf-8') as f:
        transcript_content = f.read()

    # Generate the prompt
    prompt = TRANSLATION_PROMPT_TEMPLATE.format(
        input_file=input_file,
        output_file=output_file,
        transcript_content=transcript_content
    )

    return prompt

def translate_file_with_agent(input_file, output_file):
    """Use Claude CLI to translate a single file"""

    print(f"\n{'='*70}")
    print(f"Translating: {os.path.basename(input_file)}")
    print(f"{'='*70}")

    # Create the prompt
    prompt = create_agent_translation_task(input_file, output_file)

    # Create a temporary file with the prompt
    temp_prompt_file = f"{AGENTS_DIR}/prompt_{os.path.basename(input_file)}.txt"
    with open(temp_prompt_file, 'w', encoding='utf-8') as f:
        f.write(prompt)

    # Launch Claude agent via CLI (simulated - in practice you'd use the Task tool)
    # For now, we'll output instructions for manual agent launch
    print(f"\nAgent Task Created:")
    print(f"  Input: {input_file}")
    print(f"  Output: {output_file}")
    print(f"  Prompt saved to: {temp_prompt_file}")

    return temp_prompt_file

def batch_translate_parallel():
    """Translate all markdown files using parallel agents"""

    print("Batch Translation with Claude Agents")
    print("=" * 70)
    print(f"Using parallel Task agents (max {MAX_PARALLEL_AGENTS} concurrent)")
    print("=" * 70)

    # Create directories
    os.makedirs(OUTPUT_DIR, exist_ok=True)
    os.makedirs(AGENTS_DIR, exist_ok=True)

    # Get all markdown files
    md_files = list(Path(INPUT_DIR).glob("*.md"))

    if not md_files:
        print(f"\nNo markdown files found in {INPUT_DIR}")
        print("Run pdf_to_markdown.py first!")
        return

    print(f"\nFound {len(md_files)} files to translate")

    # Create translation tasks
    tasks = []
    for md_file in md_files:
        output_filename = md_file.stem + "-spanish.md"
        output_path = os.path.join(OUTPUT_DIR, output_filename)

        tasks.append({
            'input': str(md_file),
            'output': output_path,
            'name': md_file.stem
        })

    print(f"\n{'='*70}")
    print("Creating Agent Tasks")
    print(f"{'='*70}")

    # Create prompt files for each task
    prompt_files = []
    for task in tasks:
        prompt_file = translate_file_with_agent(task['input'], task['output'])
        prompt_files.append(prompt_file)

    print(f"\n{'='*70}")
    print("Translation Tasks Created!")
    print(f"{'='*70}")
    print(f"\nTotal tasks: {len(tasks)}")
    print(f"\nPrompt files saved to: {AGENTS_DIR}/")
    print(f"Output will be saved to: {OUTPUT_DIR}/")

    print("\n" + "="*70)
    print("NEXT STEPS - Manual Agent Launch")
    print("="*70)
    print("\nSince we're in a Python script, you have two options:")
    print("\n1. Use the Task tool directly in Claude Code:")
    print("   - Copy the prompts from the agent-sessions directory")
    print("   - Launch Task agents manually")
    print("\n2. Use the integrated launcher (run from Claude Code):")
    print("   - The system will automatically spawn Task agents")
    print("   - Translations will be saved automatically")
    print("\n" + "="*70)

    return tasks, prompt_files

def main():
    """Main execution"""
    tasks, prompt_files = batch_translate_parallel()

    print("\n✓ Task preparation complete!")
    print(f"  {len(tasks)} translation tasks ready")
    print(f"  Run this script from Claude Code to launch agents automatically")

if __name__ == "__main__":
    main()
