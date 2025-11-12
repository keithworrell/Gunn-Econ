#!/bin/bash
# Download Economics USA transcripts using curl
# Based on URL pattern: https://www.learner.org/wp-content/uploads/2019/02/economics-usa-{topic}-audio-transcript.pdf

OUTPUT_DIR="economics-spanish/original-transcripts"
mkdir -p "$OUTPUT_DIR"

# Known topics from Economics USA series
TOPICS=(
    "supply-demand"
    "markets"
    "competition"
    "market-structures"
    "monopoly"
    "oligopoly"
    "labor-markets"
    "income-distribution"
    "poverty"
    "externalities"
    "public-goods"
    "government-regulation"
    "antitrust"
    "resources-scarcity"
    "economic-growth"
    "productivity"
    "unemployment"
    "inflation"
    "business-cycles"
    "monetary-policy"
    "fiscal-policy"
    "federal-deficits"
    "international-trade"
    "exchange-rates"
    "developing-economies"
    "globalization"
)

# Try different date folders
DATES=("2019/01" "2019/02" "2019/03" "2019/04" "2019/05" "2019/06")

echo "Economics USA Transcript Downloader (curl)"
echo "=========================================="

count=0
downloaded=0

for topic in "${TOPICS[@]}"; do
    count=$((count + 1))
    echo ""
    echo "[$count/${#TOPICS[@]}] Trying: $topic"

    found=false
    for date in "${DATES[@]}"; do
        # Try different filename patterns
        for pattern in "economics-usa-${topic}-audio-transcript.pdf" "economics-usa-${topic}-transcript.pdf"; do
            url="https://www.learner.org/wp-content/uploads/${date}/${pattern}"
            output="${OUTPUT_DIR}/video-$(printf '%02d' $count)-${topic}.pdf"

            # Try to download
            http_code=$(curl -s -o "$output" -w "%{http_code}" -L \
                -A "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36" \
                "$url")

            # Check if successful
            if [ "$http_code" = "200" ] && [ -f "$output" ] && [ $(stat -f%z "$output" 2>/dev/null || stat -c%s "$output" 2>/dev/null) -gt 1000 ]; then
                size=$(stat -f%z "$output" 2>/dev/null || stat -c%s "$output" 2>/dev/null)
                echo "  ✓ Downloaded: $(basename $output) (${size} bytes)"
                downloaded=$((downloaded + 1))
                found=true
                break 2
            else
                rm -f "$output"
            fi
        done
    done

    if [ "$found" = false ]; then
        echo "  ✗ Not found: $topic"
    fi

    sleep 1  # Be respectful to server
done

echo ""
echo "=========================================="
echo "Download Complete!"
echo "=========================================="
echo "Successfully downloaded: $downloaded/${#TOPICS[@]} transcripts"
echo "Files saved to: $OUTPUT_DIR"

if [ $downloaded -lt 20 ]; then
    echo ""
    echo "⚠ Found fewer than expected (Economics USA has ~28 episodes)"
    echo "Some transcripts may use different topic slugs or dates."
fi
