import fs from 'fs';
import path from 'path';
import { fileURLToPath } from 'url';

const __filename = fileURLToPath(import.meta.url);
const __dirname = path.dirname(__filename);

const rootDir = path.resolve(__dirname, '../..');
const publicEpisodesDir = path.resolve(__dirname, '../public/episodes');

// Create public/episodes directory if it doesn't exist
if (!fs.existsSync(publicEpisodesDir)) {
  fs.mkdirSync(publicEpisodesDir, { recursive: true });
}

// Get all episode folders
const items = fs.readdirSync(rootDir);
const episodeFolders = items.filter(item => {
  const itemPath = path.join(rootDir, item);
  return fs.statSync(itemPath).isDirectory() && /^\d{2}-/.test(item);
});

console.log(`Found ${episodeFolders.length} episode folders`);

// Create symlinks for each episode folder
for (const folder of episodeFolders) {
  const sourcePath = path.join(rootDir, folder);
  const targetPath = path.join(publicEpisodesDir, folder);

  // Remove existing link/folder if it exists
  if (fs.existsSync(targetPath)) {
    try {
      fs.unlinkSync(targetPath);
    } catch (e) {
      // If it's a directory, remove it
      fs.rmSync(targetPath, { recursive: true, force: true });
    }
  }

  // Create junction (Windows) or symlink (Unix)
  try {
    fs.symlinkSync(sourcePath, targetPath, 'junction');
    console.log(`Linked: ${folder}`);
  } catch (error) {
    console.error(`Failed to link ${folder}:`, error.message);
  }
}

console.log('Episode linking complete!');
