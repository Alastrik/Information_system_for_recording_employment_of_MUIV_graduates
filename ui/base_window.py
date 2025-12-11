# ui/base_window.py
import tkinter as tk
from PIL import Image, ImageTk
import os

class BaseWindow:
    def __init__(self, root, user_data, title="Приложение"):
        self.root = root
        self.user_data = user_data
        self.root.title(title)
        self.root.geometry("700x500")
        self.root.configure(bg="#f9f9f9")
        self.root.resizable(True, True)

        # Загружаем логотип
        self.original_logo = None
        self.logo_label = None
        self.load_original_logo()

        self.logo_label = tk.Label(self.root, bg="#f9f9f9", borderwidth=0, highlightthickness=0)
        self.logo_label.place(x=15, y=15)

        # ОСНОВНОЙ ФРЕЙМ ДЛЯ КОНТЕНТА
        self.main_frame = tk.Frame(self.root, bg="#f9f9f9")
        self.main_frame.pack(fill="both", expand=True, padx=20, pady=60)

        # Отслеживаем изменение размера
        self.root.bind("<Configure>", self.on_window_resize)
        self.update_logo_size()

    def load_original_logo(self):
        try:
            logo_path = os.path.join(os.getcwd(), "МУИВ.png")
            self.original_logo = Image.open(logo_path).convert("RGBA")
        except Exception as e:
            print(f"Не удалось загрузить логотип: {e}")

    def on_window_resize(self, event):
        if event.widget == self.root:
            self.update_logo_size()

    def update_logo_size(self):
        if self.original_logo is None or self.logo_label is None:
            return
        try:
            window_height = self.root.winfo_height()
            new_size = max(20, min(60, int(window_height * 0.08)))
            ratio = min(new_size / self.original_logo.width, new_size / self.original_logo.height)
            new_width = int(self.original_logo.width * ratio)
            new_height = int(self.original_logo.height * ratio)
            resized_img = self.original_logo.resize((new_width, new_height), Image.Resampling.LANCZOS)
            self.current_logo_img = ImageTk.PhotoImage(resized_img)
            self.logo_label.configure(image=self.current_logo_img)
            y_pos = (new_size - new_height) // 2 + 15
            self.logo_label.place(x=15, y=y_pos)
        except Exception as e:
            print(f"Ошибка масштабирования: {e}")

    # === ВАЖНО: ДОБАВЛЕН МЕТОД ОБРАТНОЙ СВЯЗИ ===
    def create_status_label(self, text, color="green"):
        """Создаёт временную метку обратной связи (исчезает через 3 сек)."""
        status = tk.Label(self.main_frame, text=text, fg=color, bg="#f9f9f9", font=("Arial", 9, "bold"))
        status.pack(pady=5)
        self.root.after(3000, status.destroy)