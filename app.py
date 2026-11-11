"""I'm Bored - a tiny tkinter desktop app that cures boredom."""

import random
import tkinter as tk
from tkinter import font as tkfont

# ---------------------------------------------------------------------------
# Data
# ---------------------------------------------------------------------------
ACTIVITIES = [
    "Read a chapter of a book",
    "Go for a 10-minute walk",
    "Learn 5 words in a new language",
    "Do 20 pushups",
    "Call a friend",
    "Sketch something on your desk",
    "Tidy one drawer or shelf",
    "Write down three things you're grateful for",
    "Stretch for 10 minutes",
    "Cook something you've never made before",
    "Listen to an album all the way through",
    "Write a short letter to future you",
    "Learn a simple magic trick",
    "Plan an imaginary weekend trip",
    "Water your plants",
    "Meditate for 5 minutes",
    "Watch a documentary on a topic you know nothing about",
    "Delete 10 old photos from your phone",
    "Write the first paragraph of a story",
    "Drink a glass of water and rest your eyes",
]

# ---------------------------------------------------------------------------
# Colors
# ---------------------------------------------------------------------------
BG = "#050816"          # window background
CARD = "#10182d"        # card background
ACCENT = "#52c7b8"      # button color
ACCENT_HOVER = "#6ad9ca"
ACCENT_PRESSED = "#43b0a2"
TEXT = "#f4f7fb"
SOFT_TEXT = "#97a6c0"   # for the small label above the activity
BUTTON_TEXT = "#050816" # dark text on the teal button for good contrast

WINDOW_W, WINDOW_H = 500, 350


def pick_font_family(root):
    """Return the first available font from our preferred list."""
    available = set(tkfont.families(root))
    for name in ("Segoe UI", "Helvetica", "Arial"):
        if name in available:
            return name
    return "TkDefaultFont"


class BoredApp:
    def __init__(self, root):
        self.root = root
        self.current = None  # remembers the last activity shown

        # --- Window setup --------------------------------------------------
        root.title("I'm Bored")
        root.configure(bg=BG)
        root.resizable(False, False)  # fixed size, no resizing or maximizing

        # Center the window on the screen.
        x = (root.winfo_screenwidth() - WINDOW_W) // 2
        y = (root.winfo_screenheight() - WINDOW_H) // 2
        root.geometry(f"{WINDOW_W}x{WINDOW_H}+{x}+{y}")

        family = pick_font_family(root)

        # --- Layout --------------------------------------------------------
        # The root window holds one "card" Frame. place() with relx/rely=0.5
        # and anchor="center" puts the card in the exact middle of the window.
        # The card is smaller than the window, so the dark background shows
        # around it as a border.
        card = tk.Frame(root, bg=CARD)
        card.place(relx=0.5, rely=0.5, anchor="center", width=440, height=290)

        # pack_propagate(False) stops the card from shrinking to fit its
        # children, so it keeps the fixed size set above.
        card.pack_propagate(False)

        # Inside the card, widgets are stacked top to bottom with pack().

        # Small heading at the top.
        tk.Label(
            card,
            text="WHY NOT...",
            font=(family, 10, "bold"),
            fg=ACCENT,
            bg=CARD,
        ).pack(pady=(26, 0))

        # The big activity text. expand=True + fill="both" lets this label
        # take all leftover vertical space, so the text sits in the middle
        # and the button stays pinned near the bottom. wraplength makes long
        # activities wrap onto multiple lines instead of getting cut off.
        self.activity_label = tk.Label(
            card,
            text="",
            font=(family, 22, "bold"),
            fg=TEXT,
            bg=CARD,
            wraplength=380,
            justify="center",
        )
        self.activity_label.pack(expand=True, fill="both", padx=20)

        # --- Flat "button" -------------------------------------------------
        # A Label styled as a button. Unlike tk.Button, Label colors work
        # the same on every OS, and it has no 3D border.
        self.button = tk.Label(
            card,
            text="Pick Another Activity",
            font=(family, 12, "bold"),
            fg=BUTTON_TEXT,
            bg=ACCENT,
            padx=28,
            pady=12,
            cursor="hand2",
        )
        self.button.pack(pady=(0, 28))

        # Mouse events give the button its hover and press effects.
        self.button.bind("<Enter>", lambda e: self.button.config(bg=ACCENT_HOVER))
        self.button.bind("<Leave>", lambda e: self.button.config(bg=ACCENT))
        self.button.bind("<ButtonPress-1>", lambda e: self.button.config(bg=ACCENT_PRESSED))
        self.button.bind("<ButtonRelease-1>", self.on_release)

        # Keyboard shortcuts for convenience.
        root.bind("<space>", lambda e: self.pick_activity())
        root.bind("<Return>", lambda e: self.pick_activity())

        # Show the first activity on startup.
        self.pick_activity()

    def on_release(self, event):
        """Only trigger if the mouse is still over the button on release."""
        w, h = self.button.winfo_width(), self.button.winfo_height()
        if 0 <= event.x < w and 0 <= event.y < h:
            self.button.config(bg=ACCENT_HOVER)
            self.pick_activity()
        else:
            self.button.config(bg=ACCENT)

    def pick_activity(self):
        """Choose a random activity (never the same one twice in a row)."""
        choices = [a for a in ACTIVITIES if a != self.current]
        self.current = random.choice(choices)
        self.activity_label.config(text=self.current)


def main():
    root = tk.Tk()
    BoredApp(root)
    root.mainloop()


if __name__ == "__main__":
    main()