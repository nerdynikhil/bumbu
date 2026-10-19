import json
import math
import os
import random
import sys
import tkinter as tk

from PIL import Image, ImageOps, ImageTk

from lines import LINES, PET_LINES, sound_file

HERE = getattr(sys, "_MEIPASS", os.path.dirname(os.path.abspath(__file__)))


def play(line):
    path = os.path.join(HERE, "sounds", sound_file(line))
    if sys.platform != "win32" or not os.path.exists(path):
        return
    import ctypes
    mci = ctypes.windll.winmm.mciSendStringW
    mci("close bumbu", None, 0, None)
    mci(f'open "{path}" type mpegvideo alias bumbu', None, 0, None)
    mci("play bumbu", None, 0, None)


W, TOP = 200, 58  # window width; room above the pet for the speech bubble
SIZES = {"Tiny": 28, "Small": 44, "Medium": 64, "Big": 100}  # pet height in px
TALK = {"Chatty": (4, 8), "Normal": (8, 16), "Quiet": (25, 50), "Silent": None}
PETS = [p for p in PET_LINES if os.path.isdir(os.path.join(HERE, "sprites", p.lower()))]
SETTINGS = os.path.join(os.environ.get("APPDATA", os.path.expanduser("~")), "Bumbu", "settings.json")
DEFAULTS = {"pet": "Octopus", "sound": True, "bubbles": True, "talk": "Normal",
            "size": "Tiny", "follow": True, "startup": False}
KEY = "#ff00fe"  # transparent color key
TEAL = "#6fd6d6"


def load_frames(pet, height):
    """sprites/<pet>/0.png is idle, 1-4 run right. Returns (idle, run_right, run_left) PhotoImages."""
    frames = []
    for i in range(5):
        im = Image.open(os.path.join(HERE, "sprites", pet.lower(), f"{i}.png")).convert("RGBA")
        im = im.resize((round(im.width * height / im.height), height), Image.LANCZOS)
        # the window can only make one exact color transparent, so make alpha all-or-nothing
        im.putalpha(im.getchannel("A").point(lambda a: 255 if a > 128 else 0))
        frames.append(im)
    photo = ImageTk.PhotoImage
    return (photo(frames[0]), [photo(f) for f in frames[1:]],
            [photo(ImageOps.mirror(f)) for f in frames[1:]])


class Pet:
    def __init__(self):
        self.root = tk.Tk()
        self.root.overrideredirect(True)
        self.root.attributes("-topmost", True)
        try:
            self.root.attributes("-transparentcolor", KEY)  # Windows
        except tk.TclError:
            pass
        try:
            with open(SETTINGS) as f:
                saved = {**DEFAULTS, **json.load(f)}
        except (OSError, ValueError):
            saved = dict(DEFAULTS)
        if saved["pet"] not in PETS:
            saved["pet"] = PETS[0]
        if saved["size"] not in SIZES:
            saved["size"] = DEFAULTS["size"]
        self.vars = {k: (tk.BooleanVar if isinstance(v, bool) else tk.StringVar)(value=v)
                     for k, v in saved.items()}
        for v in self.vars.values():
            v.trace_add("write", lambda *_: self.save())
        self.canvas = tk.Canvas(self.root, width=W, bg=KEY, highlightthickness=0)
        self.canvas.pack()
        self.sprite = self.canvas.create_image(W / 2, 0, anchor="s")
        self.x, self.y, self.t = 300.0, 300.0, 0
        self.running, self.facing, self.frame = False, 1, 0
        self.reload()

        self.menu = tk.Menu(self.root, tearoff=0)
        for name in PETS:
            self.menu.add_radiobutton(label=name, variable=self.vars["pet"],
                                      command=lambda: (self.reload(), self.say()))
        self.menu.add_separator()
        settings = tk.Menu(self.menu, tearoff=0)
        settings.add_checkbutton(label="Sound", variable=self.vars["sound"])
        settings.add_checkbutton(label="Speech bubbles", variable=self.vars["bubbles"])
        settings.add_checkbutton(label="Follow cursor", variable=self.vars["follow"])
        if getattr(sys, "frozen", False) and sys.platform == "win32":
            settings.add_checkbutton(label="Start with Windows", variable=self.vars["startup"],
                                     command=self.set_startup)
        for title, options, key, cmd in (("Talk", TALK, "talk", None), ("Size", SIZES, "size", self.reload)):
            sub = tk.Menu(settings, tearoff=0)
            for name in options:
                sub.add_radiobutton(label=name, variable=self.vars[key], command=cmd)
            settings.add_cascade(label=title, menu=sub)
        self.menu.add_cascade(label="Settings", menu=settings)
        self.menu.add_command(label="Quit", command=self.root.destroy)
        self.root.bind("<Button-3>", lambda e: self.menu.tk_popup(e.x_root, e.y_root))
        self.root.bind("<Double-Button-1>", lambda e: self.say())
        self.tick()
        self.root.after(1500, self.chatter)

    def get(self, key):
        return self.vars[key].get()

    def save(self):
        os.makedirs(os.path.dirname(SETTINGS), exist_ok=True)
        with open(SETTINGS, "w") as f:
            json.dump({k: v.get() for k, v in self.vars.items()}, f)

    def set_startup(self):
        import winreg
        with winreg.OpenKey(winreg.HKEY_CURRENT_USER, r"Software\Microsoft\Windows\CurrentVersion\Run",
                            0, winreg.KEY_SET_VALUE) as key:
            if self.get("startup"):
                winreg.SetValueEx(key, "Bumbu", 0, winreg.REG_SZ, f'"{sys.executable}"')
            else:
                try:
                    winreg.DeleteValue(key, "Bumbu")
                except FileNotFoundError:
                    pass

    def reload(self):
        """Load the current pet at the current size and fit the window to it."""
        self.h = SIZES[self.get("size")]
        self.idle, self.run_r, self.run_l = load_frames(self.get("pet"), self.h)
        self.pw = self.idle.width()
        self.wh = TOP + self.h + 4
        self.canvas.config(height=self.wh)
        self.root.geometry(f"{W}x{self.wh}")

    def chatter(self):
        talk = TALK[self.get("talk")]
        if talk:
            self.say()
        self.root.after(random.randint(*talk) * 1000 if talk else 5000, self.chatter)

    def say(self):
        c = self.canvas
        c.delete("bubble")
        line = random.choice(LINES + PET_LINES[self.get("pet")])
        if self.get("sound"):
            play(line)
        if not self.get("bubbles"):
            return
        text = c.create_text(W / 2, 22, text=line, width=180,
                             font=("Segoe UI", 10, "bold"), fill="#5a3a4a", tags="bubble")
        x1, y1, x2, y2 = c.bbox(text)
        x1, y1, x2, y2 = x1 - 10, y1 - 8, x2 + 10, y2 + 8
        r = 10
        pts = [x1 + r, y1, x2 - r, y1, x2, y1, x2, y1 + r, x2, y2 - r, x2, y2,
               W / 2 + 8, y2, W / 2, y2 + 9, W / 2 - 5, y2, x1, y2, x1, y2 - r, x1, y1 + r, x1, y1]
        bg = c.create_polygon(pts, smooth=True, fill="white", outline=TEAL, width=2, tags="bubble")
        c.tag_lower(bg, text)
        if getattr(self, "hide_job", None):
            self.root.after_cancel(self.hide_job)
        self.hide_job = self.root.after(3500, lambda: c.delete("bubble"))

    def tick(self):
        self.t += 1
        px, py = self.root.winfo_pointerxy()
        # window position that puts the pet just right of the cursor
        tx = px + 8 + self.pw / 2 - W / 2
        ty = py + self.h * 0.2 - (TOP + self.h / 2)
        dx, dy = tx - self.x, ty - self.y
        dist = math.hypot(dx, dy)
        # start running once the cursor is properly away, stop when we've arrived;
        # small moves (like hovering the pet to right-click it) don't wake it up
        if not self.get("follow"):
            self.running = False
        elif not self.running and dist > self.h + 20:
            self.running = True
        elif self.running and dist < 3:
            self.running = False

        if self.running:
            step = min(dist, 2.5 + self.h / 14 + dist * 0.03)  # run, and hurry if far behind
            self.x += dx / dist * step
            self.y += dy / dist * step
            if abs(dx) > 2:
                self.facing = 1 if dx > 0 else -1
            if self.t % 6 == 0:
                self.frame = (self.frame + 1) % 4
            img, bob = (self.run_r if self.facing > 0 else self.run_l)[self.frame], 0
        else:
            img, bob = self.idle, round(1.5 * math.sin(self.t / 12))
        self.root.geometry(f"+{int(self.x)}+{int(self.y)}")
        self.canvas.itemconfig(self.sprite, image=img)
        self.canvas.coords(self.sprite, W / 2, self.wh - 2 + bob)
        self.root.after(16, self.tick)

    def run(self):
        self.root.mainloop()


if __name__ == "__main__":
    Pet().run()
