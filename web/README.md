# Economics USA - Web Viewer

Modern, clean React web application for browsing and viewing Economics USA Spanish educational resources.

## Features

- **Episode Navigation**: Collapsible sidebar with all 28 episodes
- **PDF Viewer**: Embedded PDF viewer for transcripts with page navigation
- **Audio Player**: Custom audio player for Spanish MP3 files
- **RSS Feeds**: Subscribe to Spanish audio feeds for podcast apps
  - Video Audio Feed: Spanish narration of video episodes
  - Audio Program Feed: Spanish narration of supplemental audio programs
- **Responsive Design**: Clean, modern interface built with TailwindCSS
- **Bilingual Labels**: Clear English and Spanish labels for content

## Quick Start

```bash
# Install dependencies
npm install

# Run development server
npm run dev
```

The app will be available at `http://localhost:5173`

## Build for Production

```bash
# Build optimized production bundle
npm run build

# Preview production build
npm run preview
```

### RSS Feed Configuration

The RSS feeds use the `VITE_PUBLIC_URL` environment variable for audio file URLs:

**For local development:**
- Defaults to `http://localhost:5173`

**For production deployment:**
1. Copy `.env.example` to `.env`
2. Set `VITE_PUBLIC_URL` to your production URL
3. Run `npm run build`

Example for Netlify:
```bash
VITE_PUBLIC_URL=https://econ-usa.netlify.app npm run build
```

Or set in your deployment platform's environment variables.

## Deploy to Netlify

### Build Settings

Configure these settings in your Netlify site:

- **Base directory:** `web`
- **Build command:** `npm run build`
- **Publish directory:** `web/dist`

### Environment Variables

In Netlify UI (Site settings > Environment variables), add:

```
VITE_PUBLIC_URL=https://your-site-name.netlify.app
```

Replace `your-site-name.netlify.app` with your actual Netlify domain.

### Configuration File

The included `netlify.toml` file contains these settings. You can also configure directly in the Netlify UI.

## Project Structure

```
web/
├── src/
│   ├── components/
│   │   ├── EpisodeList.jsx       # Sidebar with accordion navigation
│   │   ├── ContentViewer.jsx     # Main content display area
│   │   ├── PdfViewer.jsx         # PDF embedding with controls
│   │   └── AudioPlayer.jsx       # Custom audio player
│   ├── data/
│   │   └── episodes.json         # Auto-generated episode metadata
│   ├── App.jsx                   # Main application component
│   └── index.css                 # Tailwind styles
├── scripts/
│   └── generate-episodes-data.js # Generates episode metadata from folders
└── public/                       # Static assets
```

## How It Works

1. **Metadata Generation**: The `generate-episodes-data.js` script scans episode folders and creates a JSON file with all episode and file metadata
2. **RSS Feed Generation**: The `generate-rss-feeds.js` script creates two RSS feeds for Spanish audio files (video and audio programs)
3. **File Serving**: Vite is configured to serve files from the parent directory (where episode folders are located)
4. **Component Structure**:
   - `EpisodeList` shows all episodes with accordion behavior (one open at a time) and RSS feed links
   - Clicking a file passes it to `ContentViewer`
   - `ContentViewer` routes to either `PdfViewer` or `AudioPlayer` based on file type

## Technologies

- **React 19** - UI framework
- **Vite** - Build tool and dev server
- **TailwindCSS** - Utility-first CSS framework
- **react-pdf** - PDF.js wrapper for React
- **HTML5 Audio** - Native audio playback

## Development Notes

- Episode metadata and RSS feeds are regenerated on each `npm run dev` or `npm run build`
- PDF files are served from `../XX-Episode-Title/` folders
- Audio files use native HTML5 `<audio>` element for maximum compatibility
- RSS feeds are available at:
  - `/economics-usa-video-spanish.rss` - Video audio feed
  - `/economics-usa-audio-spanish.rss` - Audio program feed
