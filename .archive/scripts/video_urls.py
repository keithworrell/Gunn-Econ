#!/usr/bin/env python3
"""
Economics USA Video List - Discovered from Web Search
Creates a list of all known video URLs for transcript download
"""

# Based on web search results and typical Annenberg Learner course structure
# Economics U$A has 28 episodes total

KNOWN_VIDEOS = [
    {
        'number': 1,
        'title': 'Resources and Scarcity',
        'url': 'https://www.learner.org/series/economics-ua-21st-century-edition/resources-and-scarcity/',
        'category': 'Macroeconomics'
    },
    {
        'number': 2,
        'title': 'Supply and Demand',
        'url': 'https://www.learner.org/series/economics-ua-21st-century-edition/supply-and-demand/',
        'category': 'Microeconomics'
    },
    {
        'number': 3,
        'title': 'Economic Efficiency',
        'url': 'https://www.learner.org/series/economics-ua-21st-century-edition/economic-efficiency/',
        'category': 'Microeconomics'
    },
    {
        'number': 4,
        'title': 'Reducing Poverty',
        'url': 'https://www.learner.org/series/economics-ua-21st-century-edition/reducing-poverty/',
        'category': 'Microeconomics'
    },
    {
        'number': 5,
        'title': 'Federal Deficits',
        'url': 'https://www.learner.org/series/economics-ua-21st-century-edition/federal-deficits/',
        'category': 'Macroeconomics'
    },
    {
        'number': 6,
        'title': 'International Trade',
        'url': 'https://www.learner.org/series/economics-ua-21st-century-edition/international-trade/',
        'category': 'International'
    },
]

# Full list structure (to be completed by visiting the series page manually or via browser)
# Common Economics USA topics include:
LIKELY_TOPICS = [
    'resources-and-scarcity',
    'supply-and-demand',
    'economic-efficiency',
    'reducing-poverty',
    'federal-deficits',
    'international-trade',
    'market-structures',
    'competition',
    'labor-markets',
    'monetary-policy',
    'fiscal-policy',
    'unemployment',
    'inflation',
    'economic-growth',
    'productivity',
    'business-cycles',
    'exchange-rates',
    'comparative-advantage',
    'income-distribution',
    'public-goods',
    'externalities',
    'antitrust',
    'regulation',
    'developing-economies',
    'transitional-economies',
    'globalization',
]

def generate_url_list():
    """Generate potential URLs for all videos"""
    base_url = "https://www.learner.org/series/economics-ua-21st-century-edition/"

    urls = []
    for topic in LIKELY_TOPICS:
        urls.append(f"{base_url}{topic}/")

    return urls

def print_known_videos():
    """Print all known video information"""
    print("Known Economics U$A Videos:")
    print("=" * 80)
    for video in KNOWN_VIDEOS:
        print(f"{video['number']:2d}. {video['title']:<40} ({video['category']})")
        print(f"    {video['url']}")
    print("=" * 80)
    print(f"Total confirmed: {len(KNOWN_VIDEOS)} videos")
    print(f"\nTo download, visit each URL and look for 'Transcript' or 'PDF' link")

if __name__ == "__main__":
    print_known_videos()
    print("\n\nPotential URLs to check:")
    print("=" * 80)
    for url in generate_url_list():
        print(url)
