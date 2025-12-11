# ui/admin_panel.py
import tkinter as tk
from ui.base_window import BaseWindow
from ui.user_management import UserManagementWindow
from ui.report_export_window import ReportExportWindow
from ui.search_window import SearchWindow
from ui.settings_window import SettingsWindow
from ui.help_window import HelpWindow

class AdminPanel(BaseWindow):
    def __init__(self, root, user_data):
        super().__init__(root, user_data, "Панель администратора — МУИВ")
        self.create_menu()
        self.setup_ui()

    def create_menu(self):
        menubar = tk.Menu(self.root)
        file_menu = tk.Menu(menubar, tearoff=0)
        file_menu.add_command(label="Управление пользователями", command=self.open_user_management)
        file_menu.add_command(label="Экспорт отчётов", command=self.open_report_export)
        file_menu.add_command(label="Поиск выпускников", command=self.open_search)
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
            text="Панель администратора",
            font=("Arial", 16, "bold"),
            bg="#f9f9f9",
            fg="#2c3e50"
        )
        title.pack(pady=(0, 20))

        # Кнопки
        buttons_frame = tk.Frame(self.main_frame, bg="#f9f9f9")
        buttons_frame.pack()

        actions = [
            ("Управление пользователями", self.open_user_management),
            ("Экспорт отчётов", self.open_report_export),
            ("Поиск выпускников", self.open_search),
            ("Настройки", self.open_settings),
            ("Справка", lambda: HelpWindow(self.root)),
        ]

        for i, (text, command) in enumerate(actions):
            row = i // 2
            col = i % 2
            btn = tk.Button(
                buttons_frame, text=text, command=command,
                bg="#2196F3", fg="white", font=("Arial", 10),
                width=22, height=2, relief="flat", cursor="hand2"
            )
            btn.grid(row=row, column=col, padx=10, pady=10)

    def open_user_management(self):
        UserManagementWindow(self.root, self.user_data['user_id'])
        self.create_status_label("Открыто окно управления пользователями")

    def open_report_export(self):
        from ui.report_export_window import ReportExportWindow
        ReportExportWindow(self.root, self.user_data)
        self.create_status_label("Открыто окно экспорта отчётов")

    def open_search(self):
        SearchWindow(self.root)
        self.create_status_label("Открыто окно поиска")

    def open_settings(self):
        from ui.settings_window import SettingsWindow
        SettingsWindow(self.root, self.user_data)
        self.create_status_label("Открыты настройки")

    def logout(self):
        from ui.login_window import LoginWindow
        self.root.destroy()
        new_root = tk.Tk()
        LoginWindow(new_root)

        new_root.mainloop()
