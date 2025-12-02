# Панель HR-специалиста (менеджера по трудоустройству)

import tkinter as tk
from ui.base_window import BaseWindow
from ui.employment_form import EmploymentFormWindow
from ui.search_window import SearchWindow
from ui.report_export_window import ReportExportWindow
from ui.help_window import HelpWindow
from ui.settings_window import SettingsWindow

class HRDashboard(BaseWindow):
    """Рабочая панель HR-специалиста."""

    def __init__(self, root, user_data):
        super().__init__(root, user_data, title="Панель HR-специалиста — Учёт трудоустройства МУИВ")
        self.setup_ui()

    def setup_ui(self):
        tk.Label(
            self.frame,
            text="Панель HR-специалиста",
            font=("Arial", 14, "bold"),
            fg="#8e44ad"
        ).pack(pady=15)

        # Краткая инструкция
        tk.Label(
            self.frame,
            text="Вы можете добавлять и редактировать данные о трудоустройстве выпускников,\n"
                 "формировать отчёты и осуществлять поиск по базе.",
            font=("Arial", 10),
            justify="center"
        ).pack(pady=10)

        # Кнопки
        actions = [
            ("Добавить данные о трудоустройстве", self.open_employment_form),
            ("Поиск выпускников", self.open_search),
            ("Экспорт отчётов", self.open_report_export),
            ("Настройки", self.open_settings),
            ("Справка", self.open_help),
            ("Выход", self.logout)
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

    def open_search(self):
        SearchWindow(self.root)

    def open_report_export(self):
        ReportExportWindow(self.root, self.user_data)

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