# ui/employment_form.py
import tkinter as tk
from tkinter import ttk, messagebox
from database import DatabaseConnection
import re
from datetime import datetime

class EmploymentFormWindow:
    def __init__(self, parent, user_data):
        self.window = tk.Toplevel(parent)
        self.window.title("Трудоустройство выпускника")
        self.window.geometry("600x650")
        self.window.configure(bg="#f9f9f9")
        self.center_window(parent)

        self.user_data = user_data
        self.db = DatabaseConnection()
        self.db.connect()
        self.employment_id = None  # для редактирования

        self.setup_ui()
        self.load_dropdown_data()

        # Если HR — загружаем список выпускников
        if self.user_data['role'] == 'manager':
            self.load_graduates()

    def center_window(self, parent):
        x = parent.winfo_rootx() + 50
        y = parent.winfo_rooty() + 50
        self.window.geometry(f"600x650+{x}+{y}")

    def load_dropdown_data(self):
        try:
            positions = self.db.execute_query("SELECT id, title FROM position ORDER BY title", fetch=True)
            self.position_options = {title: id for id, title in positions}
            self.position_combo['values'] = list(self.position_options.keys())

            statuses = self.db.execute_query("SELECT id, status_name FROM employment_status ORDER BY id", fetch=True)
            self.status_options = {name: id for id, name in statuses}
            self.status_combo['values'] = list(self.status_options.keys())
            self.status_combo.bind("<<ComboboxSelected>>", self.on_status_change)

        except Exception as e:
            messagebox.showerror("Ошибка", f"Не удалось загрузить справочники:\n{e}")

    def load_graduates(self):
        """Загружает список выпускников (только для HR)."""
        try:
            graduates = self.db.execute_query("""
                SELECT g.id, g.full_name, f.name as faculty
                FROM graduate g
                LEFT JOIN user_profile up ON g.user_profile_id = up.id
                LEFT JOIN faculty f ON up.faculty_id = f.id
                WHERE g.full_name IS NOT NULL AND TRIM(g.full_name) != ''
                ORDER BY g.full_name
            """, fetch=True)

            self.graduate_options = {}
            if not graduates:
                self.graduate_combo['values'] = ["Нет выпускников"]
                self.graduate_combo.set("Нет выпускников")
                return

            for row in graduates:
                full_name = row[1].strip() if row[1] and row[1].strip() else "Без имени"
                faculty = row[2].strip() if row[2] and row[2].strip() else "—"
                display_name = f"{full_name} ({faculty})"
                self.graduate_options[display_name] = row[0]

            self.graduate_combo['values'] = list(self.graduate_options.keys())
            first_key = list(self.graduate_options.keys())[0]
            self.graduate_combo.set(first_key)
            self.on_graduate_select()

        except Exception as e:
            messagebox.showerror("Ошибка", f"Не удалось загрузить выпускников:\n{e}")

    def setup_ui(self):
        if self.user_data['role'] == 'graduate':
            self.setup_graduate_ui()
        else:
            self.setup_hr_ui()

    def setup_graduate_ui(self):
        #Блок: ФИО, email, год выпуска (только для выпускника) 
        fio_frame = tk.LabelFrame(self.window, text="Ваши данные", font=("Arial", 10, "bold"), bg="#f9f9f9", padx=10, pady=10)
        fio_frame.pack(padx=20, pady=10, fill="x")

        tk.Label(fio_frame, text="Фамилия:", bg="#f9f9f9", font=("Arial", 10)).grid(row=0, column=0, sticky="w", pady=3)
        self.last_name_entry = tk.Entry(fio_frame, font=("Arial", 10), width=25)
        self.last_name_entry.grid(row=0, column=1, padx=10, pady=3)

        tk.Label(fio_frame, text="Имя:", bg="#f9f9f9", font=("Arial", 10)).grid(row=1, column=0, sticky="w", pady=3)
        self.first_name_entry = tk.Entry(fio_frame, font=("Arial", 10), width=25)
        self.first_name_entry.grid(row=1, column=1, padx=10, pady=3)

        tk.Label(fio_frame, text="Отчество:", bg="#f9f9f9", font=("Arial", 10)).grid(row=2, column=0, sticky="w", pady=3)
        self.patronymic_entry = tk.Entry(fio_frame, font=("Arial", 10), width=25)
        self.patronymic_entry.grid(row=2, column=1, padx=10, pady=3)

        tk.Label(fio_frame, text="Email:", bg="#f9f9f9", font=("Arial", 10)).grid(row=3, column=0, sticky="w", pady=3)
        self.email_entry = tk.Entry(fio_frame, font=("Arial", 10), width=25)
        self.email_entry.grid(row=3, column=1, padx=10, pady=3)

        tk.Label(fio_frame, text="Год выпуска:", bg="#f9f9f9", font=("Arial", 10)).grid(row=4, column=0, sticky="w", pady=3)
        current_year = datetime.now().year
        self.graduation_year_entry = tk.Spinbox(fio_frame, from_=1990, to=current_year, width=24, font=("Arial", 10))
        self.graduation_year_entry.delete(0, "end")
        self.graduation_year_entry.insert(0, current_year)
        self.graduation_year_entry.grid(row=4, column=1, padx=10, pady=3)

        self.setup_common_ui()

    def setup_hr_ui(self):
        #Блок: Выбор выпускника (только для HR)
        grad_frame = tk.LabelFrame(self.window, text="Выберите выпускника", font=("Arial", 10, "bold"), bg="#f9f9f9", padx=10, pady=10)
        grad_frame.pack(padx=20, pady=10, fill="x")

        tk.Label(grad_frame, text="Выпускник:", bg="#f9f9f9", font=("Arial", 10)).grid(row=0, column=0, sticky="w", pady=3)
        self.graduate_combo = ttk.Combobox(grad_frame, state="readonly", width=45, font=("Arial", 10))
        self.graduate_combo.grid(row=0, column=1, padx=10, pady=3)
        self.graduate_combo.bind("<<ComboboxSelected>>", lambda e: self.on_graduate_select())

        self.setup_common_ui()

    def setup_common_ui(self):
        #Блок: Место работы
        work_frame = tk.LabelFrame(self.window, text="Место работы", font=("Arial", 10, "bold"), bg="#f9f9f9", padx=10, pady=10)
        work_frame.pack(padx=20, pady=10, fill="x")

        tk.Label(work_frame, text="Организация:", bg="#f9f9f9", font=("Arial", 10)).grid(row=0, column=0, sticky="w", pady=3)
        self.company_entry = tk.Entry(work_frame, font=("Arial", 10), width=40)
        self.company_entry.grid(row=0, column=1, padx=10, pady=3, columnspan=2)

        tk.Label(work_frame, text="Должность:", bg="#f9f9f9", font=("Arial", 10)).grid(row=1, column=0, sticky="w", pady=3)
        self.position_combo = ttk.Combobox(work_frame, state="readonly", width=37, font=("Arial", 10))
        self.position_combo.grid(row=1, column=1, padx=10, pady=3, columnspan=2)

        tk.Label(work_frame, text="Статус:", bg="#f9f9f9", font=("Arial", 10)).grid(row=2, column=0, sticky="w", pady=3)
        self.status_combo = ttk.Combobox(work_frame, state="readonly", width=37, font=("Arial", 10))
        self.status_combo.grid(row=2, column=1, padx=10, pady=3, columnspan=2)

        #Блок: Дополнительно
        extra_frame = tk.LabelFrame(self.window, text="Дополнительно", font=("Arial", 10, "bold"), bg="#f9f9f9", padx=10, pady=10)
        extra_frame.pack(padx=20, pady=10, fill="x")

        tk.Label(extra_frame, text="Дата начала (ГГГГ-ММ-ДД):", bg="#f9f9f9", font=("Arial", 10)).grid(row=0, column=0, sticky="w", pady=3)
        self.date_entry = tk.Entry(extra_frame, font=("Arial", 10), width=15)
        self.date_entry.grid(row=0, column=1, pady=3, sticky="w")
        self.date_entry.insert(0, "2025-01-01")

        tk.Label(extra_frame, text="Зарплата (руб.):", bg="#f9f9f9", font=("Arial", 10)).grid(row=1, column=0, sticky="w", pady=3)
        self.salary_entry = tk.Entry(extra_frame, font=("Arial", 10), width=15)
        self.salary_entry.grid(row=1, column=1, pady=3, sticky="w")

        self.is_current_var = tk.BooleanVar(value=True)
        self.is_current_check = tk.Checkbutton(
            extra_frame, text="Текущее место работы",
            variable=self.is_current_var,
            font=("Arial", 10), bg="#f9f9f9",
            command=self.on_current_work_toggle
        )
        self.is_current_check.grid(row=2, column=0, columnspan=2, sticky="w", pady=5)

        # === Кнопки ===
        btn_frame = tk.Frame(self.window, bg="#f9f9f9")
        btn_frame.pack(pady=20)
        tk.Button(btn_frame, text="Сохранить", command=self.save_employment,
                  bg="#4CAF50", fg="white", font=("Arial", 10, "bold"), width=12).pack(side="left", padx=10)
        tk.Button(btn_frame, text="Отмена", command=self.window.destroy,
                  bg="#9E9E9E", fg="white", font=("Arial", 10), width=12).pack(side="left", padx=10)

    def on_graduate_select(self):
        """Загружает существующее трудоустройство для выбранного выпускника (HR)."""
        if self.user_data['role'] != 'manager':
            return
        graduate_name = self.graduate_combo.get()
        if not graduate_name:
            return
        graduate_id = self.graduate_options[graduate_name]
        emp = self.db.execute_query(
            "SELECT id, company_id, position_id, status_id, start_date, salary, is_current FROM employment WHERE graduate_id = %s",
            (graduate_id,), fetch=True
        )
        if emp:
            self.employment_id = emp[0][0]
            if emp[0][1]:
                company = self.db.execute_query("SELECT name FROM company WHERE id = %s", (emp[0][1],), fetch=True)
                self.company_entry.delete(0, tk.END)
                self.company_entry.insert(0, company[0][0] if company else "")
            if emp[0][2]:
                pos = self.db.execute_query("SELECT title FROM position WHERE id = %s", (emp[0][2],), fetch=True)
                self.position_combo.set(pos[0][0] if pos else "")
            if emp[0][3]:
                status = self.db.execute_query("SELECT status_name FROM employment_status WHERE id = %s", (emp[0][3],), fetch=True)
                self.status_combo.set(status[0][0] if status else "")
            self.date_entry.delete(0, tk.END)
            self.date_entry.insert(0, emp[0][4].strftime("%Y-%m-%d") if emp[0][4] else "2025-01-01")
            self.salary_entry.delete(0, tk.END)
            self.salary_entry.insert(0, str(emp[0][5]) if emp[0][5] else "")
            self.is_current_var.set(emp[0][6])

    def on_status_change(self, event=None):
        status = self.status_combo.get()
        if status in ["Уволен", "Не работает", "Ищет работу"]:
            self.company_entry.config(state="disabled")
            self.is_current_var.set(False)
            self.is_current_check.config(state="disabled")
        else:
            self.company_entry.config(state="normal")
            self.is_current_check.config(state="normal")

    def on_current_work_toggle(self):
        pass

    def is_valid_email(self, email):
        return re.match(r"^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$", email)

    def save_employment(self):
        try:
            if self.user_data['role'] == 'graduate':
                last_name = self.last_name_entry.get().strip()
                first_name = self.first_name_entry.get().strip()
                if not last_name or not first_name:
                    messagebox.showwarning("Ошибка", "Укажите фамилию и имя!")
                    return
                patronymic = self.patronymic_entry.get().strip()
                full_name = f"{last_name} {first_name}" + (f" {patronymic}" if patronymic else "")
                email = self.email_entry.get().strip()
                if email and not self.is_valid_email(email):
                    messagebox.showwarning("Ошибка", "Некорректный email!")
                    return
                try:
                    graduation_year = int(self.graduation_year_entry.get())
                except:
                    messagebox.showwarning("Ошибка", "Год выпуска должен быть числом!")
                    return

                user_id = self.user_data['user_id']
                profile = self.db.execute_query(
                    "SELECT id FROM user_profile WHERE user_id = %s", (user_id,), fetch=True
                )[0][0]
                grad_check = self.db.execute_query(
                    "SELECT id FROM graduate WHERE user_profile_id = %s", (profile,), fetch=True
                )
                if grad_check:
                    graduate_id = grad_check[0][0]
                    self.db.execute_query("""
                        UPDATE graduate SET full_name=%s, graduation_year=%s, email=%s WHERE id=%s
                    """, (full_name, graduation_year, email if email else None, graduate_id))
                else:
                    self.db.execute_query("""
                        INSERT INTO graduate (user_profile_id, full_name, graduation_year, email)
                        VALUES (%s, %s, %s, %s)
                    """, (profile, full_name, graduation_year, email if email else None))
                    graduate_id = self.db.execute_query(
                        "SELECT id FROM graduate WHERE user_profile_id = %s", (profile,), fetch=True
                    )[0][0]

            else:
                graduate_name = self.graduate_combo.get()
                if not graduate_name:
                    messagebox.showwarning("Ошибка", "Выберите выпускника!")
                    return
                graduate_id = self.graduate_options[graduate_name]

            company_name = self.company_entry.get().strip()
            status = self.status_combo.get()
            if status not in ["Уволен", "Не работает", "Ищет работу"] and not company_name:
                messagebox.showwarning("Ошибка", "Укажите организацию!")
                return

            position = self.position_combo.get()
            if not position:
                messagebox.showwarning("Ошибка", "Выберите должность!")
                return

            company_id = None
            if company_name:
                comp_check = self.db.execute_query("SELECT id FROM company WHERE name = %s", (company_name,), fetch=True)
                if comp_check:
                    company_id = comp_check[0][0]
                else:
                    industry_id = self.get_default_industry_id()
                    self.db.execute_query(
                        "INSERT INTO company (name, industry_id) VALUES (%s, %s)",
                        (company_name, industry_id)
                    )
                    new_id = self.db.execute_query(
                        "SELECT id FROM company WHERE name = %s", (company_name,), fetch=True
                    )[0][0]
                    company_id = new_id

            # Получаем ID должности и статуса
            position_id = self.position_options[position]
            status_id = self.status_options[status]
            salary_val = float(self.salary_entry.get().strip()) if self.salary_entry.get().strip().replace('.', '', 1).isdigit() else None
            start_date = self.date_entry.get().strip()
            is_current = self.is_current_var.get()

            if self.employment_id:
                # Обновляем существующее
                query = """
                    UPDATE employment SET
                        company_id=%s, position_id=%s, status_id=%s,
                        start_date=%s, salary=%s, is_current=%s
                    WHERE id=%s
                """
                self.db.execute_query(query, (company_id, position_id, status_id, start_date, salary_val, is_current, self.employment_id))
            else:
                # Создаём новое
                query = """
                    INSERT INTO employment (graduate_id, company_id, position_id, status_id, start_date, salary, is_current)
                    VALUES (%s, %s, %s, %s, %s, %s, %s)
                """
                self.db.execute_query(query, (graduate_id, company_id, position_id, status_id, start_date, salary_val, is_current))

            messagebox.showinfo("Успех", "Данные о трудоустройстве сохранены!")
            self.window.destroy()

        except Exception as e:
            messagebox.showerror("Ошибка", f"Не удалось сохранить данные:\n{e}")
        finally:
            self.db.disconnect()

    def get_default_industry_id(self):
        try:
            res = self.db.execute_query("SELECT id FROM industry WHERE name = 'Другое'", fetch=True)
            if res:
                return res[0][0]
            res = self.db.execute_query("SELECT id FROM industry ORDER BY id LIMIT 1", fetch=True)
            return res[0][0] if res else 1
        except:

            return 1
