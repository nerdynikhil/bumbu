import math
import random
import tkinter as tk

W, H = 220, 230
KEY = "#ff00fe"  # transparent color key
PINK, PINK_DARK, TEAL = "#f9b8c8", "#f4a3b8", "#6fd6d6"
CX, CY = 110, 145  # head center
LINES = [
    "hiii :3", "you're doing great!", "boop!", "i like your cursor",
    "8 arms, all for hugs", "drink some water!", "blub blub", "wanna be friends?",
    "you're my favorite human", "take a tiny break?", "*wiggles*", "snack time?",
    "i believe in you!", "ink-credible work!", "don't forget to smile", "uwu",
]


class Pet:
    def __init__(self):
        self.root = tk.Tk()
        self.root.overrideredirect(True)
        self.root.attributes("-topmost", True)
        try:
            self.root.attributes("-transparentcolor", KEY)  # Windows
        except tk.TclError:
            pass
        self.canvas = tk.Canvas(self.root, width=W, height=H, bg=KEY, highlightthickness=0)
        self.canvas.pack()
        self.root.geometry(f"{W}x{H}+300+300")
        self.root.bind("<Button-3>", lambda e: self.root.destroy())
        self.x, self.y, self.t = 300.0, 300.0, 0
        self.root.bind("<Double-Button-1>", lambda e: self.say())
        self.tick()
        self.root.after(1500, self.chatter)

    def chatter(self):
        self.say()
        self.root.after(random.randint(8000, 16000), self.chatter)

    def say(self):
        c = self.canvas
        c.delete("bubble")
        text = c.create_text(CX, 38, text=random.choice(LINES), width=180,
                             font=("Segoe UI", 11, "bold"), fill="#5a3a4a", tags="bubble")
        x1, y1, x2, y2 = c.bbox(text)
        x1, y1, x2, y2 = x1 - 10, y1 - 8, x2 + 10, y2 + 8
        r = 10
        pts = [x1 + r, y1, x2 - r, y1, x2, y1, x2, y1 + r, x2, y2 - r, x2, y2,
               CX + 10, y2, CX, y2 + 12, CX - 6, y2, x1, y2, x1, y2 - r, x1, y1 + r, x1, y1]
        bg = c.create_polygon(pts, smooth=True, fill="white", outline=TEAL, width=2, tags="bubble")
        c.tag_lower(bg, text)
        if getattr(self, "hide_job", None):
            self.root.after_cancel(self.hide_job)
        self.hide_job = self.root.after(3500, lambda: c.delete("bubble"))

    def tick(self):
        px, py = self.root.winfo_pointerxy()
        # sit just right of the cursor so we never cover it
        tx, ty = px + 20, py - 90
        self.x += (tx - self.x) * 0.08
        self.y += (ty - self.y) * 0.08
        self.root.geometry(f"+{int(self.x)}+{int(self.y)}")
        # eyes look toward cursor
        dx, dy = px - (self.x + CX), py - (self.y + CY)
        d = max(1.0, (dx * dx + dy * dy) ** 0.5)
        self.t += 1
        bob = 3 * math.sin(self.t / 10)
        self.draw(bob, 3 * dx / d, 3 * dy / d)
        self.root.after(16, self.tick)

    def lobe(self, x, y, rx=24, ry=15):
        c = self.canvas
        c.create_oval(x - rx, y - ry + 5, x + rx, y + ry + 5, fill=TEAL, outline=TEAL, tags="pet")
        c.create_oval(x - rx, y - ry, x + rx, y + ry, fill=PINK, outline=PINK_DARK, tags="pet")

    def draw(self, bob, lx, ly):
        c = self.canvas
        c.delete("pet")
        y = CY + bob
        # back tentacles
        for x, dy in ((38, 28), (182, 28), (58, 18), (162, 18)):
            self.lobe(x, y + dy)
        # head
        c.create_oval(CX - 52, y - 58, CX + 52, y + 42, fill=PINK, outline=PINK_DARK, width=2, tags="pet")
        # front tentacles
        for x, dy in ((48, 45), (82, 52), (118, 54), (152, 50), (180, 42)):
            self.lobe(x, y + dy)
        # eyes (pupils shift toward cursor by lx, ly)
        for ex in (CX - 22, CX + 22):
            ey = y - 8
            c.create_oval(ex - 9, ey - 11, ex + 9, ey + 11, fill="black", tags="pet")
            hx, hy = ex + 3 + lx, ey - 4 + ly
            c.create_oval(hx - 3, hy - 3, hx + 3, hy + 3, fill="white", outline="white", tags="pet")
        # smile
        c.create_arc(CX - 9, y + 2, CX + 9, y + 16, start=200, extent=140, style="arc", width=3, tags="pet")
        # cheeks
        for bx in (CX - 36, CX + 36):
            c.create_oval(bx - 7, y + 4, bx + 7, y + 10, fill="#f78fa7", outline="", tags="pet")

    def run(self):
        self.root.mainloop()


if __name__ == "__main__":
    Pet().run()
