# ui/graduate_profile.py
# Личный кабинет выпускника
import tkinter as tk
from ui.base_window import BaseWindow
from ui.employment_form import EmploymentFormWindow
from ui.help_window import HelpWindow
from ui.settings_window import SettingsWindow

class GraduateProfile(BaseWindow):
    def __init__(self, root, user_data):
        super().__init__(root, user_data, "Личный кабинет выпускника — МУИВ")
        self.create_menu()
        self.setup_ui()

    def create_menu(self):
        menubar = tk.Menu(self.root)
        file_menu = tk.Menu(menubar, tearoff=0)
        file_menu.add_command(label="Добавить трудоустройство", command=self.open_employment_form)
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
        tk.Label(
            self.main_frame,
            text="Личный кабинет выпускника",
            font=("Arial", 16, "bold"),
            bg="#f9f9f9",
            fg="#27ae60"
        ).pack(pady=15)

        # Информация о пользователе
        user_info = f"Вы вошли как: {self.user_data['username']}\nРоль: Выпускник"
        tk.Label(
            self.main_frame,
            text=user_info,
            font=("Arial", 11),
            bg="#f9f9f9",
            justify="left"
        ).pack(pady=10)

        # Инструкция
        tk.Label(
            self.main_frame,
            text="Здесь вы можете указать информацию о своём трудоустройстве",
            font=("Arial", 10, "italic"),
            bg="#f9f9f9",
            fg="#7f8c8d"
        ).pack(pady=5)

        # Кнопки
        actions = [
            ("Добавить/обновить данные о трудоустройстве", self.open_employment_form),
            ("Настройки", self.open_settings),
        ]

        for text, command in actions:
            tk.Button(
                self.main_frame,
                text=text,
                command=command,
                font=("Arial", 10),
                width=45,
                bg="#2196F3", fg="white", relief="flat"
            ).pack(pady=8)

    def open_employment_form(self):
        EmploymentFormWindow(self.root, self.user_data)
        self.create_status_label("Открыта форма трудоустройства")

    def open_settings(self):
        SettingsWindow(self.root, self.user_data)
        self.create_status_label("Открыты настройки")

    def logout(self):
        from ui.login_window import LoginWindow
        self.root.destroy()
        new_root = tk.Tk()
        LoginWindow(new_root)

        new_root.mainloop()
