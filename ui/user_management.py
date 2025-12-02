# Управление пользователями (только для администратора)

import tkinter as tk
from tkinter import ttk, messagebox
from database import DatabaseConnection

class UserManagementWindow:
    """Окно управления пользователями системы."""

    def __init__(self, parent):
        self.window = tk.Toplevel(parent)
        self.window.title("Управление пользователями")
        self.window.geometry("700x400")
        self.center_window(parent)

        self.db = DatabaseConnection()
        self.db.connect()

        self.setup_ui()
        self.load_users()

    def center_window(self, parent):
        parent_x = parent.winfo_rootx()
        parent_y = parent.winfo_rooty()
        x = parent_x + 30
        y = parent_y + 30
        self.window.geometry(f"700x400+{x}+{y}")

    def setup_ui(self):
        tk.Label(self.window, text="Список пользователей", font=("Arial", 12, "bold")).pack(pady=10)

        # Таблица
        columns = ("ID", "Логин", "Роль", "Активен")
        self.tree = ttk.Treeview(self.window, columns=columns, show="headings", height=10)
        for col in columns:
            self.tree.heading(col, text=col)
            self.tree.column(col, width=120, anchor="center")
        self.tree.pack(padx=20, pady=10, fill="both", expand=True)

        # Кнопки
        btn_frame = tk.Frame(self.window)
        btn_frame.pack(pady=10)
        tk.Button(btn_frame, text="Обновить", command=self.load_users, font=("Arial", 10)).pack(side="left", padx=5)
        tk.Button(btn_frame, text="Закрыть", command=self.window.destroy, font=("Arial", 10)).pack(side="left", padx=5)

    def load_users(self):
        """Загружает список пользователей из БД."""
        # Очищаем таблицу
        for item in self.tree.get_children():
            self.tree.delete(item)

        try:
            query = """
                SELECT u.id, u.username, up.role, u.is_active
                FROM auth_user u
                JOIN user_profile up ON u.id = up.user_id
                ORDER BY u.id
            """
            users = self.db.execute_query(query, fetch=True)
            if users:
                for user in users:  # ← ИСПРАВЛЕНО: было "for user in" без переменной
                    status = "Да" if user[3] else "Нет"
                    self.tree.insert("", "end", values=(user[0], user[1], user[2], status))
        except Exception as e:
            messagebox.showerror("Ошибка", f"Не удалось загрузить пользователей:\n{e}")
        finally:
            # НЕ закрываем соединение здесь — оно нужно для других действий
            # self.db.disconnect()  # закомментировано, т.к. окно может долго висеть
            pass