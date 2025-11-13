# Deployment Guide

## Netlify Deployment Checklist

### 1. Build Settings

In your Netlify site configuration, set:

- **Base directory:** `web`
- **Build command:** `npm run build`
- **Publish directory:** `web/dist`

### 2. Environment Variables

In Netlify UI (Site settings > Build & deploy > Environment variables), add:

| Key | Value |
|-----|-------|
| `VITE_PUBLIC_URL` | `https://your-site-name.netlify.app` |

**Important:** Replace `your-site-name.netlify.app` with your actual Netlify domain.

### 3. Deploy

Once configured, Netlify will:
1. Run `npm install` in the `web` directory
2. Generate episode metadata and RSS feeds with your production URL
3. Build the React application
4. Deploy to your site

### 4. Verify Deployment

After deployment, check:

- [ ] Website loads at your Netlify URL
- [ ] Episodes display in the sidebar
- [ ] PDF viewer works when clicking transcripts
- [ ] Audio player works when clicking MP3 files
- [ ] RSS feed links are accessible:
  - `https://your-site.netlify.app/economics-usa-video-spanish.rss`
  - `https://your-site.netlify.app/economics-usa-audio-spanish.rss`
- [ ] RSS feeds contain correct production URLs (not localhost)

### 5. Testing RSS Feeds

Test your RSS feeds in a podcast app:

1. Copy the RSS feed URL
2. Add to your podcast app (Apple Podcasts, Overcast, Pocket Casts, etc.)
3. Verify episodes load and audio plays correctly

## Manual Build (Local Testing)

To test the production build locally:

```bash
# Set production URL and build
VITE_PUBLIC_URL=https://your-site.netlify.app npm run build

# Preview the production build
npm run preview
```

Then open the RSS feeds to verify they contain your production URLs.

## Troubleshooting

### RSS feeds still show localhost URLs

Make sure:
1. `VITE_PUBLIC_URL` environment variable is set in Netlify
2. You've triggered a new build after setting the variable
3. Check the build logs to confirm the URL was used

### Audio files not loading

Ensure:
1. All episode folders are in the repository root (alongside `web/`)
2. File permissions allow public access
3. Audio file paths match the naming convention

### PDF viewer not working

Check:
1. Browser console for errors
2. PDF.js worker is loading from CDN
3. PDF files are accessible via direct URLs
