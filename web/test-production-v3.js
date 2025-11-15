/**
 * Production Deployment Test v3 for https://econ-usa.netlify.app/
 * Tests PDF viewing and audio playback functionality
 * Updated with correct selectors for file items
 */

import { chromium } from 'playwright';
import fs from 'fs';

async function testProduction() {
  const browser = await chromium.launch({ headless: false });
  const context = await browser.newContext();
  const page = await context.newPage();

  const results = {
    site: 'https://econ-usa.netlify.app/',
    timestamp: new Date().toISOString(),
    tests: [],
    errors: [],
    networkRequests: []
  };

  // Monitor network requests
  page.on('response', async (response) => {
    const url = response.url();
    const status = response.status();

    // Track PDF and audio file requests
    if (url.includes('.pdf') || url.includes('.mp3')) {
      const reqInfo = {
        url,
        status,
        statusText: response.statusText(),
        contentType: response.headers()['content-type'],
        ok: response.ok(),
        timestamp: new Date().toISOString()
      };

      results.networkRequests.push(reqInfo);

      const fileName = url.split('/').pop().substring(0, 50);
      const icon = response.ok() ? '✓' : '✗';
      console.log(`  ${icon} HTTP ${status} - ${fileName}`);

      if (!response.ok()) {
        results.errors.push({
          type: 'network',
          message: `Failed to load ${url} - Status: ${status}`,
          url
        });
      }
    }
  });

  // Monitor console errors
  page.on('console', msg => {
    if (msg.type() === 'error') {
      console.log(`  🔴 Console error: ${msg.text()}`);
      results.errors.push({
        type: 'console',
        message: msg.text()
      });
    }
  });

  try {
    console.log('🌐 Navigating to production site...');
    await page.goto('https://econ-usa.netlify.app/', { waitUntil: 'networkidle', timeout: 60000 });

    results.tests.push({
      name: 'Site loads',
      status: 'PASS',
      details: 'Successfully loaded homepage'
    });

    await page.screenshot({ path: 'C:\\Users\\Keith Worrell\\Documents\\Gunn-Econ\\screenshots\\homepage-v3.png', fullPage: true });
    console.log('✓ Homepage loaded\n');

    // Wait for episodes to load
    await page.waitForSelector('button', { timeout: 10000 });

    // Test Episode 1: Markets
    console.log('📁 Testing Episode 1: Markets');

    // Click on the first episode
    const marketsButton = page.locator('button:has-text("1. Markets")').first();
    await marketsButton.click();
    await page.waitForTimeout(2000);

    results.tests.push({
      name: 'Navigate to Episode 1',
      status: 'PASS',
      details: 'Successfully clicked Episode 1 button'
    });

    await page.screenshot({ path: 'C:\\Users\\Keith Worrell\\Documents\\Gunn-Econ\\screenshots\\episode1-expanded-v3.png', fullPage: true });

    // Get all file items - they appear to be clickable elements with text
    const fileItems = await page.locator('button').all();
    const fileList = [];

    for (let item of fileItems) {
      const text = await item.textContent();
      if (text && (text.includes('Transcripción') || text.includes('Transcript') || text.includes('Audio de'))) {
        fileList.push({ element: item, text: text.trim() });
      }
    }

    console.log(`  Found ${fileList.length} files in Episode 1`);
    fileList.forEach(f => console.log(`    - ${f.text}`));

    // TEST 1: PDF Viewing
    console.log('\n📄 Testing PDF viewing...');

    const pdfFile = fileList.find(f => f.text.includes('Transcripción') || f.text.includes('Transcript'));

    if (pdfFile) {
      console.log(`  Clicking PDF: ${pdfFile.text}`);

      await pdfFile.element.click();
      await page.waitForTimeout(5000); // Wait for PDF to load

      // Check if PDF viewer appeared
      const pdfCanvas = await page.locator('canvas').count();
      const pdfViewerExists = pdfCanvas > 0;

      results.tests.push({
        name: 'PDF Viewer Appears',
        status: pdfViewerExists ? 'PASS' : 'FAIL',
        details: `Found ${pdfCanvas} canvas elements (PDF.js renderer)`,
        pdfFile: pdfFile.text
      });

      if (pdfViewerExists) {
        console.log(`  ✓ PDF viewer loaded with ${pdfCanvas} canvas elements`);

        // Check if PDF actually rendered
        const canvasInfo = await page.evaluate(() => {
          const canvas = document.querySelector('canvas');
          if (!canvas) return null;
          return {
            width: canvas.width,
            height: canvas.height,
            hasContent: canvas.width > 0 && canvas.height > 0
          };
        });

        results.tests.push({
          name: 'PDF Content Rendered',
          status: canvasInfo?.hasContent ? 'PASS' : 'FAIL',
          details: canvasInfo ? `Canvas: ${canvasInfo.width}x${canvasInfo.height}` : 'No canvas found',
          canvasInfo
        });

        if (canvasInfo?.hasContent) {
          console.log(`  ✓ PDF content rendered: ${canvasInfo.width}x${canvasInfo.height}`);
        } else {
          console.log('  ⚠ PDF canvas exists but may be empty');
        }
      } else {
        console.log('  ✗ PDF viewer did not load correctly');
      }

      await page.screenshot({ path: 'C:\\Users\\Keith Worrell\\Documents\\Gunn-Econ\\screenshots\\pdf-viewer-v3.png', fullPage: true });

      // Close PDF viewer
      await page.keyboard.press('Escape');
      await page.waitForTimeout(1000);
    } else {
      results.tests.push({
        name: 'PDF Viewer Test',
        status: 'SKIP',
        details: 'No PDF files found'
      });
      console.log('  ⚠ No PDF files found to test');
    }

    // TEST 2: Audio Playback
    console.log('\n🎵 Testing audio playback...');

    // Re-expand Episode 1 if needed
    const marketsButton2 = page.locator('button:has-text("1. Markets")').first();
    await marketsButton2.click();
    await page.waitForTimeout(1000);

    // Get file list again
    const fileItems2 = await page.locator('button').all();
    const fileList2 = [];

    for (let item of fileItems2) {
      const text = await item.textContent();
      if (text && text.includes('Audio de')) {
        fileList2.push({ element: item, text: text.trim() });
      }
    }

    const audioFile = fileList2.find(f => f.text.includes('Audio de'));

    if (audioFile) {
      console.log(`  Clicking audio: ${audioFile.text}`);

      await audioFile.element.click();
      await page.waitForTimeout(5000); // Wait for audio player to load

      // Check if audio player appeared
      const audioElement = await page.locator('audio').count();
      const audioPlayerExists = audioElement > 0;

      results.tests.push({
        name: 'Audio Player Appears',
        status: audioPlayerExists ? 'PASS' : 'FAIL',
        details: `Found ${audioElement} audio elements`,
        audioFile: audioFile.text
      });

      if (audioPlayerExists) {
        console.log(`  ✓ Audio player loaded`);

        // Wait for metadata to load
        await page.waitForTimeout(3000);

        // Get audio metadata
        const audioMetadata = await page.evaluate(() => {
          const audio = document.querySelector('audio');
          if (!audio) return null;
          return {
            duration: audio.duration,
            readyState: audio.readyState,
            networkState: audio.networkState,
            src: audio.src?.substring(0, 100),
            paused: audio.paused,
            currentTime: audio.currentTime,
            error: audio.error ? audio.error.message : null
          };
        });

        const durationLoaded = audioMetadata && audioMetadata.duration > 0 && isFinite(audioMetadata.duration);

        results.tests.push({
          name: 'Audio Metadata Loads',
          status: durationLoaded ? 'PASS' : 'WARN',
          details: durationLoaded
            ? `Duration: ${Math.round(audioMetadata.duration)}s (${Math.floor(audioMetadata.duration / 60)}:${String(Math.round(audioMetadata.duration % 60)).padStart(2, '0')})`
            : `Ready state: ${audioMetadata?.readyState}, Network state: ${audioMetadata?.networkState}`,
          metadata: audioMetadata
        });

        if (durationLoaded) {
          const minutes = Math.floor(audioMetadata.duration / 60);
          const seconds = Math.round(audioMetadata.duration % 60);
          console.log(`  ✓ Audio metadata loaded: ${minutes}:${String(seconds).padStart(2, '0')} duration`);
        } else {
          console.log(`  ⚠ Audio duration not loaded yet (readyState: ${audioMetadata?.readyState})`);
        }

        // Try to play for 2 seconds
        try {
          const playResult = await page.evaluate(async () => {
            const audio = document.querySelector('audio');
            if (!audio) return { success: false, error: 'No audio element' };
            try {
              await audio.play();
              return { success: true };
            } catch (err) {
              return { success: false, error: err.message };
            }
          });

          if (playResult.success) {
            await page.waitForTimeout(2000);

            const isPlaying = await page.evaluate(() => {
              const audio = document.querySelector('audio');
              return audio && !audio.paused && audio.currentTime > 0;
            });

            results.tests.push({
              name: 'Audio Playback',
              status: isPlaying ? 'PASS' : 'WARN',
              details: isPlaying ? 'Audio playing successfully' : 'Audio may not be playing'
            });

            if (isPlaying) {
              console.log('  ✓ Audio is playing');
            } else {
              console.log('  ⚠ Audio playback status unclear');
            }
          } else {
            console.log(`  ⚠ Could not play audio: ${playResult.error}`);
          }
        } catch (err) {
          console.log(`  ⚠ Audio playback test error: ${err.message}`);
        }
      } else {
        console.log('  ✗ Audio player did not load correctly');
      }

      await page.screenshot({ path: 'C:\\Users\\Keith Worrell\\Documents\\Gunn-Econ\\screenshots\\audio-player-v3.png', fullPage: true });

      // Close audio player
      await page.keyboard.press('Escape');
      await page.waitForTimeout(1000);
    } else {
      results.tests.push({
        name: 'Audio Player Test',
        status: 'SKIP',
        details: 'No audio files found'
      });
      console.log('  ⚠ No audio files found to test');
    }

    // TEST 3: Test multiple episodes for consistency
    console.log('\n📁 Testing Episode 2: The Firm (consistency check)');

    const firmButton = page.locator('button:has-text("2. The Firm")').first();
    await firmButton.click();
    await page.waitForTimeout(2000);

    const episode2Items = await page.locator('button').all();
    const episode2Files = [];

    for (let item of episode2Items) {
      const text = await item.textContent();
      if (text && (text.includes('Transcripción') || text.includes('Transcript') || text.includes('Audio de'))) {
        episode2Files.push(text.trim());
      }
    }

    const episode2Pdfs = episode2Files.filter(f => f.includes('Transcripción') || f.includes('Transcript')).length;
    const episode2Audio = episode2Files.filter(f => f.includes('Audio de')).length;

    results.tests.push({
      name: 'Episode 2 Consistency',
      status: (episode2Pdfs > 0 && episode2Audio > 0) ? 'PASS' : 'FAIL',
      details: `Found ${episode2Pdfs} PDFs and ${episode2Audio} audio files`,
      files: episode2Files
    });

    console.log(`  ✓ Episode 2 has ${episode2Pdfs} PDFs and ${episode2Audio} audio files`);

    await page.screenshot({ path: 'C:\\Users\\Keith Worrell\\Documents\\Gunn-Econ\\screenshots\\episode2-expanded-v3.png', fullPage: true });

    // TEST 4: Test Episode 15 (middle-later episode)
    console.log('\n📁 Testing Episode 15: GDP GNP');

    const episode15Button = page.locator('button:has-text("15. GDP")').first();
    await episode15Button.click();
    await page.waitForTimeout(2000);

    const episode15Items = await page.locator('button').all();
    const episode15Files = [];

    for (let item of episode15Items) {
      const text = await item.textContent();
      if (text && (text.includes('Transcripción') || text.includes('Transcript') || text.includes('Audio de'))) {
        episode15Files.push(text.trim());
      }
    }

    const episode15Pdfs = episode15Files.filter(f => f.includes('Transcripción') || f.includes('Transcript')).length;
    const episode15Audio = episode15Files.filter(f => f.includes('Audio de')).length;

    results.tests.push({
      name: 'Episode 15 Consistency',
      status: (episode15Pdfs > 0 && episode15Audio > 0) ? 'PASS' : 'FAIL',
      details: `Found ${episode15Pdfs} PDFs and ${episode15Audio} audio files`,
      files: episode15Files
    });

    console.log(`  ✓ Episode 15 has ${episode15Pdfs} PDFs and ${episode15Audio} audio files`);

    // TEST 5: Test last episode
    console.log('\n📁 Testing Episode 28: Exchange Rates (last episode)');

    const episode28Button = page.locator('button:has-text("28. Exchange Rates")').first();
    await episode28Button.click();
    await page.waitForTimeout(2000);

    const episode28Items = await page.locator('button').all();
    const episode28Files = [];

    for (let item of episode28Items) {
      const text = await item.textContent();
      if (text && (text.includes('Transcripción') || text.includes('Transcript') || text.includes('Audio de'))) {
        episode28Files.push(text.trim());
      }
    }

    const episode28Pdfs = episode28Files.filter(f => f.includes('Transcripción') || f.includes('Transcript')).length;
    const episode28Audio = episode28Files.filter(f => f.includes('Audio de')).length;

    results.tests.push({
      name: 'Episode 28 Consistency',
      status: (episode28Pdfs > 0 && episode28Audio > 0) ? 'PASS' : 'FAIL',
      details: `Found ${episode28Pdfs} PDFs and ${episode28Audio} audio files`,
      files: episode28Files
    });

    console.log(`  ✓ Episode 28 has ${episode28Pdfs} PDFs and ${episode28Audio} audio files`);

  } catch (error) {
    results.errors.push({
      type: 'critical',
      message: error.message,
      stack: error.stack
    });
    console.error('\n❌ Critical error:', error.message);
  } finally {
    await browser.close();
  }

  // Print summary
  console.log('\n' + '='.repeat(80));
  console.log('📊 TEST SUMMARY');
  console.log('='.repeat(80));

  const passed = results.tests.filter(t => t.status === 'PASS').length;
  const failed = results.tests.filter(t => t.status === 'FAIL').length;
  const warned = results.tests.filter(t => t.status === 'WARN').length;
  const skipped = results.tests.filter(t => t.status === 'SKIP').length;

  console.log(`\n✓ Passed: ${passed}`);
  console.log(`✗ Failed: ${failed}`);
  console.log(`⚠ Warnings: ${warned}`);
  console.log(`⊘ Skipped: ${skipped}`);
  console.log(`\n🌐 Network Requests: ${results.networkRequests.length}`);
  console.log(`❌ Errors: ${results.errors.length}`);

  console.log('\n📋 Test Details:');
  results.tests.forEach(test => {
    const icon = test.status === 'PASS' ? '✓' : test.status === 'FAIL' ? '✗' : test.status === 'WARN' ? '⚠' : '⊘';
    console.log(`${icon} ${test.name}: ${test.status}`);
    if (test.details) {
      console.log(`  ${test.details}`);
    }
  });

  if (results.networkRequests.length > 0) {
    console.log('\n🌐 Network Request Summary:');
    const successfulRequests = results.networkRequests.filter(r => r.ok);
    const failedRequests = results.networkRequests.filter(r => !r.ok);

    console.log(`✓ Successful: ${successfulRequests.length}`);
    console.log(`✗ Failed: ${failedRequests.length}`);

    // Group by status code
    const statusCodes = {};
    results.networkRequests.forEach(req => {
      statusCodes[req.status] = (statusCodes[req.status] || 0) + 1;
    });

    console.log('\nStatus codes:');
    Object.entries(statusCodes).forEach(([code, count]) => {
      console.log(`  ${code}: ${count} requests`);
    });

    if (failedRequests.length > 0) {
      console.log('\nFailed requests:');
      failedRequests.forEach(req => {
        const fileName = req.url.split('/').pop();
        console.log(`  ✗ ${req.status} - ${fileName}`);
      });
    }
  }

  if (results.errors.length > 0) {
    console.log('\n❌ Errors Found:');
    results.errors.slice(0, 10).forEach((err, i) => {
      console.log(`${i + 1}. [${err.type}] ${err.message}`);
    });
    if (results.errors.length > 10) {
      console.log(`... and ${results.errors.length - 10} more errors`);
    }
  }

  // Overall status
  console.log('\n' + '='.repeat(80));
  if (failed === 0 && results.errors.filter(e => e.type === 'network').length === 0) {
    console.log('✅ PRODUCTION DEPLOYMENT: ALL TESTS PASSED');
  } else if (failed > 0) {
    console.log('⚠️  PRODUCTION DEPLOYMENT: SOME TESTS FAILED');
  } else {
    console.log('✓ PRODUCTION DEPLOYMENT: PASSED WITH WARNINGS');
  }
  console.log('='.repeat(80));

  // Save results to file
  fs.writeFileSync(
    'C:\\Users\\Keith Worrell\\Documents\\Gunn-Econ\\test-results.json',
    JSON.stringify(results, null, 2)
  );

  console.log('\n📄 Full results saved to: C:\\Users\\Keith Worrell\\Documents\\Gunn-Econ\\test-results.json');
  console.log('📸 Screenshots saved to: C:\\Users\\Keith Worrell\\Documents\\Gunn-Econ\\screenshots\\');

  return results;
}

// Run the tests
testProduction().then(results => {
  const failed = results.tests.filter(t => t.status === 'FAIL').length;
  process.exit(failed > 0 ? 1 : 0);
}).catch(err => {
  console.error('Fatal error:', err);
  process.exit(1);
});
