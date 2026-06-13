import tkinter as tk
from tkinter import ttk, colorchooser
from fonts_utils import get_system_fonts, SAMPLE_TEXTS

BG = "#0d0d1a"
BG2 = "#12122a"
BG3 = "#1a1a3e"
BG4 = "#222244"
FG = "#e8e8ff"
FG2 = "#8888aa"
ACCENT = "#7c4dff"
ACCENT2 = "#651fff"
GREEN = "#00e676"
ERROR = "#ff5252"
WARNING = "#ffab40"
FONT_UI = ("Segoe UI", 10)
FONT_TITLE = ("Segoe UI", 15, "bold")


class FontLabApp:
    def __init__(self, root):
        self.root = root
        self.root.title("FontLab")
        self.root.geometry("1000x650")
        self.root.configure(bg=BG)
        self.root.minsize(800, 500)

        self.fonts = get_system_fonts()
        self.filtered_fonts = self.fonts.copy()
        self.selected_font = self.fonts[0] if self.fonts else "Arial"
        self.font_size = 24
        self.bold = False
        self.italic = False
        self.text_color = "#e8e8ff"
        self.custom_text = ""

        self._build_header()
        self._build_main()
        self._build_statusbar()

        self._update_preview()

    def _build_header(self):
        header = tk.Frame(self.root, bg=BG3, pady=14)
        header.pack(fill=tk.X)
        tk.Label(header, text="🔠 FontLab", bg=BG3, fg=FG, font=FONT_TITLE).pack(side=tk.LEFT, padx=16)
        tk.Label(header, text="  —  Font Preview Tool", bg=BG3, fg=FG2, font=FONT_UI).pack(side=tk.LEFT)
        tk.Label(header, text=f"{len(self.fonts)} fuentes instaladas", bg=BG3, fg=FG2, font=("Segoe UI", 9)).pack(side=tk.RIGHT, padx=16)

    def _build_main(self):
        main = tk.Frame(self.root, bg=BG)
        main.pack(fill=tk.BOTH, expand=True, padx=16, pady=16)

        left = tk.Frame(main, bg=BG2, width=260)
        left.pack(side=tk.LEFT, fill=tk.Y, padx=(0, 12))
        left.pack_propagate(False)

        tk.Label(left, text="Fuentes", bg=BG2, fg=FG2, font=("Segoe UI", 9, "bold")).pack(anchor=tk.W, padx=12, pady=(12, 6))

        search_frame = tk.Frame(left, bg=BG2)
        search_frame.pack(fill=tk.X, padx=12)

        self.search_var = tk.StringVar()
        search_entry = tk.Entry(
            search_frame, bg=BG3, fg=FG, font=FONT_UI,
            relief=tk.FLAT, insertbackground=FG,
            textvariable=self.search_var, bd=0
        )
        search_entry.pack(fill=tk.X, ipady=6)
        self.search_var.trace_add("write", lambda *a: self._filter_fonts())

        list_frame = tk.Frame(left, bg=BG2)
        list_frame.pack(fill=tk.BOTH, expand=True, padx=12, pady=8)

        self.font_listbox = tk.Listbox(
            list_frame, bg=BG3, fg=FG, font=FONT_UI,
            relief=tk.FLAT, selectbackground=ACCENT,
            activestyle="none", bd=0
        )
        self.font_listbox.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)

        scroll = ttk.Scrollbar(list_frame, orient=tk.VERTICAL, command=self.font_listbox.yview)
        self.font_listbox.configure(yscrollcommand=scroll.set)
        scroll.pack(side=tk.RIGHT, fill=tk.Y)

        self.font_listbox.bind("<<ListboxSelect>>", self._on_font_select)
        self._populate_listbox()

        right = tk.Frame(main, bg=BG)
        right.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)

        self._build_controls(right)
        self._build_preview(right)

    def _build_controls(self, parent):
        controls = tk.Frame(parent, bg=BG2, pady=12, padx=16)
        controls.pack(fill=tk.X, pady=(0, 12))

        row1 = tk.Frame(controls, bg=BG2)
        row1.pack(fill=tk.X, pady=4)

        tk.Label(row1, text="Tamaño", bg=BG2, fg=FG2, font=FONT_UI, width=10, anchor="w").pack(side=tk.LEFT)
        self.size_var = tk.IntVar(value=self.font_size)
        size_scale = tk.Scale(
            row1, from_=8, to=72, orient=tk.HORIZONTAL,
            variable=self.size_var, bg=BG2, fg=FG,
            troughcolor=BG3, highlightthickness=0,
            command=lambda v: self._update_preview()
        )
        size_scale.pack(side=tk.LEFT, fill=tk.X, expand=True, padx=8)

        row2 = tk.Frame(controls, bg=BG2)
        row2.pack(fill=tk.X, pady=4)

        tk.Label(row2, text="Estilo", bg=BG2, fg=FG2, font=FONT_UI, width=10, anchor="w").pack(side=tk.LEFT)

        self.bold_var = tk.BooleanVar()
        tk.Checkbutton(
            row2, text="Negrita", variable=self.bold_var,
            bg=BG2, fg=FG, selectcolor=BG3,
            activebackground=BG2, font=FONT_UI,
            command=self._update_preview
        ).pack(side=tk.LEFT, padx=4)

        self.italic_var = tk.BooleanVar()
        tk.Checkbutton(
            row2, text="Cursiva", variable=self.italic_var,
            bg=BG2, fg=FG, selectcolor=BG3,
            activebackground=BG2, font=FONT_UI,
            command=self._update_preview
        ).pack(side=tk.LEFT, padx=4)

        tk.Button(
            row2, text="🎨 Color de texto", bg=BG3, fg=ACCENT,
            font=("Segoe UI", 9), relief=tk.FLAT,
            padx=10, pady=4, cursor="hand2",
            activebackground=BG4, activeforeground=ACCENT,
            command=self._pick_color
        ).pack(side=tk.RIGHT)

        row3 = tk.Frame(controls, bg=BG2)
        row3.pack(fill=tk.X, pady=(8, 4))

        tk.Label(row3, text="Texto de prueba", bg=BG2, fg=FG2, font=FONT_UI, width=10, anchor="w").pack(side=tk.LEFT)

        for name in SAMPLE_TEXTS:
            tk.Button(
                row3, text=name, bg=BG3, fg=FG2,
                font=("Segoe UI", 9), relief=tk.FLAT,
                padx=8, pady=3, cursor="hand2",
                activebackground=ACCENT, activeforeground="white",
                command=lambda n=name: self._set_sample_text(n)
            ).pack(side=tk.LEFT, padx=2)

        row4 = tk.Frame(controls, bg=BG2)
        row4.pack(fill=tk.X, pady=(8, 4))

        self.custom_entry = tk.Entry(
            row4, bg=BG3, fg=FG, font=FONT_UI,
            relief=tk.FLAT, insertbackground=FG, bd=0
        )
        self.custom_entry.pack(fill=tk.X, ipady=6)
        self.custom_entry.insert(0, SAMPLE_TEXTS["Pangrama"])
        self.custom_entry.bind("<KeyRelease>", lambda e: self._update_preview())

    def _build_preview(self, parent):
        preview_outer = tk.Frame(parent, bg=BG2)
        preview_outer.pack(fill=tk.BOTH, expand=True)

        header = tk.Frame(preview_outer, bg=BG2)
        header.pack(fill=tk.X, padx=16, pady=(12, 4))

        self.font_name_label = tk.Label(header, text="", bg=BG2, fg=ACCENT, font=("Segoe UI", 11, "bold"))
        self.font_name_label.pack(side=tk.LEFT)

        self.font_info_label = tk.Label(header, text="", bg=BG2, fg=FG2, font=("Segoe UI", 9))
        self.font_info_label.pack(side=tk.RIGHT)

        self.preview_canvas = tk.Canvas(preview_outer, bg=BG3, highlightthickness=0)
        self.preview_canvas.pack(fill=tk.BOTH, expand=True, padx=16, pady=(0, 16))

        self.preview_text_id = None

    def _build_statusbar(self):
        bar = tk.Frame(self.root, bg=BG3, pady=5)
        bar.pack(fill=tk.X, side=tk.BOTTOM)
        self.status_label = tk.Label(bar, text="Listo", bg=BG3, fg=FG2, font=("Segoe UI", 9))
        self.status_label.pack(side=tk.LEFT, padx=12)
        tk.Label(bar, text="FontLab v1.0", bg=BG3, fg=FG2, font=("Segoe UI", 9)).pack(side=tk.RIGHT, padx=12)

    def _set_status(self, text, color=None):
        self.status_label.config(text=text, fg=color or FG2)

    def _populate_listbox(self):
        self.font_listbox.delete(0, tk.END)
        for font_name in self.filtered_fonts:
            self.font_listbox.insert(tk.END, font_name)
        if self.filtered_fonts:
            self.font_listbox.selection_set(0)

    def _filter_fonts(self):
        query = self.search_var.get().lower().strip()
        if query:
            self.filtered_fonts = [f for f in self.fonts if query in f.lower()]
        else:
            self.filtered_fonts = self.fonts.copy()
        self._populate_listbox()

    def _on_font_select(self, event):
        selection = self.font_listbox.curselection()
        if selection:
            self.selected_font = self.filtered_fonts[selection[0]]
            self._update_preview()

    def _set_sample_text(self, name):
        self.custom_entry.delete(0, tk.END)
        self.custom_entry.insert(0, SAMPLE_TEXTS[name])
        self._update_preview()

    def _pick_color(self):
        color = colorchooser.askcolor(color=self.text_color)[1]
        if color:
            self.text_color = color
            self._update_preview()

    def _update_preview(self, *args):
        self.preview_canvas.delete("all")

        size = self.size_var.get()
        weight = "bold" if self.bold_var.get() else "normal"
        slant = "italic" if self.italic_var.get() else "roman"
        text = self.custom_entry.get() if self.custom_entry.get() else "Texto de ejemplo"

        try:
            font = (self.selected_font, size, weight, slant)
            self.preview_canvas.update_idletasks()
            width = self.preview_canvas.winfo_width()
            height = self.preview_canvas.winfo_height()

            self.preview_canvas.create_text(
                width // 2, height // 2,
                text=text, font=font, fill=self.text_color,
                width=width - 40, justify=tk.CENTER
            )

            self.font_name_label.config(text=self.selected_font)
            self.font_info_label.config(text=f"{size}px  •  {weight}  •  {slant}")
            self._set_status("Listo")
        except Exception as e:
            self._set_status(f"Error: {e}", ERROR)