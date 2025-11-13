# Economics USA - Spanish Educational Resources

Comprehensive Spanish translations and audio materials for the Economics U$A 21st Century Edition video series, designed for Spanish-speaking high school students.

## 🌐 Web Viewer

**Interactive web application for browsing all materials:**

```bash
cd web
npm install
npm run dev
```

Visit `http://localhost:5173` to use the web viewer with:
- Collapsible episode navigation sidebar
- Embedded PDF viewer for transcripts
- Custom audio player for Spanish MP3s
- Clean, responsive design

See [web/README.md](web/README.md) for more details.

## 📁 Project Structure

### Episode Folders

Each episode has its own folder containing 6 files (or 3 for episodes with partial content):

```
XX-Episode-Title/
├── XX-episode-title-video.pdf                    # English video transcript
├── XX-episode-title-audio.pdf                    # English audio transcript
├── XX-episode-title-video-spanish.pdf            # Spanish video transcript
├── XX-episode-title-audio-spanish.pdf            # Spanish audio transcript
├── XX-episode-title-video-spanish-spanish.mp3    # Spanish video audio
└── XX-episode-title-audio-spanish-spanish.mp3    # Spanish audio audio
```

**Example:** [01-Markets/](01-Markets/)
- `01-markets-video.pdf` - English video transcript
- `01-markets-audio.pdf` - English audio transcript
- `01-markets-video-spanish.pdf` - Spanish video transcript
- `01-markets-audio-spanish.pdf` - Spanish audio transcript
- `01-markets-video-spanish-spanish.mp3` - Spanish video audio
- `01-markets-audio-spanish-spanish.mp3` - Spanish audio audio

### Web Application

- **[web/](web/)** - React web viewer for browsing all materials
  - Modern, responsive interface with episode navigation
  - Embedded PDF viewer and audio player
  - See [web/README.md](web/README.md) for setup instructions

### Archive

- **[.archive/](.archive/)** - Development scripts, documentation, and intermediate files
  - `scripts/` - Python scripts for downloading, translation, and audio generation
  - `docs/` - Technical documentation and guides
  - `intermediate-files/` - Markdown conversions and processing artifacts

## 📊 Coverage

**28 Complete Episodes** (both video and audio transcripts):
- Markets
- The Firm
- Supply and Demand
- Perfect Competition and Inelastic Demand
- Monopoly
- Oligopolies
- Pollution & the Environment
- Labor and Management
- Profits and Interest
- Reducing Poverty
- Economic Growth
- Public Goods and Responsibilities
- Resources and Scarcity
- GDP/GNP
- Boom and Bust
- The Great Depression and the Keynesian Revolution
- Fiscal Policy
- Inflation
- The Banking System
- The Federal Reserve
- Stagflation
- Productivity
- Federal Deficits
- Monetary Policy
- Stabilization Policy
- International Trade
- Exchange Rates

**Plus:** Economic Efficiency (video transcript only)

**Total:** 55 out of 56 possible transcripts (98.2% complete)

## 🎯 Purpose

This project provides accessible Spanish-language educational materials for Economics USA, supporting:
- Spanish-speaking students learning economics
- Bilingual education programs
- English Language Learner (ELL) support
- Accessibility through both written and audio formats

## 📝 Organization

**28 Episode Folders** organized as `XX-Episode-Title/`

Each folder contains all related materials:
- Original English transcripts (video + audio PDFs)
- Spanish translations (video + audio PDFs)
- Spanish audio files (video + audio MP3s)

**File naming pattern:** `{episode-number}-{topic-slug}-{type}.{ext}`

27 complete episodes have 6 files each. Episode 05 (Economic Efficiency) has only 3 files (video transcript only).

## 🔗 Original Source

Content based on **Economics U$A: 21st Century Edition** from Annenberg Learner:
- Original series: https://www.learner.org/series/economics-ua-21st-century-edition/
- Note: Learner.org will sunset on July 1, 2026

## 📄 License

Educational materials derived from Annenberg Learner's Economics U$A series.
Translations and audio generated for educational purposes.

---

**Generated:** November 2025
**For:** Gunn High School Economics Program
