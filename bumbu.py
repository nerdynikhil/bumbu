import math
import random
import tkinter as tk

W, H = 220, 230
KEY = "#ff00fe"  # transparent color key
PINK, PINK_DARK, TEAL = "#f9b8c8", "#f4a3b8", "#6fd6d6"
CX, CY = 110, 145  # head center
LINES = [
    "hiii :3", "you're doing great!", "boop!", "i like your cursor",
    "drink some water!", "wanna be friends?", "you're my favorite human",
    "take a tiny break?", "*wiggles*", "snack time?", "i believe in you!",
    "don't forget to smile", "uwu",
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
        self.pet = tk.StringVar(value="Octopus")
        self.menu = tk.Menu(self.root, tearoff=0)
        for name in PETS:
            self.menu.add_radiobutton(label=name, variable=self.pet, command=self.say)
        self.menu.add_separator()
        self.menu.add_command(label="Quit", command=self.root.destroy)
        self.root.bind("<Button-3>", lambda e: self.menu.tk_popup(e.x_root, e.y_root))
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
        text = c.create_text(CX, 38, text=random.choice(LINES + PETS[self.pet.get()][1]), width=180,
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
        self.look = (3 * dx / d, 3 * dy / d)
        self.draw(bob, *self.look)
        self.root.after(16, self.tick)

    def draw(self, bob, lx, ly):
        self.canvas.delete("pet")
        PETS[self.pet.get()][0](self, CY + bob, lx, ly)
        self.canvas.tag_raise("bubble")

    def oval(self, x1, y1, x2, y2, fill, outline="", width=1):
        self.canvas.create_oval(x1, y1, x2, y2, fill=fill, outline=outline, width=width, tags="pet")

    def face(self, ey, gap, my=None, cheeks="#f78fa7"):
        """Eyes at height ey (pupils follow the cursor), optional smile at my, cheeks."""
        for ex in (CX - gap, CX + gap):
            self.oval(ex - 9, ey - 11, ex + 9, ey + 11, "black")
            hx, hy = ex + 3 + self.look[0], ey - 4 + self.look[1]
            self.oval(hx - 3, hy - 3, hx + 3, hy + 3, "white")
        if my is not None:
            self.canvas.create_arc(CX - 9, my, CX + 9, my + 14, start=200, extent=140,
                                   style="arc", width=3, tags="pet")
        cy = (my if my is not None else ey + 12) + 7
        for bx in (CX - gap - 14, CX + gap + 14):
            self.oval(bx - 7, cy - 3, bx + 7, cy + 3, cheeks)

    def octopus(self, y, lx, ly):
        def lobe(x, ly_, rx=24, ry=15):
            self.oval(x - rx, ly_ - ry + 5, x + rx, ly_ + ry + 5, TEAL, TEAL)
            self.oval(x - rx, ly_ - ry, x + rx, ly_ + ry, PINK, PINK_DARK)
        for x, dy in ((38, 28), (182, 28), (58, 18), (162, 18)):
            lobe(x, y + dy)
        self.oval(CX - 52, y - 58, CX + 52, y + 42, PINK, PINK_DARK, 2)
        for x, dy in ((48, 45), (82, 52), (118, 54), (152, 50), (180, 42)):
            lobe(x, y + dy)
        self.face(y - 8, 22, y + 2)

    def cat(self, y, lx, ly):
        fur, edge, pink = "#ffc48a", "#f0a868", "#ffb3c1"
        c = self.canvas
        c.create_line(CX + 35, y + 68, CX + 78, y + 62, CX + 82, y + 22, smooth=True,
                      width=14, fill=edge, capstyle="round", tags="pet")
        self.oval(CX - 45, y + 10, CX + 45, y + 78, fur, edge, 2)
        for s_ in (-1, 1):
            c.create_polygon(CX + s_ * 48, y - 22, CX + s_ * 40, y - 66, CX + s_ * 10, y - 42,
                             fill=fur, outline=edge, width=2, tags="pet")
            c.create_polygon(CX + s_ * 40, y - 28, CX + s_ * 37, y - 54, CX + s_ * 20, y - 40,
                             fill=pink, tags="pet")
        self.oval(CX - 52, y - 48, CX + 52, y + 36, fur, edge, 2)
        for s_ in (-1, 1):
            self.oval(CX + s_ * 18 - 12, y + 66, CX + s_ * 18 + 12, y + 82, fur, edge, 2)
            for dy in (6, 13):
                c.create_line(CX + s_ * 22, y + dy, CX + s_ * 56, y + dy - 4 + dy // 3,
                              fill=edge, width=2, tags="pet")
        self.face(y - 8, 22, y + 4)

    def bunny(self, y, lx, ly):
        fur, edge, pink = "#fffaf5", "#e8d6cc", "#ffc9d6"
        for s_ in (-1, 1):
            x1, x2 = sorted((CX + s_ * 10, CX + s_ * 34))
            self.oval(x1, y - 102, x2, y - 20, fur, edge, 2)
            self.oval(x1 + 6, y - 92, x2 - 6, y - 30, pink)
        self.oval(CX - 42, y + 12, CX + 42, y + 74, fur, edge, 2)
        for s_ in (-1, 1):
            self.oval(CX + s_ * 26 - 16, y + 62, CX + s_ * 26 + 16, y + 80, fur, edge, 2)
        self.oval(CX - 50, y - 46, CX + 50, y + 36, fur, edge, 2)
        self.face(y - 6, 20, y + 4)

    def duck(self, y, lx, ly):
        body, edge, beak = "#ffe27a", "#f2c94c", "#ff9f43"
        for s_ in (-1, 1):
            self.oval(CX + s_ * 22 - 16, y + 62, CX + s_ * 22 + 16, y + 80, beak)
        self.oval(CX - 60, y - 8, CX + 60, y + 72, body, edge, 2)
        self.oval(CX + 18, y + 18, CX + 62, y + 52, edge)
        self.oval(CX - 42, y - 58, CX + 42, y + 22, body, edge, 2)
        self.canvas.create_line(CX - 2, y - 56, CX - 8, y - 70, CX + 6, y - 64, smooth=True,
                                width=3, fill=edge, tags="pet")
        self.face(y - 24, 17)
        self.oval(CX - 15, y - 12, CX + 15, y + 4, beak, "#f08a2c")

    def frog(self, y, lx, ly):
        skin, edge = "#9be38b", "#6cc35e"
        for s_ in (-1, 1):
            self.oval(CX + s_ * 42 - 20, y + 50, CX + s_ * 42 + 20, y + 72, skin, edge, 2)
        self.oval(CX - 58, y - 14, CX + 58, y + 64, skin, edge, 2)
        for s_ in (-1, 1):
            self.oval(CX + s_ * 28 - 22, y - 52, CX + s_ * 28 + 22, y - 8, skin, edge, 2)
        self.oval(CX - 50, y - 12, CX + 50, y + 20, skin)  # hide bump outlines into the head
        self.face(y - 30, 28, y + 8)

    def run(self):
        self.root.mainloop()


# name -> (draw method, extra lines)
PETS = {
    "Octopus": (Pet.octopus, ["8 arms, all for hugs", "blub blub", "ink-credible work!"]),
    "Cat": (Pet.cat, ["meow :3", "purr purr", "pet me pls", "i knocked something over"]),
    "Bunny": (Pet.bunny, ["hop hop!", "got any carrots?", "*nose wiggle*", "some-bunny loves you"]),
    "Duck": (Pet.duck, ["quack!", "quack quack <3", "you're un-duck-niably great", "waddle waddle"]),
    "Frog": (Pet.frog, ["ribbit!", "toad-ally proud of you", "hop to it!", "it's a good day to be a frog"]),
}

if __name__ == "__main__":
    Pet().run()
