import fs from 'fs';
import path from 'path';
import { fileURLToPath } from 'url';

const __filename = fileURLToPath(import.meta.url);
const __dirname = path.dirname(__filename);

const rootDir = path.resolve(__dirname, '../..');
const publicDir = path.resolve(__dirname, '../public');

// Episode metadata mapping
const episodeMetadata = [
  { num: 1, title: 'Markets', folder: '01-Markets' },
  { num: 2, title: 'The Firm', folder: '02-The-Firm' },
  { num: 3, title: 'Supply and Demand', folder: '03-Supply-and-Demand' },
  { num: 4, title: 'Perfect Competition and Inelastic Demand', folder: '04-Perfect-Competition-and-Inelastic-Demand' },
  { num: 5, title: 'Economic Efficiency', folder: '05-Economic-Efficiency' },
  { num: 6, title: 'Monopoly', folder: '06-Monopoly' },
  { num: 7, title: 'Oligopolies', folder: '07-Oligopolies' },
  { num: 8, title: 'Pollution & the Environment', folder: '08-Pollution-and-Environment' },
  { num: 9, title: 'Labor and Management', folder: '09-Labor-and-Management' },
  { num: 10, title: 'Profits and Interest', folder: '10-Profits-and-Interest' },
  { num: 11, title: 'Reducing Poverty', folder: '11-Reducing-Poverty' },
  { num: 12, title: 'Economic Growth', folder: '12-Economic-Growth' },
  { num: 13, title: 'Public Goods and Responsibilities', folder: '13-Public-Goods-and-Responsibilities' },
  { num: 14, title: 'Resources and Scarcity', folder: '14-Resources-and-Scarcity' },
  { num: 15, title: 'GDP/GNP', folder: '15-GDP-GNP' },
  { num: 16, title: 'Boom and Bust', folder: '16-Boom-and-Bust' },
  { num: 17, title: 'The Great Depression and the Keynesian Revolution', folder: '17-The-Great-Depression-and-the-Keynesian-Revolution' },
  { num: 18, title: 'Fiscal Policy', folder: '18-Fiscal-Policy' },
  { num: 19, title: 'Inflation', folder: '19-Inflation' },
  { num: 20, title: 'The Banking System', folder: '20-The-Banking-System' },
  { num: 21, title: 'The Federal Reserve', folder: '21-The-Federal-Reserve' },
  { num: 22, title: 'Stagflation', folder: '22-Stagflation' },
  { num: 23, title: 'Productivity', folder: '23-Productivity' },
  { num: 24, title: 'Federal Deficits', folder: '24-Federal-Deficits' },
  { num: 25, title: 'Monetary Policy', folder: '25-Monetary-Policy' },
  { num: 26, title: 'Stabilization Policy', folder: '26-Stabilization-Policy' },
  { num: 27, title: 'International Trade', folder: '27-International-Trade' },
  { num: 28, title: 'Exchange Rates', folder: '28-Exchange-Rates' },
];

function escapeXml(text) {
  return text
    .replace(/&/g, '&amp;')
    .replace(/</g, '&lt;')
    .replace(/>/g, '&gt;')
    .replace(/"/g, '&quot;')
    .replace(/'/g, '&apos;');
}

function getFileSize(filePath) {
  try {
    const stats = fs.statSync(filePath);
    return stats.size;
  } catch (e) {
    return 0;
  }
}

function getFileModifiedDate(filePath) {
  try {
    const stats = fs.statSync(filePath);
    return stats.mtime;
  } catch (e) {
    return new Date();
  }
}

function generateRssFeed(type, baseUrl) {
  const isVideo = type === 'video';
  const feedTitle = isVideo
    ? 'Economics USA - Spanish Video Audio'
    : 'Economics USA - Spanish Audio Program';
  const feedDescription = isVideo
    ? 'Spanish audio narration for Economics USA video episodes'
    : 'Spanish audio for Economics USA supplemental audio programs';

  let items = [];

  for (const episode of episodeMetadata) {
    const episodePath = path.join(rootDir, episode.folder);
    const episodeNum = String(episode.num).padStart(2, '0');

    // Construct filename based on type
    const audioFileName = isVideo
      ? `${episodeNum}-${episode.folder.substring(3).toLowerCase()}-video-spanish-spanish.mp3`
      : `${episodeNum}-${episode.folder.substring(3).toLowerCase()}-audio-spanish-spanish.mp3`;

    const audioFilePath = path.join(episodePath, audioFileName);

    // Check if file exists
    if (!fs.existsSync(audioFilePath)) {
      continue;
    }

    const fileSize = getFileSize(audioFilePath);
    const pubDate = getFileModifiedDate(audioFilePath);
    const enclosureUrl = `${baseUrl}/episodes/${episode.folder}/${audioFileName}`;

    items.push({
      title: `Episode ${episode.num}: ${episode.title}`,
      description: `${feedDescription} - Episode ${episode.num}: ${episode.title}`,
      pubDate: pubDate.toUTCString(),
      enclosureUrl: enclosureUrl,
      enclosureLength: fileSize,
      guid: enclosureUrl,
      episodeNum: episode.num
    });
  }

  // Generate RSS XML
  const rss = `<?xml version="1.0" encoding="UTF-8"?>
<rss version="2.0" xmlns:itunes="http://www.itunes.com/dtds/podcast-1.0.dtd">
  <channel>
    <title>${escapeXml(feedTitle)}</title>
    <description>${escapeXml(feedDescription)}</description>
    <link>${baseUrl}</link>
    <language>es</language>
    <lastBuildDate>${new Date().toUTCString()}</lastBuildDate>
    <itunes:author>Economics USA Spanish Translation Project</itunes:author>
    <itunes:summary>${escapeXml(feedDescription)}</itunes:summary>
    <itunes:category text="Education"/>
${items.map(item => `    <item>
      <title>${escapeXml(item.title)}</title>
      <description>${escapeXml(item.description)}</description>
      <pubDate>${item.pubDate}</pubDate>
      <enclosure url="${escapeXml(item.enclosureUrl)}" length="${item.enclosureLength}" type="audio/mpeg"/>
      <guid isPermaLink="true">${escapeXml(item.guid)}</guid>
      <itunes:duration>0</itunes:duration>
      <itunes:episode>${item.episodeNum}</itunes:episode>
    </item>`).join('\n')}
  </channel>
</rss>`;

  return rss;
}

function main() {
  console.log('Generating RSS feeds for Economics USA Spanish audio...');

  // Get base URL from environment variable or use localhost default
  const baseUrl = process.env.VITE_PUBLIC_URL || 'http://localhost:5173';
  console.log(`Using base URL: ${baseUrl}`);

  // Ensure public directory exists
  if (!fs.existsSync(publicDir)) {
    fs.mkdirSync(publicDir, { recursive: true });
  }

  // Generate video audio RSS feed
  const videoRss = generateRssFeed('video', baseUrl);
  const videoRssPath = path.join(publicDir, 'economics-usa-video-spanish.rss');
  fs.writeFileSync(videoRssPath, videoRss);
  console.log(`Generated: ${videoRssPath}`);

  // Generate audio program RSS feed
  const audioRss = generateRssFeed('audio', baseUrl);
  const audioRssPath = path.join(publicDir, 'economics-usa-audio-spanish.rss');
  fs.writeFileSync(audioRssPath, audioRss);
  console.log(`Generated: ${audioRssPath}`);

  console.log('RSS feeds generated successfully!');
}

main();
