# Форма ввода данных о трудоустройстве

import tkinter as tk
from tkinter import ttk, messagebox
from database import DatabaseConnection
from ui.confirmation_dialog import show_confirmation

class EmploymentFormWindow:
    """Форма для ввода или редактирования данных о трудоустройстве."""

    def __init__(self, parent, user_data):
        self.window = tk.Toplevel(parent)
        self.window.title("Форма трудоустройства")
        self.window.geometry("550x500")
        self.window.resizable(False, False)
        self.center_window(parent)

        self.user_data = user_data
        self.db = DatabaseConnection()
        self.db.connect()

        self.setup_ui()
        self.load_dropdown_data()

    def center_window(self, parent):
        parent_x = parent.winfo_rootx()
        parent_y = parent.winfo_rooty()
        x = parent_x + 50
        y = parent_y + 50
        self.window.geometry(f"550x500+{x}+{y}")

    def load_dropdown_data(self):
        """Загружает справочники из БД для выпадающих списков."""
        try:
            # Компании
            companies = self.db.execute_query("SELECT id, name FROM company ORDER BY name", fetch=True)
            self.company_options = {name: id for id, name in companies}
            self.company_combo['values'] = list(self.company_options.keys())

            # Должности
            positions = self.db.execute_query("SELECT id, title FROM position ORDER BY title", fetch=True)
            self.position_options = {title: id for id, title in positions}
            self.position_combo['values'] = list(self.position_options.keys())

            # Статусы
            statuses = self.db.execute_query("SELECT id, status_name FROM employment_status ORDER BY id", fetch=True)
            self.status_options = {name: id for id, name in statuses}
            self.status_combo['values'] = list(self.status_options.keys())

        except Exception as e:
            messagebox.showerror("Ошибка", f"Не удалось загрузить справочники:\n{e}")

    def setup_ui(self):
        tk.Label(self.window, text="Добавить информацию о трудоустройстве", font=("Arial", 12, "bold")).pack(pady=10)

        # Выбор выпускника (в реальном проекте — автоподбор по ФИО)
        tk.Label(self.window, text="Выпускник (ФИО):", font=("Arial", 10)).pack(anchor="w", padx=20)
        self.graduate_entry = tk.Entry(self.window, width=50)
        self.graduate_entry.pack(pady=5, padx=20)

        # Компания
        tk.Label(self.window, text="Организация:", font=("Arial", 10)).pack(anchor="w", padx=20)
        self.company_combo = ttk.Combobox(self.window, state="readonly", width=47)
        self.company_combo.pack(pady=5, padx=20)

        # Должность
        tk.Label(self.window, text="Должность:", font=("Arial", 10)).pack(anchor="w", padx=20)
        self.position_combo = ttk.Combobox(self.window, state="readonly", width=47)
        self.position_combo.pack(pady=5, padx=20)

        # Статус
        tk.Label(self.window, text="Статус трудоустройства:", font=("Arial", 10)).pack(anchor="w", padx=20)
        self.status_combo = ttk.Combobox(self.window, state="readonly", width=47)
        self.status_combo.pack(pady=5, padx=20)

        # Дата начала
        tk.Label(self.window, text="Дата начала работы (ГГГГ-ММ-ДД):", font=("Arial", 10)).pack(anchor="w", padx=20)
        self.date_entry = tk.Entry(self.window, width=50)
        self.date_entry.pack(pady=5, padx=20)
        self.date_entry.insert(0, "2025-01-01")

        # Зарплата
        tk.Label(self.window, text="Зарплата (руб.):", font=("Arial", 10)).pack(anchor="w", padx=20)
        self.salary_entry = tk.Entry(self.window, width=50)
        self.salary_entry.pack(pady=5, padx=20)

        # Текущая работа?
        self.is_current_var = tk.BooleanVar(value=True)
        tk.Checkbutton(self.window, text="Текущее место работы", variable=self.is_current_var, font=("Arial", 10)).pack(pady=10)

        # Кнопки
        btn_frame = tk.Frame(self.window)
        btn_frame.pack(pady=20)
        tk.Button(btn_frame, text="Сохранить", command=self.save_employment, font=("Arial", 11), width=12).pack(side="left", padx=10)
        tk.Button(btn_frame, text="Отмена", command=self.window.destroy, font=("Arial", 11), width=12).pack(side="left", padx=10)

    def save_employment(self):
        """Сохраняет данные о трудоустройстве в БД."""
        graduate_name = self.graduate_entry.get().strip()
        company_name = self.company_combo.get()
        position_title = self.position_combo.get()
        status_name = self.status_combo.get()
        start_date = self.date_entry.get().strip()
        salary = self.salary_entry.get().strip()

        if not graduate_name or not company_name or not position_title or not status_name:
            messagebox.showwarning("Ошибка", "Заполните все обязательные поля!")
            return

        if not show_confirmation(self.window, "Сохранение", "Сохранить данные о трудоустройстве?"):
            return

        try:
            # В учебной версии — не связываем с реальным graduate.id, просто сохраняем как строку
            # В продакшене — нужно искать graduate.id по ФИО
            company_id = self.company_options[company_name]
            position_id = self.position_options[position_title]
            status_id = self.status_options[status_name]
            salary_val = float(salary) if salary else None

            # Заглушка: используем graduate_id = 1 (для демонстрации)
            query = """
                INSERT INTO employment (graduate_id, company_id, position_id, status_id, start_date, salary, is_current)
                VALUES (%s, %s, %s, %s, %s, %s, %s)
            """
            self.db.execute_query(query, (1, company_id, position_id, status_id, start_date, salary_val, self.is_current_var.get()))
            messagebox.showinfo("Успех", "Данные о трудоустройстве сохранены!")
            self.window.destroy()
        except Exception as e:
            messagebox.showerror("Ошибка", f"Не удалось сохранить данные:\n{e}")
        finally:
            self.db.disconnect()