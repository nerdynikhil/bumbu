"""Pre-render every line to sounds/*.mp3. Run once after editing lines.py:
pip install edge-tts && python make_voices.py"""
import asyncio
import os

import edge_tts

from lines import LINES, PET_LINES, SPOKEN, VOICE, sound_file


async def main():
    os.makedirs("sounds", exist_ok=True)
    for line in LINES + [l for extra in PET_LINES.values() for l in extra]:
        path = os.path.join("sounds", sound_file(line))
        if not os.path.exists(path):
            await edge_tts.Communicate(SPOKEN.get(line, line), VOICE).save(path)
            print(path, line)

asyncio.run(main())
