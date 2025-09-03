# ScrollableFrame.py  (or paste it straight into your main script)
import tkinter as tk
from tkinter import ttk

class ScrollableFrame(ttk.Frame):
    """A Frame that contains a vertical scrollbar and a child frame where
    you can pack your real widgets. Works on Windows, macOS and Linux.
    """
    def __init__(self, container, *args, **kwargs):
        super().__init__(container, *args, **kwargs)
        self.canvas = tk.Canvas(self, borderwidth=0, highlightthickness=0)
        self.vscroll = ttk.Scrollbar(self, orient="vertical", command=self.canvas.yview)
        self.canvas.configure(yscrollcommand=self.vscroll.set)
        self.vscroll.pack(side="right", fill="y")
        self.canvas.pack(side="left", fill="both", expand=True)
        self.scrollable_frame = ttk.Frame(self.canvas)
        self.canvas.create_window((0, 0), window=self.scrollable_frame, anchor="nw")
        self.scrollable_frame.bind("<Configure>", lambda e: self.canvas.configure(scrollregion=self.canvas.bbox("all")))
        self.canvas.bind("<Enter>", self._bind)
        self.canvas.bind("<Leave>", self._unbind)


    # --------------------------------------------------------------------
    #  Mouse‑wheel helpers (kept inside the class for clarity)
    # --------------------------------------------------------------------
    def _bind(self, event):
        """Bind mouse wheel events while the mouse is over the canvas."""
        self.canvas.bind_all("<MouseWheel>", self._on_mousewheel)
        self.canvas.bind_all("<Button-4>", self._on_mousewheel)
        self.canvas.bind_all("<Button-5>", self._on_mousewheel)

    def _unbind(self, event):
        """Remove the mouse wheel bindings."""
        self.canvas.unbind_all("<MouseWheel>")
        self.canvas.unbind_all("<Button-4>")
        self.canvas.unbind_all("<Button-5>")
        self.canvas.unbind("<Up>")
        self.canvas.unbind("<Down>")



    def _on_mousewheel(self, event):
        if event.delta:
            self.canvas.yview_scroll(-1 * int(event.delta / 120), "units")
        elif event.num in (4, 5):
            self.canvas.yview_scroll(-1 * (1 if event.num == 4 else -1), "units")
    def _on_key_press(self, event):
        """Handle arrow key and PageUp/PageDown scrolling."""
        if event.keysym == 'Down':
            self.canvas.yview_scroll(1, "units")
        elif event.keysym == 'Up':
            self.canvas.yview_scroll(-1, "units")
        # Return "break" to prevent the event from propagating further
        return "break"