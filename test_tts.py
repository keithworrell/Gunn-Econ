#!/usr/bin/env python3
"""
Test script to debug TTS issues with different SSML complexity levels.
"""

import asyncio
import edge_tts

VOICE = 'es-MX-DaliaNeural'

async def test_plain_text():
    """Test 1: Plain text without SSML"""
    print("\n=== Test 1: Plain text ===")
    text = "Hola. Este es un texto de prueba en español."
    try:
        communicate = edge_tts.Communicate(text, VOICE)
        await communicate.save("test1_plain.mp3")
        print("✓ Plain text SUCCESS")
        return True
    except Exception as e:
        print(f"✗ Plain text FAILED: {e}")
        return False


async def test_simple_ssml():
    """Test 2: Simple SSML with breaks"""
    print("\n=== Test 2: Simple SSML ===")
    ssml = '''<speak version="1.0" xmlns="http://www.w3.org/2001/10/synthesis" xml:lang="es-MX">
Hola.<break time="500ms"/> Este es un texto de prueba.<break time="500ms"/> Con pausas.
</speak>'''
    try:
        communicate = edge_tts.Communicate(ssml, VOICE)
        await communicate.save("test2_simple_ssml.mp3")
        print("✓ Simple SSML SUCCESS")
        return True
    except Exception as e:
        print(f"✗ Simple SSML FAILED: {e}")
        return False


async def test_complex_ssml():
    """Test 3: Complex SSML with emphasis and prosody"""
    print("\n=== Test 3: Complex SSML ===")
    ssml = '''<speak version="1.0" xmlns="http://www.w3.org/2001/10/synthesis" xml:lang="es-MX">
<emphasis level="moderate">Título importante</emphasis><break time="500ms"/>
<prosody rate="95%">Texto con velocidad ajustada</prosody><break time="500ms"/>
Texto normal con pausa.<break time="400ms"/>
</speak>'''
    try:
        communicate = edge_tts.Communicate(ssml, VOICE)
        await communicate.save("test3_complex_ssml.mp3")
        print("✓ Complex SSML SUCCESS")
        return True
    except Exception as e:
        print(f"✗ Complex SSML FAILED: {e}")
        return False


async def test_actual_file():
    """Test 4: Load and test actual SSML file (first 2000 chars)"""
    print("\n=== Test 4: Actual SSML file (truncated) ===")
    try:
        with open("economics-spanish/tts-prepared/01-markets-video-spanish.ssml", "r", encoding="utf-8") as f:
            content = f.read()

        # Find the closing </speak> tag
        closing_tag = "</speak>"

        # Take first 2000 chars of content between <speak> and </speak>
        start = content.find(">") + 1  # After opening <speak ...>
        truncated = content[:2000]

        # Make sure it ends properly
        if closing_tag not in truncated:
            # Find last complete sentence
            last_period = truncated.rfind(".")
            if last_period > 0:
                truncated = content[:start] + content[start:last_period+1] + "\n" + closing_tag
            else:
                truncated = content[:start] + content[start:2000] + "\n" + closing_tag

        print(f"Testing with {len(truncated)} characters...")
        communicate = edge_tts.Communicate(truncated, VOICE)
        await communicate.save("test4_actual_truncated.mp3")
        print("✓ Actual SSML (truncated) SUCCESS")
        return True
    except Exception as e:
        print(f"✗ Actual SSML FAILED: {e}")
        print(f"First 500 chars of content:\n{truncated[:500]}")
        return False


async def main():
    """Run all tests"""
    print("=" * 70)
    print("TTS Debugging Tests")
    print("=" * 70)

    tests = [
        test_plain_text,
        test_simple_ssml,
        test_complex_ssml,
        test_actual_file,
    ]

    results = []
    for test in tests:
        result = await test()
        results.append(result)
        if not result:
            print("\n⚠ Stopping at first failure to debug")
            break

    print("\n" + "=" * 70)
    print("Test Summary")
    print("=" * 70)
    passed = sum(results)
    total = len(results)
    print(f"Passed: {passed}/{total}")

    if passed < total:
        print("\n💡 Recommendation:")
        if not results[0]:
            print("   Basic TTS is failing. Check internet connection and edge-tts installation.")
        elif not results[1]:
            print("   SSML breaks are not supported. Try plain text without SSML.")
        elif not results[2]:
            print("   Complex SSML tags not supported. Simplify the SSML.")
        else:
            print("   The actual SSML file has issues. Check for:")
            print("   - Invalid SSML syntax")
            print("   - Unsupported tags")
            print("   - Special characters that need escaping")
            print("   - File might be too long (try shorter segments)")


if __name__ == "__main__":
    asyncio.run(main())
