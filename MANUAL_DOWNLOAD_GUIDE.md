# Manual Download Guide

Unfortunately, learner.org blocks automated downloads with 403 Forbidden responses. You'll need to manually download the transcripts first.

## Step 1: Manual Download Instructions

### Option A: Download Individual Transcripts

1. **Visit the series page:**
   https://learner.org/series/economics-ua-21st-century-edition

2. **For each video:**
   - Click on the video link in the sidebar
   - Look for a "Transcript" or "PDF" download link
   - Download the PDF transcript
   - Save to `economics-spanish/original-transcripts/` folder
   - Name files as: `video-01-title.pdf`, `video-02-title.pdf`, etc.

### Option B: Bulk Download with Browser Extension

1. Install a bulk download extension like:
   - **DownThemAll** (Firefox)
   - **Download Master** (Chrome)

2. Navigate to the series page

3. Use the extension to filter and download all PDF files

4. Move PDFs to `economics-spanish/original-transcripts/` folder

5. Rename files sequentially: `video-01.pdf`, `video-02.pdf`, etc.

### Option C: Browser Developer Tools Method

1. Open browser Developer Tools (F12)
2. Go to Network tab
3. Navigate through each video page
4. Filter by "PDF" or "Document" type
5. Right-click on transcript PDF and "Open in new tab"
6. Save each PDF manually

## Step 2: Verify Downloads

After downloading, verify your files:

```bash
ls -la economics-spanish/original-transcripts/
```

You should see files like:
```
video-01-what-sets-prices.pdf
video-02-command-economies.pdf
video-03-mixed-economies.pdf
...
```

## Step 3: Run Translation and Audio Generation

Once you have the PDFs downloaded:

```bash
# Translate all transcripts to Spanish
python translate_transcripts.py

# Generate audio files
python generate_audio.py
```

Or run both at once:

```bash
python run_pipeline.py --translate --audio
```

## Video List

Here are the Economics U$A videos (you'll need to download each manually):

1. What Sets Prices?
2. Command Economies
3. Mixed Economies
4. The Role of Government
5. Measuring the Macroeconomy
6. Monetary Policy
7. Fiscal Policy
8. Unemployment
9. Inflation
10. The Business Cycle
11. Economic Growth
12. International Trade
13. Foreign Exchange
14. Less Developed Countries
15. Transitional Economies
16. The Study of Economics
17. Market Structure
18. Productive Resources
19. Entrepreneurship
20. The Stock Market
21. Personal Finance
22. Banking
23. Money and Banking History
24. Market Failures
25. Public Choice
26. Income Distribution

## Alternative: Use a Sample Transcript

If you want to test the pipeline first with one transcript:

1. Download just ONE transcript manually
2. Place it in `economics-spanish/original-transcripts/`
3. Run the pipeline:
   ```bash
   python run_pipeline.py --translate --audio
   ```

This will let you verify the translation and audio generation work before downloading all 26 transcripts.

## Troubleshooting

**Q: I can't find the transcript PDF on the video page**
A: Some videos may not have transcripts available. Skip those and continue with the next video.

**Q: The PDFs are scanned images, not text**
A: The translation script uses pdfplumber which can extract text from most PDFs. If a PDF is a pure image, you may need OCR tools.

**Q: Can I use a different naming convention?**
A: Yes! The scripts work with any PDF files in the folder. The sequential naming just helps keep things organized.

## Need Help?

If you successfully download the transcripts manually, the rest of the pipeline (translation and audio generation) works automatically and has been tested to work correctly!
