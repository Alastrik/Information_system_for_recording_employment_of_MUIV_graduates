# ui/hr_dashboard.py
import tkinter as tk
from ui.base_window import BaseWindow
from ui.employment_form import EmploymentFormWindow
from ui.search_window import SearchWindow
from ui.report_export_window import ReportExportWindow
from ui.help_window import HelpWindow
from ui.settings_window import SettingsWindow

class HRDashboard(BaseWindow):
    def __init__(self, root, user_data):
        super().__init__(root, user_data, "Панель HR-специалиста — МУИВ")
        self.create_menu()
        self.setup_ui()

    def create_menu(self):
        menubar = tk.Menu(self.root)
        file_menu = tk.Menu(menubar, tearoff=0)
        file_menu.add_command(label="Добавить трудоустройство", command=self.open_employment_form)
        file_menu.add_command(label="Поиск выпускников", command=self.open_search)
        file_menu.add_command(label="Экспорт отчётов", command=self.open_report_export)
        file_menu.add_separator()
        file_menu.add_command(label="Выход", command=self.logout)
        menubar.add_cascade(label="Файл", menu=file_menu)

        help_menu = tk.Menu(menubar, tearoff=0)
        help_menu.add_command(label="Справка", command=lambda: HelpWindow(self.root))
        help_menu.add_command(label="О программе", command=self.show_about)
        menubar.add_cascade(label="Справка", menu=help_menu)

        self.root.config(menu=menubar)

    def show_about(self):
        from config import AUTHOR_NAME
        tk.messagebox.showinfo("О программе", f"Автор: {AUTHOR_NAME}\n© 2025")

    def setup_ui(self):
        # Заголовок
        title = tk.Label(
            self.main_frame,
            text="Панель HR-специалиста",
            font=("Arial", 16, "bold"),
            bg="#f9f9f9",
            fg="#8e44ad"
        )
        title.pack(pady=(0, 20))

        # Описание
        desc = tk.Label(
            self.main_frame,
            text="Добавляйте и редактируйте данные о трудоустройстве выпускников",
            font=("Arial", 10), bg="#f9f9f9", fg="#2c3e50"
        )
        desc.pack(pady=(0, 15))

        # Кнопки
        actions = [
            ("Добавить данные о трудоустройстве", self.open_employment_form),
            ("Поиск выпускников", self.open_search),
            ("Экспорт отчётов", self.open_report_export),
            ("Настройки", self.open_settings),
        ]

        for text, command in actions:
            btn = tk.Button(
                self.main_frame,
                text=text, command=command,
                bg="#2196F3", fg="white", font=("Arial", 10),
                width=40, height=1, relief="flat", cursor="hand2"
            )
            btn.pack(pady=6)

    def open_employment_form(self):
        EmploymentFormWindow(self.root, self.user_data)
        self.create_status_label("Открыта форма трудоустройства")

    def open_search(self):
        SearchWindow(self.root)
        self.create_status_label("Открыто окно поиска")

    def open_report_export(self):
        ReportExportWindow(self.root, self.user_data)
        self.create_status_label("Открыто окно экспорта")

    def open_settings(self):
        SettingsWindow(self.root, self.user_data)
        self.create_status_label("Открыты настройки")

    def logout(self):
        from ui.login_window import LoginWindow
        self.root.destroy()
        new_root = tk.Tk()
        LoginWindow(new_root)

        new_root.mainloop()
