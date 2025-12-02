# Окно настроек приложения

import tkinter as tk
from tkinter import ttk, messagebox
import os

class SettingsWindow:
    """Окно настроек с не менее чем 5 пунктами управления."""

    def __init__(self, parent, user_data):
        self.window = tk.Toplevel(parent)
        self.window.title("Настройки")
        self.window.geometry("500x350")
        self.window.resizable(False, False)
        self.center_window(parent)

        tk.Label(self.window, text="Настройки системы", font=("Arial", 14, "bold")).pack(pady=15)

        # Фрейм для элементов
        frame = tk.Frame(self.window)
        frame.pack(padx=20, pady=10, fill="both", expand=True)

        # 1. Язык интерфейса
        tk.Label(frame, text="Язык интерфейса:", font=("Arial", 10)).grid(row=0, column=0, sticky="w", pady=5)
        self.lang_var = tk.StringVar(value="Русский")
        lang_combo = ttk.Combobox(frame, textvariable=self.lang_var, values=["Русский"], state="disabled", width=20)
        lang_combo.grid(row=0, column=1, sticky="w", pady=5)

        # 2. Каталог для отчётов
        tk.Label(frame, text="Папка для отчётов:", font=("Arial", 10)).grid(row=1, column=0, sticky="w", pady=5)
        self.report_dir = tk.StringVar(value=os.path.join(os.path.expanduser("~"), "MUIV_Employment_Reports"))
        dir_entry = tk.Entry(frame, textvariable=self.report_dir, width=30)
        dir_entry.grid(row=1, column=1, sticky="w", pady=5)
        tk.Button(frame, text="Обзор...", command=self.select_report_dir, font=("Arial", 9)).grid(row=1, column=2, padx=5)

        # 3. Автосохранение
        self.autosave_var = tk.BooleanVar(value=True)
        autosave_check = tk.Checkbutton(frame, text="Включить автосохранение", variable=self.autosave_var, font=("Arial", 10))
        autosave_check.grid(row=2, column=0, columnspan=2, sticky="w", pady=5)

        # 4. Уведомления
        self.notify_var = tk.BooleanVar(value=True)
        notify_check = tk.Checkbutton(frame, text="Показывать уведомления", variable=self.notify_var, font=("Arial", 10))
        notify_check.grid(row=3, column=0, columnspan=2, sticky="w", pady=5)

        # 5. Проверка обновлений
        self.update_var = tk.BooleanVar(value=False)
        update_check = tk.Checkbutton(frame, text="Проверять обновления при запуске", variable=self.update_var, font=("Arial", 10))
        update_check.grid(row=4, column=0, columnspan=2, sticky="w", pady=5)

        # Кнопки
        button_frame = tk.Frame(self.window)
        button_frame.pack(pady=20)
        tk.Button(button_frame, text="Сохранить", command=self.save_settings, font=("Arial", 11), width=12).pack(side="left", padx=10)
        tk.Button(button_frame, text="Отмена", command=self.window.destroy, font=("Arial", 11), width=12).pack(side="left", padx=10)

    def select_report_dir(self):
        """Открывает диалог выбора папки."""
        from tkinter import filedialog
        folder = filedialog.askdirectory(initialdir=self.report_dir.get())
        if folder:
            self.report_dir.set(folder)

    def save_settings(self):
        """Сохраняет настройки (заглушка)."""
        # Здесь можно в будущем сохранять в файл config.ini
        messagebox.showinfo("Успех", "Настройки сохранены!")
        self.window.destroy()

    def center_window(self, parent):
        parent_x = parent.winfo_rootx()
        parent_y = parent.winfo_rooty()
        x = parent_x + 50
        y = parent_y + 50
        self.window.geometry(f"500x350+{x}+{y}")