# Панель администратора системы

import tkinter as tk
from tkinter import ttk, messagebox
from ui.base_window import BaseWindow
from ui.user_management import UserManagementWindow
from ui.report_export_window import ReportExportWindow
from ui.search_window import SearchWindow
from ui.help_window import HelpWindow
from ui.settings_window import SettingsWindow
from config import AUTHOR_NAME

class AdminPanel(BaseWindow):
    """Главная панель администратора с навигацией по функциям."""

    def __init__(self, root, user_data):
        super().__init__(root, user_data, title="Панель администратора — Учёт трудоустройства МУИВ")
        self.setup_ui()

    def setup_ui(self):
        # Приветствие
        welcome = tk.Label(
            self.frame,
            text=f"Добро пожаловать, администратор!\n{AUTHOR_NAME}",
            font=("Arial", 12, "bold"),
            fg="#2c3e50"
        )
        welcome.pack(pady=10)

        # Основное меню — кнопки действий
        buttons = [
            ("Управление пользователями", self.open_user_management),
            ("Экспорт отчётов", self.open_report_export),
            ("Поиск и фильтрация", self.open_search),
            ("Настройки системы", self.open_settings),
            ("Справка", self.open_help),
            ("Выход", self.logout)
        ]

        for text, command in buttons:
            btn = tk.Button(
                self.frame,
                text=text,
                command=command,
                font=("Arial", 11),
                width=30,
                height=1,
                bg="#3498db",
                fg="white",
                activebackground="#2980b9"
            )
            btn.pack(pady=8)

    def open_user_management(self):
        UserManagementWindow(self.root)

    def open_report_export(self):
        ReportExportWindow(self.root, self.user_data)

    def open_search(self):
        SearchWindow(self.root)

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