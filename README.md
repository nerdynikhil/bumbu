# Bumbu 🐙

A tiny pink octopus (or cat, bunny, duck, frog) that follows your cursor around Windows and says cute things.

- **Run:** `python bumbu.py` (Python 3 on Windows, no extra deps)
- **Build exe:** `build.bat` → `dist\Bumbu.exe`
- **Installer:** push a `v*` tag; CI builds `BumbuSetup.exe` and attaches it to the GitHub Release
- **Double-click** Bumbu to make it talk, **right-click** to switch pets, open Settings (sound, bubbles, talkativeness, size, follow, start with Windows) or quit.
- **Voices:** edit `lines.py`, then `pip install edge-tts && python make_voices.py` to render new clips into `sounds/`.
