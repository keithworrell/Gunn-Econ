# Economics Transcript Translation & Audio Project

Automated pipeline to download, translate, and generate audio from economics video transcripts for Spanish-speaking students.

**Source:** [Economics U$A: 21st Century Edition - learner.org](https://learner.org/series/economics-ua-21st-century-edition)

## 📋 Table of Contents

- [Overview](#overview)
- [Features](#features)
- [Installation](#installation)
- [Usage](#usage)
- [Project Structure](#project-structure)
- [Technical Details](#technical-details)
- [Troubleshooting](#troubleshooting)
- [Customization](#customization)

## 🎯 Overview

This project provides a complete automated workflow to:

1. **Download** PDF transcripts from learner.org economics video series
2. **Translate** transcripts from English to Spanish while preserving formatting
3. **Generate** high-quality MP3 audio files from Spanish transcripts using Microsoft TTS

Perfect for educators who want to make educational content accessible to Spanish-speaking students.

## ✨ Features

- 🤖 **Automated Web Scraping**: Extracts all video links and downloads PDF transcripts
- 🌐 **Smart Translation**: Uses Google Translate API with rate limiting and error handling
- 📄 **Format Preservation**: Maintains original document structure (headers, paragraphs, spacing)
- 🎙️ **High-Quality TTS**: Microsoft Edge TTS with natural-sounding Spanish voices
- 📊 **Progress Tracking**: Visual progress bars and detailed logging
- 🔄 **Modular Pipeline**: Run individual steps or complete workflow
- 🛡️ **Error Handling**: Robust error handling with detailed error messages

## 📦 Installation

### Prerequisites

- Python 3.8 or higher
- Chrome/Chromium browser (for web scraping)
- Internet connection

### Setup

1. **Clone or download this repository**

2. **Install dependencies**

```bash
pip install -r requirements.txt
```

This will install:
- Selenium & WebDriver Manager (web scraping)
- Beautiful Soup (HTML parsing)
- pdfplumber (PDF text extraction)
- deep-translator (translation)
- reportlab (PDF generation)
- edge-tts (text-to-speech)
- tqdm (progress bars)

3. **Verify installation**

```bash
python run_pipeline.py --help
```

## 🚀 Usage

### Quick Start - Run Complete Pipeline

```bash
python run_pipeline.py --all
```

This will:
1. Download all transcripts
2. Translate them to Spanish
3. Generate audio files

### Run Individual Steps

**Download transcripts only:**
```bash
python run_pipeline.py --download
# or
python download_transcripts.py
```

**Translate existing transcripts:**
```bash
python run_pipeline.py --translate
# or
python translate_transcripts.py
```

**Generate audio from Spanish transcripts:**
```bash
python run_pipeline.py --audio
# or
python generate_audio.py
```

**Combine steps:**
```bash
python run_pipeline.py --translate --audio
```

### Command-Line Options

```bash
python run_pipeline.py [OPTIONS]

Options:
  --all           Run complete pipeline (download, translate, audio)
  --download      Download transcripts only
  --translate     Translate transcripts only
  --audio         Generate audio only
  --skip-check    Skip dependency verification
  -h, --help      Show help message
```

## 📁 Project Structure

```
economics-spanish/
├── original-transcripts/      # Downloaded PDF transcripts (English)
├── spanish-transcripts/       # Translated PDF transcripts (Spanish)
└── audio-files/              # Generated MP3 audio files

Scripts:
├── download_transcripts.py   # Web scraper and PDF downloader
├── translate_transcripts.py  # Translation and PDF generation
├── generate_audio.py         # Text-to-speech audio generation
├── run_pipeline.py          # Main orchestration script
└── requirements.txt         # Python dependencies
```

## 🔧 Technical Details

### Download Process

- Uses Selenium with headless Chrome for JavaScript-rendered pages
- Automatically handles dynamic content loading
- Saves page source for debugging if errors occur
- Implements polite scraping with delays between requests

### Translation Process

- Extracts text from PDFs while preserving structure
- Identifies headers vs. paragraphs for proper formatting
- Handles long text by splitting into chunks
- Rate-limited API calls to prevent blocking
- Maintains original document layout in new PDFs

### Audio Generation

- Uses Microsoft Edge TTS (free, no API key required)
- Multiple Spanish voice options:
  - `es-MX-DaliaNeural` (Mexican Spanish, Female) - Default
  - `es-MX-JorgeNeural` (Mexican Spanish, Male)
  - `es-ES-ElviraNeural` (Spain Spanish, Female)
  - `es-ES-AlvaroNeural` (Spain Spanish, Male)
- Cleans text for optimal TTS output
- Estimates audio duration before generation

## 🐛 Troubleshooting

### Web Scraping Issues

**Problem:** 403 Forbidden or no videos found

**Solutions:**
1. Check if learner.org website structure has changed
2. Inspect the HTML manually and update selectors in `download_transcripts.py`
3. Check `page_source_debug.html` for actual page content
4. Ensure Chrome/Chromium is properly installed

### Translation Issues

**Problem:** Translation fails or text appears garbled

**Solutions:**
1. Check internet connection
2. Verify PDF text extraction: some PDFs may be scanned images
3. Try reducing batch size for very long texts
4. Check if Google Translate API is accessible from your region

### Audio Generation Issues

**Problem:** No audio files created

**Solutions:**
1. Verify Spanish transcripts exist in `spanish-transcripts/` folder
2. Check if edge-tts is properly installed: `pip install --upgrade edge-tts`
3. Ensure adequate disk space for audio files
4. Check internet connection (edge-tts requires online access)

### General Issues

**Problem:** Module not found errors

**Solution:**
```bash
pip install -r requirements.txt --upgrade
```

**Problem:** Permission denied

**Solution:**
```bash
chmod +x *.py
```

## 🎨 Customization

### Change TTS Voice

Edit `generate_audio.py` and modify the `DEFAULT_VOICE` variable:

```python
DEFAULT_VOICE = SPANISH_VOICES['male']  # For male voice
```

To see all available voices, uncomment this line in `generate_audio.py`:
```python
asyncio.run(list_available_voices())
```

### Adjust Translation Style

Modify the translator initialization in `translate_transcripts.py`:

```python
# For more formal translation
self.translator = GoogleTranslator(source='en', target='es', proxies=None)
```

### Customize PDF Layout

Edit the styles in `translate_transcripts.py`:

```python
body_style = ParagraphStyle(
    'CustomBody',
    fontSize=11,  # Increase font size
    alignment=TA_JUSTIFY,
)
```

### Change Output Directories

Modify the constants at the top of each script:

```python
OUTPUT_DIR = "my-custom-folder/transcripts"
```

## 📝 File Naming Convention

- Original transcripts: `video-01-title.pdf`
- Spanish transcripts: `video-01-title-spanish.pdf`
- Audio files: `video-01-title-spanish.mp3`

Files are numbered sequentially to maintain order and allow easy matching between versions.

## ⚖️ Legal & Ethical Considerations

- Ensure you have permission to download and translate copyrighted content
- This tool is intended for educational purposes
- Respect learner.org's terms of service and robots.txt
- Use reasonable rate limiting when scraping
- Consider purchasing or licensing content for commercial use

## 🤝 Contributing

Suggestions and improvements welcome! Common enhancements:

- Add support for other languages
- Implement OCR for image-based PDFs
- Add batch processing with parallel downloads
- Integrate with learning management systems
- Add subtitle/caption generation

## 📧 Support

For issues specific to this codebase, check the troubleshooting section above.

For learner.org content access issues, contact learner.org directly.

## 🙏 Acknowledgments

- **learner.org** for providing educational content
- **Microsoft Edge TTS** for free, high-quality text-to-speech
- **Google Translate** for translation services
- Open-source Python community for excellent libraries

---

**Happy Teaching! 🎓**
