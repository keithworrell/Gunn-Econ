#!/usr/bin/env python3
"""
Setup Verification Script
Checks if all dependencies are properly installed
"""

import sys

def check_module(module_name, import_name=None):
    """Check if a Python module is installed"""
    if import_name is None:
        import_name = module_name.replace('-', '_')

    try:
        __import__(import_name)
        print(f"  ✓ {module_name}")
        return True
    except ImportError:
        print(f"  ✗ {module_name} - NOT INSTALLED")
        return False

def check_chrome_driver():
    """Check if Chrome/Chromium can be detected"""
    try:
        from selenium import webdriver
        from selenium.webdriver.chrome.options import Options
        from webdriver_manager.chrome import ChromeDriverManager

        print("  ⟳ Checking Chrome WebDriver...")
        options = Options()
        options.add_argument("--headless")
        options.add_argument("--no-sandbox")

        # This will download driver if needed
        ChromeDriverManager().install()
        print("  ✓ Chrome WebDriver available")
        return True
    except Exception as e:
        print(f"  ✗ Chrome WebDriver issue: {e}")
        return False

def main():
    """Main verification function"""
    print("="*60)
    print("Setup Verification for Economics Transcript Pipeline")
    print("="*60)

    all_good = True

    # Check Python version
    print("\n1. Python Version:")
    version = sys.version_info
    if version.major >= 3 and version.minor >= 8:
        print(f"  ✓ Python {version.major}.{version.minor}.{version.micro}")
    else:
        print(f"  ✗ Python {version.major}.{version.minor}.{version.micro} - Need 3.8+")
        all_good = False

    # Check required modules
    print("\n2. Required Python Packages:")

    modules = [
        ('selenium', 'selenium'),
        ('webdriver-manager', 'webdriver_manager'),
        ('beautifulsoup4', 'bs4'),
        ('requests', 'requests'),
        ('PyPDF2', 'PyPDF2'),
        ('pypdf', 'pypdf'),
        ('reportlab', 'reportlab'),
        ('pdfplumber', 'pdfplumber'),
        ('deep-translator', 'deep_translator'),
        ('edge-tts', 'edge_tts'),
        ('tqdm', 'tqdm'),
    ]

    for module_name, import_name in modules:
        if not check_module(module_name, import_name):
            all_good = False

    # Check Chrome WebDriver
    print("\n3. Web Scraping Setup:")
    if not check_chrome_driver():
        all_good = False

    # Check directory structure
    print("\n4. Project Structure:")
    import os
    dirs = [
        'economics-spanish',
        'economics-spanish/original-transcripts',
        'economics-spanish/spanish-transcripts',
        'economics-spanish/audio-files',
    ]

    for dir_path in dirs:
        if os.path.exists(dir_path):
            print(f"  ✓ {dir_path}/")
        else:
            print(f"  ✗ {dir_path}/ - MISSING")
            all_good = False

    # Final result
    print("\n" + "="*60)
    if all_good:
        print("✓ All checks passed! You're ready to run the pipeline.")
        print("\nNext steps:")
        print("  python run_pipeline.py --all")
    else:
        print("✗ Some checks failed. Please install missing dependencies:")
        print("\n  pip install -r requirements.txt")
        print("\nThen run this script again to verify.")
        sys.exit(1)
    print("="*60)

if __name__ == "__main__":
    main()
