# main.py
import tkinter as tk
from tkinter import font
from ui.login_window import LoginWindow

if __name__ == "__main__":
    root = tk.Tk()

    # === ЕДИНЫЙ СТИЛЬ ДЛЯ ВСЕГО ПРИЛОЖЕНИЯ ===
    # Устанавливаем шрифт по умолчанию
    default_font = font.nametofont("TkDefaultFont")
    default_font.configure(family="Arial", size=10)
    text_font = font.nametofont("TkTextFont")
    text_font.configure(family="Arial", size=10)

    # Фон окна по умолчанию
    root.configure(bg="#f9f9f9")

    app = LoginWindow(root)
    root.mainloop()