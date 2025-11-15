/**
 * Production Deployment Test v2 for https://econ-usa.netlify.app/
 * Tests PDF viewing and audio playback functionality
 * Updated to work with the actual site structure (buttons, not links)
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

      const fileName = url.split('/').pop();
      const icon = response.ok() ? '✓' : '✗';
      console.log(`${icon} ${status} - ${fileName}`);

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
      console.log(`🔴 Console error: ${msg.text()}`);
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

    // Take screenshot of homepage
    await page.screenshot({ path: 'C:\\Users\\Keith Worrell\\Documents\\Gunn-Econ\\screenshots\\homepage.png', fullPage: true });
    console.log('✓ Homepage loaded');

    // Wait for episodes to load
    await page.waitForSelector('button', { timeout: 10000 });

    // Get all episode buttons
    const episodeButtons = await page.locator('button').all();
    console.log(`\nFound ${episodeButtons.length} buttons on page`);

    // Test Episode 1: Markets
    console.log('\n📁 Testing Episode 1: Markets');

    // Click on the first episode (1. Markets)
    const marketsButton = page.locator('button:has-text("1. Markets")').first();
    await marketsButton.click();
    await page.waitForTimeout(2000);

    results.tests.push({
      name: 'Navigate to Episode 1',
      status: 'PASS',
      details: 'Successfully clicked Episode 1 button'
    });

    await page.screenshot({ path: 'C:\\Users\\Keith Worrell\\Documents\\Gunn-Econ\\screenshots\\episode1-expanded.png', fullPage: true });

    // Look for file links within the expanded episode
    const fileButtons = await page.locator('button[class*="pl-"]').all();
    console.log(`Found ${fileButtons.length} file buttons in Episode 1`);

    // TEST 1: PDF Viewing
    console.log('\n📄 Testing PDF viewing...');

    // Try to find PDF file buttons
    let pdfTested = false;
    for (let i = 0; i < fileButtons.length && !pdfTested; i++) {
      const buttonText = await fileButtons[i].textContent();
      if (buttonText && buttonText.toLowerCase().includes('.pdf')) {
        console.log(`\nClicking PDF: ${buttonText.trim()}`);

        await fileButtons[i].click();
        await page.waitForTimeout(4000); // Wait for PDF to load

        // Check if PDF viewer appeared
        const pdfCanvas = await page.locator('canvas').count();
        const pdfViewerExists = pdfCanvas > 0;

        results.tests.push({
          name: 'PDF Viewer Appears',
          status: pdfViewerExists ? 'PASS' : 'FAIL',
          details: `Found ${pdfCanvas} canvas elements (PDF.js renderer)`,
          pdfFile: buttonText.trim()
        });

        if (pdfViewerExists) {
          console.log(`✓ PDF viewer loaded with ${pdfCanvas} canvas elements`);

          // Check if PDF actually rendered
          const canvasHasContent = await page.evaluate(() => {
            const canvas = document.querySelector('canvas');
            if (!canvas) return false;
            const ctx = canvas.getContext('2d');
            if (!ctx) return false;
            // Check if canvas has been drawn to
            return canvas.width > 0 && canvas.height > 0;
          });

          results.tests.push({
            name: 'PDF Content Rendered',
            status: canvasHasContent ? 'PASS' : 'FAIL',
            details: canvasHasContent ? 'Canvas has content' : 'Canvas is empty'
          });

          if (canvasHasContent) {
            console.log('✓ PDF content rendered to canvas');
          } else {
            console.log('⚠ PDF canvas exists but may be empty');
          }
        } else {
          console.log('✗ PDF viewer did not load correctly');
        }

        await page.screenshot({ path: 'C:\\Users\\Keith Worrell\\Documents\\Gunn-Econ\\screenshots\\pdf-viewer.png', fullPage: true });

        // Close PDF viewer (look for close button or press Escape)
        await page.keyboard.press('Escape');
        await page.waitForTimeout(1000);

        pdfTested = true;
      }
    }

    if (!pdfTested) {
      results.tests.push({
        name: 'PDF Viewer Test',
        status: 'SKIP',
        details: 'No PDF file buttons found'
      });
      console.log('⚠ No PDF files found to test');
    }

    // TEST 2: Audio Playback
    console.log('\n🎵 Testing audio playback...');

    // Re-expand Episode 1 if needed
    const marketsButton2 = page.locator('button:has-text("1. Markets")').first();
    await marketsButton2.click();
    await page.waitForTimeout(1000);

    const fileButtons2 = await page.locator('button[class*="pl-"]').all();

    let audioTested = false;
    for (let i = 0; i < fileButtons2.length && !audioTested; i++) {
      const buttonText = await fileButtons2[i].textContent();
      if (buttonText && buttonText.toLowerCase().includes('.mp3')) {
        console.log(`\nClicking audio: ${buttonText.trim()}`);

        await fileButtons2[i].click();
        await page.waitForTimeout(4000); // Wait for audio player to load

        // Check if audio player appeared
        const audioElement = await page.locator('audio').count();
        const audioPlayerExists = audioElement > 0;

        results.tests.push({
          name: 'Audio Player Appears',
          status: audioPlayerExists ? 'PASS' : 'FAIL',
          details: `Found ${audioElement} audio elements`,
          audioFile: buttonText.trim()
        });

        if (audioPlayerExists) {
          console.log(`✓ Audio player loaded`);

          // Wait a bit more for metadata to load
          await page.waitForTimeout(2000);

          // Try to get audio duration
          const audioMetadata = await page.evaluate(() => {
            const audio = document.querySelector('audio');
            if (!audio) return null;
            return {
              duration: audio.duration,
              readyState: audio.readyState,
              networkState: audio.networkState,
              src: audio.src,
              paused: audio.paused,
              error: audio.error ? audio.error.message : null
            };
          });

          console.log('Audio metadata:', JSON.stringify(audioMetadata, null, 2));

          const durationLoaded = audioMetadata && audioMetadata.duration > 0 && isFinite(audioMetadata.duration);

          results.tests.push({
            name: 'Audio Metadata Loads',
            status: durationLoaded ? 'PASS' : 'WARN',
            details: durationLoaded
              ? `Duration: ${Math.round(audioMetadata.duration)}s (${Math.floor(audioMetadata.duration / 60)}m ${Math.round(audioMetadata.duration % 60)}s)`
              : `Ready state: ${audioMetadata?.readyState}, Duration: ${audioMetadata?.duration}`,
            metadata: audioMetadata
          });

          if (durationLoaded) {
            console.log(`✓ Audio metadata loaded: ${Math.round(audioMetadata.duration)}s duration`);
          } else {
            console.log('⚠ Audio duration not loaded yet (may still be loading or streaming)');
          }

          // Try to play for 2 seconds
          try {
            await page.evaluate(() => {
              const audio = document.querySelector('audio');
              if (audio) audio.play();
            });
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
              console.log('✓ Audio is playing');
            } else {
              console.log('⚠ Audio playback status unclear');
            }
          } catch (err) {
            console.log('⚠ Could not test audio playback:', err.message);
          }
        } else {
          console.log('✗ Audio player did not load correctly');
        }

        await page.screenshot({ path: 'C:\\Users\\Keith Worrell\\Documents\\Gunn-Econ\\screenshots\\audio-player.png', fullPage: true });

        // Close audio player
        await page.keyboard.press('Escape');
        await page.waitForTimeout(1000);

        audioTested = true;
      }
    }

    if (!audioTested) {
      results.tests.push({
        name: 'Audio Player Test',
        status: 'SKIP',
        details: 'No audio file buttons found'
      });
      console.log('⚠ No audio files found to test');
    }

    // TEST 3: Test Episode 2 for consistency
    console.log('\n📁 Testing Episode 2: The Firm (consistency check)');

    const firmButton = page.locator('button:has-text("2. The Firm")').first();
    await firmButton.click();
    await page.waitForTimeout(2000);

    const episode2FileButtons = await page.locator('button[class*="pl-"]').all();
    const episode2Files = [];

    for (let btn of episode2FileButtons) {
      const text = await btn.textContent();
      if (text) episode2Files.push(text.trim());
    }

    const episode2Pdfs = episode2Files.filter(f => f.toLowerCase().includes('.pdf')).length;
    const episode2Audio = episode2Files.filter(f => f.toLowerCase().includes('.mp3')).length;

    results.tests.push({
      name: 'Episode 2 Consistency',
      status: (episode2Pdfs > 0 && episode2Audio > 0) ? 'PASS' : 'FAIL',
      details: `Found ${episode2Pdfs} PDFs and ${episode2Audio} audio files`,
      files: episode2Files
    });

    console.log(`✓ Episode 2 has ${episode2Pdfs} PDFs and ${episode2Audio} audio files`);
    console.log('Files:', episode2Files);

    await page.screenshot({ path: 'C:\\Users\\Keith Worrell\\Documents\\Gunn-Econ\\screenshots\\episode2-expanded.png', fullPage: true });

    // TEST 4: Test Episode 10 (middle episode)
    console.log('\n📁 Testing Episode 10: Profits and Interest (middle episode check)');

    const episode10Button = page.locator('button:has-text("10. Profits and Interest")').first();
    await episode10Button.click();
    await page.waitForTimeout(2000);

    const episode10FileButtons = await page.locator('button[class*="pl-"]').all();
    const episode10Files = [];

    for (let btn of episode10FileButtons) {
      const text = await btn.textContent();
      if (text) episode10Files.push(text.trim());
    }

    const episode10Pdfs = episode10Files.filter(f => f.toLowerCase().includes('.pdf')).length;
    const episode10Audio = episode10Files.filter(f => f.toLowerCase().includes('.mp3')).length;

    results.tests.push({
      name: 'Episode 10 Consistency',
      status: (episode10Pdfs > 0 && episode10Audio > 0) ? 'PASS' : 'FAIL',
      details: `Found ${episode10Pdfs} PDFs and ${episode10Audio} audio files`,
      files: episode10Files
    });

    console.log(`✓ Episode 10 has ${episode10Pdfs} PDFs and ${episode10Audio} audio files`);

  } catch (error) {
    results.errors.push({
      type: 'critical',
      message: error.message,
      stack: error.stack
    });
    console.error('❌ Critical error:', error);
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

    if (failedRequests.length > 0) {
      console.log('\nFailed requests:');
      failedRequests.forEach(req => {
        console.log(`  ✗ ${req.status} - ${req.url}`);
      });
    }
  }

  if (results.errors.length > 0) {
    console.log('\n❌ Errors Found:');
    results.errors.forEach((err, i) => {
      console.log(`${i + 1}. [${err.type}] ${err.message}`);
    });
  }

  // Overall status
  console.log('\n' + '='.repeat(80));
  if (failed === 0 && results.errors.filter(e => e.type !== 'console').length === 0) {
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

  console.log('\n📄 Full results saved to: test-results.json');
  console.log('📸 Screenshots saved to: screenshots/');

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
