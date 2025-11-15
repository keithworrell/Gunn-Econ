/**
 * Production Deployment Test for https://econ-usa.netlify.app/
 * Tests PDF viewing and audio playback functionality
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
      results.networkRequests.push({
        url,
        status,
        statusText: response.statusText(),
        contentType: response.headers()['content-type'],
        ok: response.ok()
      });

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
      results.errors.push({
        type: 'console',
        message: msg.text()
      });
    }
  });

  try {
    console.log('🌐 Navigating to production site...');
    await page.goto('https://econ-usa.netlify.app/', { waitUntil: 'networkidle' });

    results.tests.push({
      name: 'Site loads',
      status: 'PASS',
      details: 'Successfully loaded homepage'
    });

    // Take screenshot of homepage
    await page.screenshot({ path: 'C:\\Users\\Keith Worrell\\Documents\\Gunn-Econ\\screenshots\\homepage.png', fullPage: true });
    console.log('✓ Homepage loaded');

    // Test Episode 1
    console.log('\n📁 Testing Episode 1: Markets');

    // Click on Episode 1
    const episode1Link = page.locator('text=Episode 1').first();
    await episode1Link.click();
    await page.waitForTimeout(2000);

    results.tests.push({
      name: 'Navigate to Episode 1',
      status: 'PASS',
      details: 'Successfully clicked Episode 1 link'
    });

    await page.screenshot({ path: 'C:\\Users\\Keith Worrell\\Documents\\Gunn-Econ\\screenshots\\episode1-page.png', fullPage: true });

    // TEST 1: PDF Viewing
    console.log('\n📄 Testing PDF viewing...');

    // Try to find and click a PDF link
    const pdfLinks = await page.locator('a[href*=".pdf"]').all();
    console.log(`Found ${pdfLinks.length} PDF links`);

    if (pdfLinks.length > 0) {
      const firstPdfLink = pdfLinks[0];
      const pdfHref = await firstPdfLink.getAttribute('href');
      console.log(`Clicking PDF: ${pdfHref}`);

      await firstPdfLink.click();
      await page.waitForTimeout(3000); // Wait for PDF to load

      // Check if PDF viewer appeared
      const pdfCanvas = await page.locator('canvas').count();
      const pdfViewerExists = pdfCanvas > 0;

      results.tests.push({
        name: 'PDF Viewer Appears',
        status: pdfViewerExists ? 'PASS' : 'FAIL',
        details: `Found ${pdfCanvas} canvas elements (PDF.js renderer)`,
        pdfUrl: pdfHref
      });

      if (pdfViewerExists) {
        console.log(`✓ PDF viewer loaded with ${pdfCanvas} canvas elements`);
      } else {
        console.log('✗ PDF viewer did not load correctly');
        results.errors.push({
          type: 'pdf-viewer',
          message: 'PDF canvas elements not found',
          pdfUrl: pdfHref
        });
      }

      await page.screenshot({ path: 'C:\\Users\\Keith Worrell\\Documents\\Gunn-Econ\\screenshots\\pdf-viewer.png', fullPage: true });

      // Go back to episode page
      await page.goBack();
      await page.waitForTimeout(1000);
    } else {
      results.tests.push({
        name: 'PDF Viewer Test',
        status: 'SKIP',
        details: 'No PDF links found on page'
      });
      console.log('⚠ No PDF links found');
    }

    // TEST 2: Audio Playback
    console.log('\n🎵 Testing audio playback...');

    const audioLinks = await page.locator('a[href*=".mp3"]').all();
    console.log(`Found ${audioLinks.length} audio links`);

    if (audioLinks.length > 0) {
      const firstAudioLink = audioLinks[0];
      const audioHref = await firstAudioLink.getAttribute('href');
      console.log(`Clicking audio: ${audioHref}`);

      await firstAudioLink.click();
      await page.waitForTimeout(3000); // Wait for audio player to load

      // Check if audio player appeared
      const audioElement = await page.locator('audio').count();
      const audioPlayerExists = audioElement > 0;

      results.tests.push({
        name: 'Audio Player Appears',
        status: audioPlayerExists ? 'PASS' : 'FAIL',
        details: `Found ${audioElement} audio elements`,
        audioUrl: audioHref
      });

      if (audioPlayerExists) {
        console.log(`✓ Audio player loaded`);

        // Try to get audio duration
        try {
          const duration = await page.evaluate(() => {
            const audio = document.querySelector('audio');
            return audio ? audio.duration : null;
          });

          const durationLoaded = duration && duration > 0 && isFinite(duration);

          results.tests.push({
            name: 'Audio Metadata Loads',
            status: durationLoaded ? 'PASS' : 'FAIL',
            details: durationLoaded ? `Duration: ${Math.round(duration)}s` : 'Duration not loaded or infinite'
          });

          if (durationLoaded) {
            console.log(`✓ Audio metadata loaded: ${Math.round(duration)}s duration`);
          } else {
            console.log('⚠ Audio duration not loaded yet (may still be loading)');
          }
        } catch (err) {
          results.errors.push({
            type: 'audio-duration',
            message: err.message
          });
        }
      } else {
        console.log('✗ Audio player did not load correctly');
        results.errors.push({
          type: 'audio-player',
          message: 'Audio element not found',
          audioUrl: audioHref
        });
      }

      await page.screenshot({ path: 'C:\\Users\\Keith Worrell\\Documents\\Gunn-Econ\\screenshots\\audio-player.png', fullPage: true });

      // Go back to episode page
      await page.goBack();
      await page.waitForTimeout(1000);
    } else {
      results.tests.push({
        name: 'Audio Player Test',
        status: 'SKIP',
        details: 'No audio links found on page'
      });
      console.log('⚠ No audio links found');
    }

    // TEST 3: Test another episode for consistency
    console.log('\n📁 Testing Episode 2: The Firm (consistency check)');

    await page.goto('https://econ-usa.netlify.app/', { waitUntil: 'networkidle' });

    const episode2Link = page.locator('text=Episode 2').first();
    await episode2Link.click();
    await page.waitForTimeout(2000);

    const episode2PdfLinks = await page.locator('a[href*=".pdf"]').count();
    const episode2AudioLinks = await page.locator('a[href*=".mp3"]').count();

    results.tests.push({
      name: 'Episode 2 Consistency',
      status: (episode2PdfLinks > 0 && episode2AudioLinks > 0) ? 'PASS' : 'FAIL',
      details: `Found ${episode2PdfLinks} PDFs and ${episode2AudioLinks} audio files`
    });

    console.log(`✓ Episode 2 has ${episode2PdfLinks} PDFs and ${episode2AudioLinks} audio files`);

    await page.screenshot({ path: 'C:\\Users\\Keith Worrell\\Documents\\Gunn-Econ\\screenshots\\episode2-page.png', fullPage: true });

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
  const skipped = results.tests.filter(t => t.status === 'SKIP').length;

  console.log(`\n✓ Passed: ${passed}`);
  console.log(`✗ Failed: ${failed}`);
  console.log(`⊘ Skipped: ${skipped}`);
  console.log(`\n🌐 Network Requests: ${results.networkRequests.length}`);
  console.log(`❌ Errors: ${results.errors.length}`);

  console.log('\n📋 Test Details:');
  results.tests.forEach(test => {
    const icon = test.status === 'PASS' ? '✓' : test.status === 'FAIL' ? '✗' : '⊘';
    console.log(`${icon} ${test.name}: ${test.status}`);
    if (test.details) {
      console.log(`  ${test.details}`);
    }
  });

  if (results.networkRequests.length > 0) {
    console.log('\n🌐 Network Requests:');
    results.networkRequests.forEach(req => {
      const icon = req.ok ? '✓' : '✗';
      const fileName = req.url.split('/').pop().substring(0, 50);
      console.log(`${icon} ${req.status} - ${fileName}`);
    });
  }

  if (results.errors.length > 0) {
    console.log('\n❌ Errors Found:');
    results.errors.forEach((err, i) => {
      console.log(`${i + 1}. [${err.type}] ${err.message}`);
    });
  }

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
