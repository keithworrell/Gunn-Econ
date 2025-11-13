# Quick Start Guide

Get up and running in 5 minutes!

## Step 1: Install Dependencies

```bash
pip install -r requirements.txt
```

This will install all required packages (may take 2-3 minutes).

## Step 2: Verify Setup

```bash
python verify_setup.py
```

This checks that everything is installed correctly.

## Step 3: Run the Pipeline

### Option A: Run Everything at Once

```bash
python run_pipeline.py --all
```

This will:
- Download all transcripts from learner.org (~5-10 minutes)
- Translate them to Spanish (~10-20 minutes depending on count)
- Generate audio files (~5-15 minutes)

**Total time: ~20-45 minutes** (mostly automated)

### Option B: Run Step by Step

**Step 1: Download Transcripts**
```bash
python download_transcripts.py
```

**Step 2: Translate to Spanish**
```bash
python translate_transcripts.py
```

**Step 3: Generate Audio (Optional)**
```bash
python generate_audio.py
```

## Expected Output

After completion, you'll find:

```
economics-spanish/
├── original-transcripts/    # English PDFs
│   ├── video-01-*.pdf
│   ├── video-02-*.pdf
│   └── ...
├── spanish-transcripts/     # Spanish PDFs
│   ├── video-01-*-spanish.pdf
│   ├── video-02-*-spanish.pdf
│   └── ...
└── audio-files/             # Spanish MP3s
    ├── video-01-*-spanish.mp3
    ├── video-02-*-spanish.mp3
    └── ...
```

## Troubleshooting

### "Module not found" error
```bash
pip install -r requirements.txt --upgrade
```

### "No videos found" message
The website structure may have changed. Check `page_source_debug.html` and update selectors in `download_transcripts.py`.

### Translation taking too long
This is normal! Each transcript may have thousands of words. Grab a coffee ☕

### Audio generation fails
Make sure you have internet connection - edge-tts requires online access.

## Tips

- **Run overnight**: The full pipeline can take 30-60 minutes for many videos
- **Test with one video first**: Manually download one PDF and test translation/audio
- **Customize voice**: Edit `generate_audio.py` to change the Spanish voice
- **Resume failed steps**: Scripts are idempotent - rerun if something fails

## What's Happening Under the Hood?

1. **Download**: Selenium opens learner.org, finds all videos, downloads PDFs
2. **Translate**: Extracts text from PDFs, translates via Google Translate, creates new PDFs
3. **Audio**: Reads Spanish PDFs, sends to Microsoft TTS, saves MP3 files

## Need Help?

Check the full README.md for detailed troubleshooting and customization options.

---

**Ready to start? Run:** `python run_pipeline.py --all`
