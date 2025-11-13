#!/usr/bin/env python3
"""
Test if edge-tts actually processes SSML tags or ignores them.
"""

import asyncio
import edge_tts

VOICE = 'es-MX-DaliaNeural'

async def test_ssml_vs_plain():
    """Compare SSML with breaks vs plain text"""

    # Test 1: Plain text
    plain = "Hola. Esto es una prueba. Con tres oraciones."

    # Test 2: Text with SSML breaks (should have 2-second pauses)
    ssml_breaks = '''<speak version="1.0" xmlns="http://www.w3.org/2001/10/synthesis" xml:lang="es-MX">
Hola.<break time="2000ms"/> Esto es una prueba.<break time="2000ms"/> Con tres oraciones.
</speak>'''

    # Test 3: Text with emphasis
    ssml_emphasis = '''<speak version="1.0" xmlns="http://www.w3.org/2001/10/synthesis" xml:lang="es-MX">
<emphasis level="strong">Hola</emphasis>. Esto es una <emphasis level="moderate">prueba</emphasis>. Con tres oraciones.
</speak>'''

    # Test 4: Text with prosody (slower rate)
    ssml_prosody = '''<speak version="1.0" xmlns="http://www.w3.org/2001/10/synthesis" xml:lang="es-MX">
<prosody rate="50%">Hola. Esto es una prueba. Con tres oraciones.</prosody>
</speak>'''

    print("Generating test files...")
    print("=" * 70)

    tests = [
        ("test_plain.mp3", plain, "Plain text (no SSML)"),
        ("test_breaks.mp3", ssml_breaks, "SSML with 2-second breaks"),
        ("test_emphasis.mp3", ssml_emphasis, "SSML with emphasis"),
        ("test_prosody.mp3", ssml_prosody, "SSML with 50% slower rate"),
    ]

    for filename, text, description in tests:
        try:
            communicate = edge_tts.Communicate(text, VOICE)
            await communicate.save(filename)
            print(f"✓ {filename:20s} - {description}")
        except Exception as e:
            print(f"✗ {filename:20s} - FAILED: {e}")

    print("=" * 70)
    print("\nTest files created. Listen and compare:")
    print("1. test_plain.mp3       - Baseline (no SSML)")
    print("2. test_breaks.mp3      - Should have LONG 2-second pauses")
    print("3. test_emphasis.mp3    - Should emphasize 'Hola' and 'prueba'")
    print("4. test_prosody.mp3     - Should be NOTICEABLY slower (half speed)")
    print("\nIf they all sound the same, edge-tts does NOT support SSML.")
    print("If 2-4 sound different from 1, edge-tts DOES support SSML.")

if __name__ == "__main__":
    asyncio.run(test_ssml_vs_plain())
