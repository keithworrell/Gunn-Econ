/**
 * Quick audio-only test for production deployment
 */

import { chromium } from 'playwright';
import fs from 'fs';

async function testAudio() {
  const browser = await chromium.launch({ headless: false });
  const context = await browser.newContext();
  const page = await context.newPage();

  const results = [];

  // Monitor network requests
  page.on('response', async (response) => {
    const url = response.url();
    const status = response.status();

    if (url.includes('.mp3')) {
      const fileName = url.split('/').pop().substring(0, 50);
      const icon = response.ok() ? '✓' : '✗';
      console.log(`  ${icon} HTTP ${status} - ${fileName}`);
    }
  });

  try {
    console.log('🌐 Navigating to production site...');
    await page.goto('https://econ-usa.netlify.app/', { waitUntil: 'networkidle', timeout: 60000 });
    console.log('✓ Homepage loaded\n');

    // Expand Episode 1
    console.log('📁 Opening Episode 1: Markets');
    const marketsButton = page.locator('button:has-text("1. Markets")').first();
    await marketsButton.click();
    await page.waitForTimeout(2000);

    // Find ALL buttons and filter for audio
    const allButtons = await page.locator('button').all();
    console.log(`\nFound ${allButtons.length} total buttons`);

    for (let btn of allButtons) {
      const text = await btn.textContent();
      if (text && text.trim()) {
        const trimmed = text.trim();
        if (trimmed.startsWith('Audio de')) {
          console.log(`\n🎵 Testing: ${trimmed}`);

          await btn.click();
          await page.waitForTimeout(5000);

          const audioCount = await page.locator('audio').count();
          console.log(`  Audio elements found: ${audioCount}`);

          if (audioCount > 0) {
            await page.waitForTimeout(3000);

            const metadata = await page.evaluate(() => {
              const audio = document.querySelector('audio');
              if (!audio) return null;
              return {
                duration: audio.duration,
                readyState: audio.readyState,
                src: audio.src?.substring(audio.src.lastIndexOf('/') + 1),
                paused: audio.paused,
                error: audio.error ? audio.error.message : null
              };
            });

            console.log(`  Metadata:`, JSON.stringify(metadata, null, 2));

            if (metadata && metadata.duration > 0 && isFinite(metadata.duration)) {
              const minutes = Math.floor(metadata.duration / 60);
              const seconds = Math.round(metadata.duration % 60);
              console.log(`  ✓ Duration loaded: ${minutes}:${String(seconds).padStart(2, '0')}`);
              results.push({ file: trimmed, status: 'PASS', duration: metadata.duration });
            } else {
              console.log(`  ⚠ Duration not loaded (readyState: ${metadata?.readyState})`);
              results.push({ file: trimmed, status: 'WARN', metadata });
            }

            await page.screenshot({
              path: `C:\\Users\\Keith Worrell\\Documents\\Gunn-Econ\\screenshots\\audio-${Date.now()}.png`,
              fullPage: true
            });

            await page.keyboard.press('Escape');
            await page.waitForTimeout(1000);
          }

          break; // Test only first audio file
        }
      }
    }

  } catch (error) {
    console.error('❌ Error:', error.message);
  } finally {
    await browser.close();
  }

  console.log('\n📊 Results:', results);
  fs.writeFileSync(
    'C:\\Users\\Keith Worrell\\Documents\\Gunn-Econ\\audio-test-results.json',
    JSON.stringify(results, null, 2)
  );
}

testAudio();
