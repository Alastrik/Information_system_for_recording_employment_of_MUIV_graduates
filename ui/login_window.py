# Окно авторизации пользователя

import tkinter as tk
from tkinter import messagebox
from auth import AuthService
from config import AUTHOR_NAME

class LoginWindow:
    """Окно входа в систему с проверкой логина и пароля."""

    def __init__(self, root):
        self.root = root
        self.root.title("Вход в систему — Учёт трудоустройства выпускников МУИВ")
        self.root.geometry("400x250")
        self.root.resizable(False, False)

        # Центрирование окна
        self.center_window()

        # Инициализация сервиса аутентификации
        self.auth_service = AuthService()

        # Элементы интерфейса
        tk.Label(root, text="Имя пользователя:", font=("Arial", 12)).pack(pady=(20, 5))
        self.username_entry = tk.Entry(root, font=("Arial", 12), width=30)
        self.username_entry.pack()

        tk.Label(root, text="Пароль:", font=("Arial", 12)).pack(pady=(10, 5))
        self.password_entry = tk.Entry(root, font=("Arial", 12), width=30, show="*")
        self.password_entry.pack()

        tk.Button(root, text="Войти", command=self.login, font=("Arial", 12), width=15).pack(pady=20)

        # Привязка Enter к кнопке входа
        self.password_entry.bind("<Return>", lambda event: self.login())

    def center_window(self):
        """Центрирует окно на экране."""
        self.root.update_idletasks()
        x = (self.root.winfo_screenwidth() // 2) - (400 // 2)
        y = (self.root.winfo_screenheight() // 2) - (250 // 2)
        self.root.geometry(f"400x250+{x}+{y}")

    def login(self):
        """Обработчик нажатия кнопки 'Войти'."""
        username = self.username_entry.get().strip()
        password = self.password_entry.get().strip()

        if not username or not password:
            messagebox.showwarning("Ошибка", "Заполните все поля!")
            return

        user = self.auth_service.authenticate(username, password)
        if user:
            messagebox.showinfo("Успешно", f"Добро пожаловать, {username}!")
            self.root.destroy()
            self.open_main_interface(user)
        else:
            messagebox.showerror("Ошибка", "Неверное имя пользователя или пароль!")

    def open_main_interface(self, user_data):
        """Открывает главное окно в зависимости от роли пользователя."""
        # Заглушка — далее будет реализовано переключение на dashboard
        role = user_data['role']
        if role == 'admin':
            from ui.admin_panel import AdminPanel
            root = tk.Tk()
            app = AdminPanel(root, user_data)
            root.mainloop()
        elif role == 'manager':
            from ui.hr_dashboard import HRDashboard
            root = tk.Tk()
            app = HRDashboard(root, user_data)
            root.mainloop()
        elif role == 'graduate':
            from ui.graduate_profile import GraduateProfile
            root = tk.Tk()
            app = GraduateProfile(root, user_data)
            root.mainloop()
        else:
            messagebox.showerror("Ошибка", "Неизвестная роль пользователя!")