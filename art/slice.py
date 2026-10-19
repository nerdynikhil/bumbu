"""Cut a raw 5-frame AI sprite sheet (art/<pet>-raw.png) into sprites/<pet>/0..4.png.
Frame 0 = idle, 1-4 = run cycle facing right. Usage: python art/slice.py octopus [green|magenta]"""
import os
import sys

from PIL import Image

pet, bg = sys.argv[1], (sys.argv[2] if len(sys.argv) > 2 else "green")
here = os.path.dirname(os.path.abspath(__file__))
im = Image.open(os.path.join(here, f"{pet}-raw.png")).convert("RGBA")
w, h = im.size
px = im.load()
for y in range(h):
    for x in range(w):
        r, g, b, _ = px[x, y]
        score = g - max(r, b) if bg == "green" else min(r, b) - g
        a = 255 if score < 30 else 0 if score > 80 else int(255 * (80 - score) / 50)
        if bg == "green" and a and g > max(r, b):  # remove green spill on edges
            g = max(r, b)
        px[x, y] = (r, g, b, a)

# frames = runs of columns that contain character pixels
alpha = im.getchannel("A")
cols = [sum(1 for y in range(h) if alpha.getpixel((x, y)) > 128) > 2 for x in range(w)]
runs, start = [], None
for x, on in enumerate(cols + [False]):
    if on and start is None:
        start = x
    elif not on and start is not None:
        if x - start > 30:
            runs.append((start, x))
        start = None
if len(runs) != 5:
    sys.exit(f"expected 5 frames, found {len(runs)}: {runs}")

frames = [im.crop((x1, 0, x2, h)).crop(im.crop((x1, 0, x2, h)).getbbox()) for x1, x2 in runs]
fw, fh = max(f.width for f in frames), max(f.height for f in frames)
out = os.path.join(here, "..", "sprites", pet)
os.makedirs(out, exist_ok=True)
for i, f in enumerate(frames):
    canvas = Image.new("RGBA", (fw, fh))
    canvas.paste(f, ((fw - f.width) // 2, fh - f.height))
    canvas.resize((round(fw * 128 / fh), 128), Image.LANCZOS).save(os.path.join(out, f"{i}.png"))
print(pet, "ok", [f.size for f in frames])
