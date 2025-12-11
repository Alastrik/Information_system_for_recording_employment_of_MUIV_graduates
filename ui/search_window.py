# ui/search_window.py
# Расширенный поиск выпускников по ФИО

import tkinter as tk
from tkinter import ttk, messagebox
from database import DatabaseConnection


class SearchWindow:
    """Окно поиска выпускников по имени, фамилии или ФИО."""

    def __init__(self, parent):
        self.window = tk.Toplevel(parent)
        self.window.title("Поиск выпускников")
        self.window.geometry("700x500")
        self.window.configure(bg="#f9f9f9")

        # Центрирование относительно родителя
        self.center_window(parent)

        # Подключение к БД
        self.db = DatabaseConnection()
        self.db.connect()

        self.setup_ui()

    def center_window(self, parent):
        parent_x = parent.winfo_rootx()
        parent_y = parent.winfo_rooty()
        x = parent_x + 50
        y = parent_y + 50
        self.window.geometry(f"700x500+{x}+{y}")

    def setup_ui(self):
        # Заголовок
        tk.Label(
            self.window, text="Поиск выпускников",
            font=("Arial", 14, "bold"), bg="#f9f9f9", fg="#2c3e50"
        ).pack(pady=15)

        # Поле ввода
        input_frame = tk.Frame(self.window, bg="#f9f9f9")
        input_frame.pack(pady=10)

        tk.Label(input_frame, text="Введите имя, фамилию или ФИО:", bg="#f9f9f9", font=("Arial", 10)).pack(anchor="w",
                                                                                                           padx=20)
        self.search_entry = tk.Entry(input_frame, font=("Arial", 11), width=50)
        self.search_entry.pack(padx=20, pady=5)
        self.search_entry.bind("<Return>", lambda e: self.perform_search())

        # Кнопки
        btn_frame = tk.Frame(self.window, bg="#f9f9f9")
        btn_frame.pack(pady=10)
        tk.Button(
            btn_frame, text="Найти", command=self.perform_search,
            bg="#2196F3", fg="white", font=("Arial", 10, "bold"), width=12
        ).pack(side="left", padx=10)
        tk.Button(
            btn_frame, text="Сбросить", command=self.reset_search,
            bg="#9E9E9E", fg="white", font=("Arial", 10), width=12
        ).pack(side="left", padx=10)
        tk.Button(
            btn_frame, text="Закрыть", command=self.window.destroy,
            bg="#f44336", fg="white", font=("Arial", 10), width=12
        ).pack(side="left", padx=10)

        # Метка с количеством результатов
        self.result_label = tk.Label(self.window, text="Найдено: 0 записей", bg="#f9f9f9", font=("Arial", 10, "bold"))
        self.result_label.pack(pady=5)

        # Таблица результатов
        columns = ("ФИО", "Год выпуска", "Факультет", "Компания", "Должность", "Статус")
        self.tree = ttk.Treeview(self.window, columns=columns, show="headings", height=12)

        # Настройка стиля
        style = ttk.Style()
        style.configure("Treeview", font=("Arial", 9), rowheight=25)
        style.configure("Treeview.Heading", font=("Arial", 10, "bold"))

        for col in columns:
            self.tree.heading(col, text=col)
            self.tree.column(col, width=100, anchor="center")

        # Прокрутка
        scrollbar = ttk.Scrollbar(self.window, orient="vertical", command=self.tree.yview)
        self.tree.configure(yscroll=scrollbar.set)

        self.tree.pack(padx=20, pady=10, fill="both", expand=True)
        scrollbar.pack(side="right", fill="y")

    def perform_search(self):
        """Выполняет поиск в базе данных по ФИО."""
        query = self.search_entry.get().strip()
        if not query:
            messagebox.showwarning("Внимание", "Введите текст для поиска!")
            return

        try:
            # SQL-запрос: поиск по полю full_name с использованием ILIKE (регистронезависимый)
            sql = """
                SELECT 
                    g.full_name,
                    g.graduation_year,
                    f.name AS faculty,
                    c.name AS company,
                    p.title AS position,
                    es.status_name
                FROM graduate g
                LEFT JOIN user_profile up ON g.user_profile_id = up.id
                LEFT JOIN faculty f ON up.faculty_id = f.id
                LEFT JOIN employment e ON g.id = e.graduate_id
                LEFT JOIN company c ON e.company_id = c.id
                LEFT JOIN position p ON e.position_id = p.id
                LEFT JOIN employment_status es ON e.status_id = es.id
                WHERE g.full_name ILIKE %s
                ORDER BY g.full_name
            """
            # Добавляем % вокруг запроса для частичного совпадения
            like_pattern = f"%{query}%"
            results = self.db.execute_query(sql, (like_pattern,), fetch=True)

            # Очистка таблицы
            for item in self.tree.get_children():
                self.tree.delete(item)

            # Вставка результатов
            for row in results:
                self.tree.insert("", "end", values=row)

            # Обновление счётчика
            count = len(results)
            self.result_label.config(text=f"Найдено: {count} записей", fg="green" if count > 0 else "red")

        except Exception as e:
            messagebox.showerror("Ошибка", f"Не удалось выполнить поиск:\n{e}")

    def reset_search(self):
        """Сбрасывает поиск."""
        self.search_entry.delete(0, tk.END)
        for item in self.tree.get_children():
            self.tree.delete(item)
        self.result_label.config(text="Найдено: 0 записей", fg="black")

    def __del__(self):
        """Закрываем соединение с БД при уничтожении окна."""
        if hasattr(self, 'db') and self.db.connection:

            self.db.disconnect()
