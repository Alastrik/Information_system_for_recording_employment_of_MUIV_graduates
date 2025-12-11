# ui/registration_window.py
import tkinter as tk
from tkinter import ttk, messagebox
from database import DatabaseConnection
import re

class RegistrationWindow:
    def __init__(self, parent):
        self.window = tk.Toplevel(parent)
        self.window.title("Регистрация выпускника")
        self.window.geometry("520x620")
        self.window.configure(bg="#f9f9f9")
        self.center_window(parent)
        self.db = DatabaseConnection()
        self.db.connect()
        self.setup_ui()
        self.load_faculties()

    def center_window(self, parent):
        x = parent.winfo_rootx() + 100
        y = parent.winfo_rooty() + 30
        self.window.geometry(f"520x620+{x}+{y}")

    def load_faculties(self):
        try:
            faculties = self.db.execute_query("SELECT id, name FROM faculty ORDER BY name", fetch=True)
            self.faculty_options = {name: id for id, name in faculties}
            self.faculty_combo['values'] = list(self.faculty_options.keys())
            if faculties:
                self.faculty_combo.set(faculties[0][1])
        except Exception as e:
            messagebox.showerror("Ошибка", f"Не удалось загрузить факультеты:\n{e}")

    def setup_ui(self):
        # Заголовок
        tk.Label(
            self.window, text="Регистрация выпускника",
            font=("Arial", 14, "bold"), bg="#f9f9f9", fg="#2c3e50"
        ).pack(pady=15)

        # Основной фрейм для формы
        form_frame = tk.Frame(self.window, bg="#f9f9f9")
        form_frame.pack(padx=30, pady=10, fill="both", expand=True)

        # Вспомогательная функция для создания поля
        def create_labeled_entry(parent, label_text, row, is_password=False, is_spinbox=False, spin_from=1990, spin_to=2025):
            tk.Label(parent, text=label_text, bg="#f9f9f9", font=("Arial", 10), anchor="w").grid(
                row=row, column=0, sticky="w", pady=5, padx=5
            )
            if is_spinbox:
                var = tk.Spinbox(parent, from_=spin_from, to=spin_to, width=40, font=("Arial", 10))
                var.grid(row=row, column=1, pady=5, padx=10, sticky="ew")
            else:
                var = tk.Entry(parent, width=40, font=("Arial", 10), show="*" if is_password else "")
                var.grid(row=row, column=1, pady=5, padx=10, sticky="ew")
            return var

        # Поля ввода
        self.login_entry = create_labeled_entry(form_frame, "Логин (уникальный):", 0)
        self.pass1_entry = create_labeled_entry(form_frame, "Пароль:", 1, is_password=True)
        self.pass2_entry = create_labeled_entry(form_frame, "Подтвердите пароль:", 2, is_password=True)
        self.email_entry = create_labeled_entry(form_frame, "Email (уникальный):", 3)

        # Год выпуска
        self.year_spin = create_labeled_entry(form_frame, "Год выпуска:", 4, is_spinbox=True, spin_from=1990, spin_to=2025)

        # ФИО (отдельный блок)
        fio_frame = tk.LabelFrame(form_frame, text="ФИО", font=("Arial", 10, "bold"), bg="#f9f9f9", padx=10, pady=10)
        fio_frame.grid(row=5, column=0, columnspan=2, pady=10, sticky="ew")

        tk.Label(fio_frame, text="Фамилия:", bg="#f9f9f9", font=("Arial", 10)).grid(row=0, column=0, sticky="w", pady=3)
        self.last_name = tk.Entry(fio_frame, width=25, font=("Arial", 10))
        self.last_name.grid(row=0, column=1, padx=10, pady=3, sticky="w")

        tk.Label(fio_frame, text="Имя:", bg="#f9f9f9", font=("Arial", 10)).grid(row=1, column=0, sticky="w", pady=3)
        self.first_name = tk.Entry(fio_frame, width=25, font=("Arial", 10))
        self.first_name.grid(row=1, column=1, padx=10, pady=3, sticky="w")

        tk.Label(fio_frame, text="Отчество (необязательно):", bg="#f9f9f9", font=("Arial", 10)).grid(row=2, column=0, sticky="w", pady=3)
        self.patronymic = tk.Entry(fio_frame, width=25, font=("Arial", 10))
        self.patronymic.grid(row=2, column=1, padx=10, pady=3, sticky="w")

        # Факультет
        tk.Label(form_frame, text="Факультет:", bg="#f9f9f9", font=("Arial", 10), anchor="w").grid(
            row=6, column=0, sticky="w", pady=5, padx=5
        )
        self.faculty_combo = ttk.Combobox(form_frame, state="readonly", width=38, font=("Arial", 10))
        self.faculty_combo.grid(row=6, column=1, pady=5, padx=10, sticky="w")

        # Кнопки
        btn_frame = tk.Frame(self.window, bg="#f9f9f9")
        btn_frame.pack(pady=20)

        tk.Button(
            btn_frame, text="Зарегистрироваться", command=self.register,
            bg="#4CAF50", fg="white", font=("Arial", 10, "bold"), width=18
        ).pack(side="left", padx=5)

        tk.Button(
            btn_frame, text="Отмена", command=self.window.destroy,
            bg="#9E9E9E", fg="white", font=("Arial", 10), width=10
        ).pack(side="left", padx=5)

        # Настройка растяжения колонок
        form_frame.columnconfigure(1, weight=1)

    def is_valid_email(self, email):
        return re.match(r"^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$", email)

    def register(self):
        # Валидация
        login = self.login_entry.get().strip()
        pass1 = self.pass1_entry.get()
        pass2 = self.pass2_entry.get()
        if not login or len(login) < 3:
            messagebox.showwarning("Ошибка", "Логин должен быть не короче 3 символов")
            return
        if pass1 != pass2:
            messagebox.showwarning("Ошибка", "Пароли не совпадают!")
            return
        if len(pass1) < 6:
            messagebox.showwarning("Ошибка", "Пароль должен быть не короче 6 символов")
            return

        last = self.last_name.get().strip()
        first = self.first_name.get().strip()
        if not last or not first:
            messagebox.showwarning("Ошибка", "Укажите фамилию и имя!")
            return

        email = self.email_entry.get().strip()
        if email and not self.is_valid_email(email):
            messagebox.showwarning("Ошибка", "Некорректный email!")
            return

        # Проверка уникальности
        if not self.is_login_unique(login):
            messagebox.showerror("Ошибка", "Логин уже занят!")
            return
        if email and not self.is_email_unique(email):
            messagebox.showerror("Ошибка", "Email уже используется!")
            return

        # Сохранение
        try:
            full_name = f"{last} {first}" + (f" {self.patronymic.get().strip()}" if self.patronymic.get().strip() else "")
            graduation_year = int(self.year_spin.get())
            faculty_id = self.faculty_options[self.faculty_combo.get()]

            self.db.execute_query(
                "INSERT INTO auth_user (username, password, is_active) VALUES (%s, %s, TRUE)",
                (login, pass1)
            )
            user_id = self.db.execute_query(
                "SELECT id FROM auth_user WHERE username = %s", (login,), fetch=True
            )[0][0]

            self.db.execute_query(
                "INSERT INTO user_profile (user_id, role, faculty_id) VALUES (%s, 'graduate', %s)",
                (user_id, faculty_id)
            )
            profile_id = self.db.execute_query(
                "SELECT id FROM user_profile WHERE user_id = %s", (user_id,), fetch=True
            )[0][0]

            self.db.execute_query(
                "INSERT INTO graduate (user_profile_id, full_name, graduation_year, email) VALUES (%s, %s, %s, %s)",
                (profile_id, full_name, graduation_year, email if email else None)
            )

            messagebox.showinfo("Успех", "Регистрация завершена!\nТеперь вы можете войти в систему.")
            self.window.destroy()

        except Exception as e:
            messagebox.showerror("Ошибка", f"Не удалось зарегистрироваться:\n{e}")
        finally:
            self.db.disconnect()

    def is_login_unique(self, login):
        res = self.db.execute_query("SELECT 1 FROM auth_user WHERE username = %s", (login,), fetch=True)
        return len(res) == 0

    def is_email_unique(self, email):
        res = self.db.execute_query("SELECT 1 FROM graduate WHERE email = %s", (email,), fetch=True)
        return len(res) == 0