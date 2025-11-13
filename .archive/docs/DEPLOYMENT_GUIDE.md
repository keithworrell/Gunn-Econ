# Deployment Guide - Running on Your Local Machine

The automated pipeline scripts in this repository need to be run on your local machine due to environment requirements for web scraping and external API access.

## Why Local Execution is Needed

1. **Web Scraping**: Playwright/Selenium require a full browser environment
2. **Translation API**: Google Translate requires internet access
3. **TTS API**: Microsoft Edge TTS requires internet connectivity
4. **Large Files**: Generated audio and PDF files are easier to manage locally

## Setup on Your Local Machine

### Prerequisites

- Python 3.8 or higher
- Internet connection
- 1-2 GB free disk space (for all transcripts and audio)

### Step 1: Clone the Repository

```bash
git clone <your-repo-url>
cd Gunn-Econ
```

### Step 2: Install Dependencies

```bash
pip install -r requirements.txt
```

### Step 3: Install Playwright Browser

```bash
python -m playwright install chromium
```

### Step 4: Verify Setup

```bash
python verify_setup.py
```

This will check that all dependencies are installed correctly.

## Running the Pipeline

### Option 1: Complete Automated Pipeline (Recommended)

If the website allows automated downloads:

```bash
python run_pipeline.py --all
```

This will:
1. Download all transcripts (~5-10 minutes)
2. Translate to Spanish (~15-30 minutes)
3. Generate audio files (~10-20 minutes)

**Total time: 30-60 minutes** (runs unattended)

### Option 2: Using Playwright for Download

If the basic download script fails, use the Playwright version:

```bash
python download_with_playwright.py
```

Playwright is more robust against anti-bot protections.

### Option 3: Manual Download + Automated Processing

If automated downloads are blocked:

1. **Manually download PDFs**: See [MANUAL_DOWNLOAD_GUIDE.md](MANUAL_DOWNLOAD_GUIDE.md)
2. **Place in folder**: `economics-spanish/original-transcripts/`
3. **Run processing**:
   ```bash
   python run_pipeline.py --translate --audio
   ```

## Expected Results

After completion, you'll have:

```
economics-spanish/
├── original-transcripts/       # ~26 English PDF files (~50-100 MB)
│   ├── video-01-*.pdf
│   ├── video-02-*.pdf
│   └── ...
├── spanish-transcripts/        # ~26 Spanish PDF files (~50-100 MB)
│   ├── video-01-*-spanish.pdf
│   ├── video-02-*-spanish.pdf
│   └── ...
└── audio-files/                # ~26 MP3 files (~200-500 MB)
    ├── video-01-*-spanish.mp3
    ├── video-02-*-spanish.mp3
    └── ...
```

## Committing Results Back to Repository

After running the pipeline successfully:

```bash
# Add generated files
git add economics-spanish/

# Commit
git commit -m "Add translated transcripts and audio files"

# Push
git push origin <your-branch>
```

## Troubleshooting Local Execution

### Download Issues

**Problem**: 403 Forbidden or no videos found
```bash
# Try Playwright version
python download_with_playwright.py

# Or download manually (see MANUAL_DOWNLOAD_GUIDE.md)
```

**Problem**: Chrome not found
```bash
# Install Playwright browsers
python -m playwright install chromium

# Or install Chrome/Chromium via your package manager
```

### Translation Issues

**Problem**: "Connection refused" or translation errors
```bash
# Check internet connection
ping google.com

# Try running again (Google may rate-limit temporarily)
python translate_transcripts.py
```

**Problem**: Some text not translated
- This is normal for image-based PDFs
- The script preserves original text when translation fails

### Audio Generation Issues

**Problem**: "Cannot connect to host"
```bash
# Check internet connection
ping api.msedgeservices.com

# edge-tts requires online access
```

**Problem**: Audio quality issues
```bash
# Try a different voice in generate_audio.py
# Change DEFAULT_VOICE to one of:
#   - es-MX-JorgeNeural (Mexican Spanish, Male)
#   - es-ES-ElviraNeural (Spain Spanish, Female)
#   - es-ES-AlvaroNeural (Spain Spanish, Male)
```

## Performance Tips

### Speed Up Translation

- Translation is the slowest step due to API rate limiting
- Run overnight if processing many files
- The script auto-saves progress - safe to ctrl+C and resume

### Speed Up Downloads

- Use Playwright version for better reliability
- Downloads are sequential to avoid overloading the server
- Expect ~15-30 seconds per video

### Disk Space

- Full pipeline generates ~600-800 MB of files
- Original PDFs: ~50-100 MB
- Spanish PDFs: ~50-100 MB
- Audio files: ~400-600 MB
- Ensure adequate free space before starting

## Development and Testing

### Test with One Transcript First

```bash
# Create sample
python create_sample_transcript.py

# Translate only
python translate_transcripts.py

# Audio only
python generate_audio.py
```

This verifies everything works before processing all 26 videos.

### Running Individual Steps

```bash
# Just download
python download_transcripts.py

# Or use Playwright
python download_with_playwright.py

# Just translate
python translate_transcripts.py

# Just audio
python generate_audio.py

# Or use the pipeline script
python run_pipeline.py --download
python run_pipeline.py --translate
python run_pipeline.py --audio
```

## Cloud/Server Deployment

If you want to run this on a cloud server (AWS, GCP, Azure):

1. **Use a VM with GUI support** (for browser automation)
2. **Or use headless mode** (already configured in scripts)
3. **Ensure adequate bandwidth** (downloading PDFs and API calls)
4. **Consider costs** (translation and TTS are free but bandwidth isn't)

Example Dockerfile (if needed):
```dockerfile
FROM python:3.11
RUN apt-get update && apt-get install -y chromium chromium-driver
WORKDIR /app
COPY requirements.txt .
RUN pip install -r requirements.txt
RUN python -m playwright install chromium --with-deps
COPY . .
CMD ["python", "run_pipeline.py", "--all"]
```

## Next Steps

After successfully running the pipeline:

1. **Share with students**: Distribute the Spanish PDFs and audio files
2. **Upload to LMS**: Add to Canvas, Moodle, Google Classroom, etc.
3. **Create playlists**: Organize audio files for sequential playback
4. **Verify quality**: Spot-check translations and audio for accuracy

## Support

For issues:
- Check [QUICKSTART.md](QUICKSTART.md) for common questions
- See [README.md](README.md) for detailed documentation
- Review [MANUAL_DOWNLOAD_GUIDE.md](MANUAL_DOWNLOAD_GUIDE.md) if downloads fail

The scripts are designed to be resilient - they'll skip problematic files and continue processing.
