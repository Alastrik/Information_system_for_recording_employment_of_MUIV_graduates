# ui/user_management.py
# Управление пользователями (только для администратора)

import tkinter as tk
from tkinter import ttk, messagebox
from database import DatabaseConnection

class UserManagementWindow:
    """Окно управления пользователями системы."""

    def __init__(self, parent, current_user_id):
        self.window = tk.Toplevel(parent)
        self.window.title("Управление пользователями")
        self.window.geometry("750x450")
        self.center_window(parent)

        self.current_user_id = current_user_id  # ID текущего админа (чтобы нельзя было удалить себя)
        self.db = DatabaseConnection()
        self.db.connect()

        self.setup_ui()
        self.load_users()

    def center_window(self, parent):
        parent_x = parent.winfo_rootx()
        parent_y = parent.winfo_rooty()
        x = parent_x + 30
        y = parent_y + 30
        self.window.geometry(f"750x450+{x}+{y}")

    def setup_ui(self):
        tk.Label(self.window, text="Список пользователей", font=("Arial", 12, "bold")).pack(pady=10)

        # Таблица
        columns = ("ID", "Логин", "Роль", "Факультет", "Активен")
        self.tree = ttk.Treeview(self.window, columns=columns, show="headings", height=12)
        for col in columns:
            self.tree.heading(col, text=col)
            self.tree.column(col, width=120, anchor="center")
        self.tree.pack(padx=20, pady=10, fill="both", expand=True)

        # Кнопки
        btn_frame = tk.Frame(self.window)
        btn_frame.pack(pady=10)
        tk.Button(btn_frame, text="Обновить", command=self.load_users, font=("Arial", 10), width=10).pack(side="left", padx=5)
        tk.Button(btn_frame, text="Удалить выбранного", command=self.delete_user, font=("Arial", 10), bg="#f44336", fg="white", width=15).pack(side="left", padx=5)
        tk.Button(btn_frame, text="Закрыть", command=self.window.destroy, font=("Arial", 10), width=10).pack(side="left", padx=5)

    def load_users(self):
        """Загружает список пользователей из БД."""
        for item in self.tree.get_children():
            self.tree.delete(item)

        try:
            query = """
                SELECT 
                    u.id, 
                    u.username, 
                    up.role, 
                    f.name AS faculty,
                    u.is_active
                FROM auth_user u
                JOIN user_profile up ON u.id = up.user_id
                LEFT JOIN faculty f ON up.faculty_id = f.id
                ORDER BY u.id
            """
            users = self.db.execute_query(query, fetch=True)
            if users:
                for user in users:
                    status = "Да" if user[4] else "Нет"
                    faculty = user[3] if user[3] else "—"
                    self.tree.insert("", "end", values=(user[0], user[1], user[2], faculty, status))
        except Exception as e:
            messagebox.showerror("Ошибка", f"Не удалось загрузить пользователей:\n{e}")

    def delete_user(self):
        """Удаляет выбранного пользователя (кроме самого админа)."""
        selected = self.tree.selection()
        if not selected:
            messagebox.showwarning("Внимание", "Выберите пользователя для удаления!")
            return

        item = self.tree.item(selected[0])
        user_id = item['values'][0]
        username = item['values'][1]

        # Защита: нельзя удалить самого себя
        if user_id == self.current_user_id:
            messagebox.showerror("Ошибка", "Нельзя удалить самого себя!")
            return

        # Подтверждение
        confirm = messagebox.askyesno(
            "Подтверждение удаления",
            f"Вы уверены, что хотите удалить пользователя:\n{username} (ID: {user_id})?\n\nЭто действие необратимо!"
        )
        if not confirm:
            return

        try:
            # Удаление пользователя (каскадно удалятся user_profile, graduate, employment и т.д.)
            self.db.execute_query("DELETE FROM auth_user WHERE id = %s", (user_id,))
            messagebox.showinfo("Успех", f"Пользователь {username} удалён!")
            self.load_users()  # Обновить список
        except Exception as e:
            messagebox.showerror("Ошибка", f"Не удалось удалить пользователя:\n{e}")

    def __del__(self):
        if hasattr(self, 'db') and self.db.connection:
            self.db.disconnect()