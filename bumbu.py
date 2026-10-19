import tkinter as tk

W, H = 220, 230
KEY = "#ff00fe"  # transparent color key
PINK, PINK_DARK, TEAL = "#f9b8c8", "#f4a3b8", "#6fd6d6"
CX, CY = 110, 145  # head center


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
        self.draw(0, 0, 0)

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
