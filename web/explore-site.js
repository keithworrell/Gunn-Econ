/**
 * Explore the production site structure
 */

import { chromium } from 'playwright';
import fs from 'fs';

async function exploreSite() {
  const browser = await chromium.launch({ headless: false });
  const context = await browser.newContext();
  const page = await context.newPage();

  try {
    console.log('🌐 Navigating to production site...');
    await page.goto('https://econ-usa.netlify.app/', { waitUntil: 'networkidle', timeout: 60000 });

    console.log('✓ Homepage loaded');

    // Take screenshot
    await page.screenshot({ path: 'C:\\Users\\Keith Worrell\\Documents\\Gunn-Econ\\screenshots\\homepage.png', fullPage: true });

    // Get page title
    const title = await page.title();
    console.log(`Page title: ${title}`);

    // Get all links
    const links = await page.evaluate(() => {
      const allLinks = Array.from(document.querySelectorAll('a'));
      return allLinks.map(link => ({
        text: link.textContent.trim(),
        href: link.getAttribute('href'),
        visible: link.offsetWidth > 0 && link.offsetHeight > 0
      }));
    });

    console.log(`\nFound ${links.length} links on the page:`);
    links.slice(0, 20).forEach((link, i) => {
      console.log(`${i + 1}. "${link.text}" -> ${link.href} (visible: ${link.visible})`);
    });

    // Look for episode-related links
    const episodeLinks = links.filter(link =>
      link.text.toLowerCase().includes('episode') ||
      link.text.toLowerCase().includes('market') ||
      link.href?.includes('episode') ||
      link.href?.includes('01-')
    );

    console.log(`\n📚 Episode-related links (${episodeLinks.length}):`);
    episodeLinks.forEach((link, i) => {
      console.log(`${i + 1}. "${link.text}" -> ${link.href}`);
    });

    // Get page structure
    const structure = await page.evaluate(() => {
      const getStructure = (element, depth = 0) => {
        if (depth > 3) return null;
        const children = Array.from(element.children);
        return {
          tag: element.tagName,
          id: element.id || undefined,
          class: element.className || undefined,
          text: element.textContent?.substring(0, 100),
          children: children.map(child => getStructure(child, depth + 1)).filter(Boolean)
        };
      };
      return getStructure(document.body);
    });

    console.log('\n🏗️ Page structure:');
    console.log(JSON.stringify(structure, null, 2).substring(0, 1000));

    // Try to find navigation or episode listing
    const mainContent = await page.evaluate(() => {
      const main = document.querySelector('main') || document.querySelector('#root') || document.querySelector('body');
      return main ? main.innerHTML.substring(0, 500) : 'No main content found';
    });

    console.log('\n📄 Main content HTML (first 500 chars):');
    console.log(mainContent);

    // Save exploration results
    fs.writeFileSync(
      'C:\\Users\\Keith Worrell\\Documents\\Gunn-Econ\\site-exploration.json',
      JSON.stringify({ title, links, structure, mainContent }, null, 2)
    );

    console.log('\n✓ Exploration complete. Results saved to site-exploration.json');

  } catch (error) {
    console.error('❌ Error:', error.message);
  } finally {
    await browser.close();
  }
}

exploreSite();
