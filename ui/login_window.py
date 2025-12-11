# ui/login_window.py
import tkinter as tk
from tkinter import messagebox
from auth import AuthService
from config import AUTHOR_NAME

class LoginWindow:
    def __init__(self, root):
        self.root = root
        self.root.title("Вход — Учёт трудоустройства МУИВ")
        self.root.geometry("500x350")
        self.root.configure(bg="#f9f9f9")
        self.root.resizable(False, False)

        # === МЕНЮ ===
        self.create_menu()

        # === ОСНОВНОЙ КОНТЕНТ ===
        content_frame = tk.Frame(self.root, bg="#f9f9f9")
        content_frame.pack(expand=True)

        # Заголовок
        tk.Label(
            content_frame, text="Вход в систему",
            font=("Arial", 16, "bold"),
            bg="#f9f9f9", fg="#2c3e50"
        ).grid(row=0, column=0, columnspan=2, pady=(0, 20))

        # Логин
        tk.Label(content_frame, text="Имя пользователя:", bg="#f9f9f9", font=("Arial", 10)).grid(row=1, column=0, sticky="w", padx=10)
        self.username_entry = tk.Entry(content_frame, font=("Arial", 10), width=25)
        self.username_entry.grid(row=1, column=1, pady=5, padx=10)

        # Пароль
        tk.Label(content_frame, text="Пароль:", bg="#f9f9f9", font=("Arial", 10)).grid(row=2, column=0, sticky="w", padx=10)
        self.password_entry = tk.Entry(content_frame, font=("Arial", 10), width=25, show="*")
        self.password_entry.grid(row=2, column=1, pady=5, padx=10)
        self.password_entry.bind("<Return>", lambda e: self.login())

        # Кнопка входа
        login_btn = tk.Button(
            content_frame, text="Войти", command=self.login,
            bg="#2196F3", fg="white", font=("Arial", 10, "bold"),
            width=15, relief="flat", cursor="hand2"
        )
        login_btn.grid(row=3, column=0, columnspan=2, pady=20)
        # После кнопки "Войти"
        tk.Button(
            content_frame, text="Регистрация выпускника", command=self.open_registration,
            bg="#9E9E9E", fg="white", font=("Arial", 9),
            width=20, relief="flat"
        ).grid(row=4, column=0, columnspan=2, pady=5)

        self.auth_service = AuthService()

    def create_menu(self):
        menubar = tk.Menu(self.root)
        help_menu = tk.Menu(menubar, tearoff=0)
        help_menu.add_command(label="О программе", command=self.show_help)
        menubar.add_cascade(label="Справка", menu=help_menu)
        self.root.config(menu=menubar)

    def open_registration(self):
        from ui.registration_window import RegistrationWindow
        RegistrationWindow(self.root)
    def show_help(self):
        messagebox.showinfo("О программе", f"Система учёта трудоустройства выпускников МУИВ\nАвтор: {AUTHOR_NAME}")

    def login(self):
        username = self.username_entry.get().strip()
        password = self.password_entry.get().strip()
        if not username or not password:
            messagebox.showwarning("Ошибка", "Заполните все поля!")
            return

        user = self.auth_service.authenticate(username, password)
        if user:
            self.root.destroy()
            self.open_main_interface(user)  # ← Теперь метод есть!
        else:
            messagebox.showerror("Ошибка", "Неверный логин или пароль!")

    # === ДОБАВЛЕННЫЙ МЕТОД ===
    def open_main_interface(self, user_data):
        """Открывает главное окно в зависимости от роли пользователя."""
        root = tk.Tk()
        role = user_data['role']
        if role == 'admin':
            from ui.admin_panel import AdminPanel
            app = AdminPanel(root, user_data)
        elif role == 'manager':
            from ui.hr_dashboard import HRDashboard
            app = HRDashboard(root, user_data)
        elif role == 'graduate':
            from ui.graduate_profile import GraduateProfile
            app = GraduateProfile(root, user_data)
        else:
            messagebox.showerror("Ошибка", "Неизвестная роль пользователя!")
            return
        root.mainloop()