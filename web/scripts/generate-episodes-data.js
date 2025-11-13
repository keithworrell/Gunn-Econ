import fs from 'fs';
import path from 'path';
import { fileURLToPath } from 'url';

const __filename = fileURLToPath(import.meta.url);
const __dirname = path.dirname(__filename);

const rootDir = path.resolve(__dirname, '../..');
const episodesOutputPath = path.resolve(__dirname, '../src/data/episodes.json');

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

// Content type labels
const contentLabels = {
  'video-english': 'Video Transcript (English)',
  'audio-english': 'Audio Transcript (English)',
  'video-spanish': 'Transcripción de Video (Español)',
  'audio-spanish': 'Transcripción de Audio (Español)',
  'video-audio-spanish': 'Audio de Video (Español)',
  'audio-audio-spanish': 'Audio de Audio (Español)',
};

function generateEpisodesData() {
  const episodes = [];

  for (const episode of episodeMetadata) {
    const episodePath = path.join(rootDir, episode.folder);

    if (!fs.existsSync(episodePath)) {
      console.warn(`Warning: Episode folder not found: ${episode.folder}`);
      continue;
    }

    const files = fs.readdirSync(episodePath);
    const contents = [];

    // Detect and categorize files
    for (const file of files) {
      const filePath = `episodes/${episode.folder}/${file}`;

      if (file.endsWith('-video.pdf')) {
        contents.push({
          type: 'video-english',
          format: 'pdf',
          fileName: file,
          path: filePath,
          label: contentLabels['video-english']
        });
      } else if (file.endsWith('-audio.pdf') && !file.includes('spanish')) {
        contents.push({
          type: 'audio-english',
          format: 'pdf',
          fileName: file,
          path: filePath,
          label: contentLabels['audio-english']
        });
      } else if (file.endsWith('-video-spanish.pdf')) {
        contents.push({
          type: 'video-spanish',
          format: 'pdf',
          fileName: file,
          path: filePath,
          label: contentLabels['video-spanish']
        });
      } else if (file.endsWith('-audio-spanish.pdf')) {
        contents.push({
          type: 'audio-spanish',
          format: 'pdf',
          fileName: file,
          path: filePath,
          label: contentLabels['audio-spanish']
        });
      } else if (file.endsWith('-video-spanish-spanish.mp3')) {
        contents.push({
          type: 'video-audio-spanish',
          format: 'mp3',
          fileName: file,
          path: filePath,
          label: contentLabels['video-audio-spanish']
        });
      } else if (file.endsWith('-audio-spanish-spanish.mp3')) {
        contents.push({
          type: 'audio-audio-spanish',
          format: 'mp3',
          fileName: file,
          path: filePath,
          label: contentLabels['audio-audio-spanish']
        });
      }
    }

    episodes.push({
      id: episode.num,
      number: episode.num,
      title: episode.title,
      folder: episode.folder,
      contents: contents
    });
  }

  // Ensure data directory exists
  const dataDir = path.dirname(episodesOutputPath);
  if (!fs.existsSync(dataDir)) {
    fs.mkdirSync(dataDir, { recursive: true });
  }

  // Write episodes.json
  fs.writeFileSync(episodesOutputPath, JSON.stringify(episodes, null, 2));
  console.log(`Generated episodes data: ${episodesOutputPath}`);
  console.log(`Total episodes: ${episodes.length}`);
}

generateEpisodesData();
