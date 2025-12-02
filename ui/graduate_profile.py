# Личный кабинет выпускника

import tkinter as tk
from tkinter import ttk, messagebox
from ui.base_window import BaseWindow
from ui.employment_form import EmploymentFormWindow
from ui.help_window import HelpWindow
from ui.settings_window import SettingsWindow

class GraduateProfile(BaseWindow):
    """Личный кабинет выпускника."""

    def __init__(self, root, user_data):
        super().__init__(root, user_data, title="Личный кабинет выпускника — МУИВ")
        self.setup_ui()

    def setup_ui(self):
        # Заголовок
        tk.Label(
            self.frame,
            text="Личный кабинет выпускника",
            font=("Arial", 14, "bold"),
            fg="#27ae60"
        ).pack(pady=15)

        # Информация о выпускнике (заглушка — в реальном проекте: запрос к БД)
        profile_info = f"Имя пользователя: {self.user_data['username']}\n" \
                       f"Роль: Выпускник\n" \
                       f"Факультет: Информационных технологий"  # Можно загрузить из БД

        tk.Label(
            self.frame,
            text=profile_info,
            font=("Arial", 11),
            justify="left",
            anchor="w"
        ).pack(pady=10)

        # Кнопки действий
        actions = [
            ("Добавить/обновить данные о трудоустройстве", self.open_employment_form),
            ("Настройки", self.open_settings),
            ("Справка", self.open_help),
            ("Выйти", self.logout)
        ]

        for text, command in actions:
            tk.Button(
                self.frame,
                text=text,
                command=command,
                font=("Arial", 10),
                width=40
            ).pack(pady=6)

    def open_employment_form(self):
        EmploymentFormWindow(self.root, self.user_data)

    def open_settings(self):
        SettingsWindow(self.root, self.user_data)

    def open_help(self):
        HelpWindow(self.root)

    def logout(self):
        from ui.login_window import LoginWindow
        self.root.destroy()
        new_root = tk.Tk()
        LoginWindow(new_root)
        new_root.mainloop()