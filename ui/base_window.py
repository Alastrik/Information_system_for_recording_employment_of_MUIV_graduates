import tkinter as tk
from config import THEMES, CURRENT_THEME


class BaseWindow:
    def __init__(self, root, user_data, title="Приложение"):
        self.root = root
        self.user_data = user_data
        self.root.title(title)
        self.root.geometry("650x500")
        self.center_window()

        # Применяем тему
        self.apply_theme()

        self.frame = tk.Frame(self.root, bg=self.bg_color)
        self.frame.pack(fill="both", expand=True, padx=20, pady=20)

    def apply_theme(self):
        theme = THEMES[CURRENT_THEME]
        self.bg_color = theme["bg"]
        self.fg_color = theme["fg"]
        self.button_bg = theme["button_bg"]
        self.button_fg = theme["button_fg"]
        self.entry_bg = theme["entry_bg"]
        self.frame_bg = theme["frame_bg"]

        self.root.configure(bg=self.bg_color)

    def center_window(self):
        self.root.update_idletasks()
        x = (self.root.winfo_screenwidth() // 2) - (650 // 2)
        y = (self.root.winfo_screenheight() // 2) - (500 // 2)
        self.root.geometry(f"650x500+{x}+{y}")

    def set_theme(self, theme_name):
        """Метод для смены темы (вызывается из настроек)"""
        from config import THEMES
        global CURRENT_THEME
        CURRENT_THEME = theme_name
        self.apply_theme()
        # Обновляем фон фрейма
        self.frame.configure(bg=self.frame_bg)
        # Перерисовываем все виджеты (см. ниже)
        self.update_theme_in_widgets()

    def update_theme_in_widgets(self):
        """Переопредели в каждом окне!"""
        pass  # базовая реализация — пустая