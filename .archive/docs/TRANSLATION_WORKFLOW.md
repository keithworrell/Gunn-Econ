# Translation Workflow with Claude Agents

High-quality translation pipeline using Claude agents for ELL-optimized Spanish transcripts.

## Why This Approach?

✅ **Higher Quality**: Claude understands economics concepts and context
✅ **ELL-Optimized**: Generates comprehensive learning headers for English Language Learners
✅ **Parallel Processing**: Multiple agents translate simultaneously (much faster)
✅ **No API Limits**: No rate limiting issues
✅ **Markdown Native**: Clean format preservation
✅ **Teacher-Friendly**: Structured output perfect for non-Spanish-speaking teachers

## Complete Workflow

### Step 1: PDF → Markdown (Extract)

Convert downloaded PDFs to clean markdown format:

```bash
python pdf_to_markdown.py
```

**Output**: `economics-spanish/markdown-english/*.md`

This extracts text while preserving:
- Headings and subheadings
- Paragraph structure
- Page breaks
- Formatting

### Step 2: Generate Translation Tasks

Create task specifications for Claude agents:

```bash
python translate_orchestrator.py
```

**Output**: `economics-spanish/translation-tasks.json`

This creates a JSON file with:
- Input/output file paths
- Complete translation prompts
- ELL header specifications

### Step 3: Translate with Claude Agents (The Magic! ✨)

**Option A: Ask Claude Code to Run Batch**

Simply say to Claude Code:

> "Read translation-tasks.json and launch Task agents in parallel to translate all transcripts. Process 5 at a time."

Claude will:
- Launch multiple Task agents simultaneously
- Each agent translates one complete transcript
- Generates ELL-optimized headers automatically
- Saves Spanish markdown files

**Option B: Launch Individual Agents**

For more control:

> "Launch a Task agent to translate video-01-supply-and-demand. Use the prompt from translation-tasks.json."

**Option C: Manual (if needed)**

1. Open `translation-tasks.json`
2. Copy a prompt
3. Paste to Claude Code
4. Claude reads input, translates, writes output

### Step 4: Markdown → PDF (Format)

Convert Spanish markdown to beautifully formatted PDFs:

```bash
python markdown_to_pdf.py
```

**Output**: `economics-spanish/spanish-transcripts/*.pdf`

Creates professional PDFs with:
- Proper Spanish formatting
- Visual hierarchy
- Icons and tables
- Page breaks

## ELL-Optimized Header Structure

Each translated transcript includes a comprehensive learning header:

### 📚 Resumen del Episodio
2-3 sentence overview of the episode topic and importance

### 🎯 Objetivos de Aprendizaje
3 learning objectives starting with "Al final de este episodio, podrás..."

### 🔑 Vocabulario Clave

**Términos Económicos Principales**
Table with 5-8 key terms:
- Término Español
- English Term
- Definición (in Spanish)
- Ejemplo en Contexto

**Cognados Útiles**
Spanish-English cognates to help students recognize familiar words

### 💡 Conceptos Fundamentales
2-3 main concepts, each with:
- ¿Qué es? (What is it?)
- ¿Por qué importa? (Why does it matter?)
- Ejemplo cotidiano (Everyday example)

### 🌎 Conexión con Tu Vida
1-2 relatable real-world scenarios students can connect to

### ❓ Preguntas para Reflexionar
- 2 pre-reading questions (activate prior knowledge)
- 2 post-reading questions (check comprehension)

### 📖 Transcripción Completa
Full translated transcript with formatting preserved

## Design Principles for ELL Students

1. **Visual Hierarchy**: Icons and clear sections aid scanning
2. **Bilingual Scaffolding**: Key terms show English in parentheses
3. **Cognate Recognition**: Leverages Spanish-English similarities
4. **Context First**: Summary before details
5. **Real-World Connections**: Abstract → Concrete
6. **Metacognitive Questions**: Activate and assess understanding
7. **Consistent Structure**: Same format every episode
8. **Culturally Relevant**: Examples students can relate to

## For Non-Spanish-Speaking Teachers

Even without Spanish fluency, teachers can:
- **Follow the structure**: Same sections every document
- **Recognize cognates**: Many economic terms are similar
- **Track progress**: Numbered objectives and questions
- **Assess understanding**: Clear pre/post questions
- **Navigate easily**: Visual icons and headings

## Performance

**With downloaded PDFs (26 transcripts):**
- PDF → Markdown: ~30 seconds
- Generate tasks: ~5 seconds
- Translation (5 parallel agents): ~10-15 minutes
- Markdown → PDF: ~30 seconds

**Total time: ~15-20 minutes** for all 26 transcripts!

Compare to sequential Google Translate: ~30-45 minutes (and lower quality)

## File Organization

```
economics-spanish/
├── original-transcripts/       # Downloaded PDFs (English)
├── markdown-english/           # Converted to markdown
├── markdown-spanish/           # Translated with ELL headers
├── spanish-transcripts/        # Final formatted PDFs
├── translation-tasks.json      # Agent task specifications
└── agent-sessions/             # Agent prompt files (for reference)
```

## Quality Assurance

Claude agents provide:
- Accurate economic terminology (not word-for-word translation)
- Age-appropriate language (high school level)
- Culturally relevant examples
- Proper Spanish grammar and style
- Consistent formatting across all documents

## Example Translation

See: `economics-spanish/markdown-spanish/video-01-supply-and-demand-spanish.md`

This demonstrates:
- Complete ELL header with all sections
- Natural, clear Spanish translation
- Maintained markdown formatting
- Relatable examples for students
- Proper economic terminology

## Troubleshooting

**"No markdown files found"**
- Run `python pdf_to_markdown.py` first

**"Task agent not launching"**
- Ensure you're asking Claude Code (not running Python directly)
- Claude Code has access to the Task tool
- Python scripts create the tasks, Claude Code executes them

**"Translation quality concerns"**
- Review `translation-tasks.json` prompts
- Adjust the template in `translate_orchestrator.py`
- Regenerate tasks and re-translate

**"PDF formatting issues"**
- Check the markdown file directly
- Adjust styles in `markdown_to_pdf.py`
- Regenerate PDFs

## Next Steps

After translation:
1. **Review**: Spot-check a few translations for quality
2. **Generate Audio**: Run `python generate_audio.py` on Spanish transcripts
3. **Distribute**: Share PDFs and audio with students
4. **Upload to LMS**: Add to Canvas, Google Classroom, etc.

## Tips

- **Test first**: Translate 1-2 files to verify quality before batch processing
- **Save prompts**: Keep `translation-tasks.json` for reference and re-runs
- **Customize**: Edit the header template in `translate_orchestrator.py` for your needs
- **Parallel power**: More agents = faster completion (use 5-10 at once)
- **Keep markdown**: Easier to edit than PDFs if you need to make changes

## Script Reference

| Script | Purpose | Input | Output |
|--------|---------|-------|--------|
| `pdf_to_markdown.py` | Extract PDFs | `original-transcripts/*.pdf` | `markdown-english/*.md` |
| `translate_orchestrator.py` | Generate tasks | `markdown-english/*.md` | `translation-tasks.json` |
| *(Ask Claude Code)* | Translate | `translation-tasks.json` | `markdown-spanish/*.md` |
| `markdown_to_pdf.py` | Format PDFs | `markdown-spanish/*.md` | `spanish-transcripts/*.pdf` |

---

**Happy Teaching! 🎓**

High-quality, ELL-optimized translations ready in minutes!
