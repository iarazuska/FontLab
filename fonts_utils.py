import tkinter as tk
import tkinter.font as tkfont


def get_system_fonts():
    root = tk._default_root
    if root is None:
        root = tk.Tk()
        root.withdraw()
    fonts = list(tkfont.families())
    fonts = sorted(set(fonts), key=lambda f: f.lower())
    fonts = [f for f in fonts if not f.startswith("@")]
    return fonts


SAMPLE_TEXTS = {
    "Pangrama": "El veloz murciélago hindú comía feliz cardillo y kiwi",
    "Alfabeto": "ABCDEFGHIJKLMNOPQRSTUVWXYZ abcdefghijklmnopqrstuvwxyz",
    "Números": "0123456789 !@#$%^&*()",
    "Texto corto": "Hola Mundo",
}