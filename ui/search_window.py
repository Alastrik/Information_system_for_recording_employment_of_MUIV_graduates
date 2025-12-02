# Поиск и фильтрация выпускников

import tkinter as tk
from tkinter import ttk

class SearchWindow:
    """Окно поиска выпускников."""

    def __init__(self, parent):
        self.window = tk.Toplevel(parent)
        self.window.title("Поиск выпускников")
        self.window.geometry("600x300")
        self.center_window(parent)

        tk.Label(self.window, text="Поиск и фильтрация", font=("Arial", 12, "bold")).pack(pady=15)

        # Поля поиска
        frame = tk.Frame(self.window)
        frame.pack(padx=20, pady=10)

        tk.Label(frame, text="ФИО:", font=("Arial", 10)).grid(row=0, column=0, sticky="w", pady=5)
        self.name_entry = tk.Entry(frame, width=30)
        self.name_entry.grid(row=0, column=1, pady=5, padx=10)

        tk.Label(frame, text="Год выпуска:", font=("Arial", 10)).grid(row=1, column=0, sticky="w", pady=5)
        self.year_entry = tk.Entry(frame, width=30)
        self.year_entry.grid(row=1, column=1, pady=5, padx=10)

        tk.Label(frame, text="Компания:", font=("Arial", 10)).grid(row=2, column=0, sticky="w", pady=5)
        self.company_entry = tk.Entry(frame, width=30)
        self.company_entry.grid(row=2, column=1, pady=5, padx=10)

        # Кнопки
        btn_frame = tk.Frame(self.window)
        btn_frame.pack(pady=20)
        tk.Button(btn_frame, text="Найти", command=self.search, font=("Arial", 10), width=12).pack(side="left", padx=10)
        tk.Button(btn_frame, text="Сбросить", command=self.reset, font=("Arial", 10), width=12).pack(side="left", padx=10)
        tk.Button(btn_frame, text="Закрыть", command=self.window.destroy, font=("Arial", 10), width=12).pack(side="left", padx=10)

    def center_window(self, parent):
        x = parent.winfo_rootx() + 50
        y = parent.winfo_rooty() + 50
        self.window.geometry(f"600x300+{x}+{y}")

    def search(self):
        # Заглушка: в реальном проекте — запрос к БД с фильтрами
        name = self.name_entry.get().strip()
        year = self.year_entry.get().strip()
        company = self.company_entry.get().strip()
        print(f"Поиск: ФИО={name}, Год={year}, Компания={company}")
        # Здесь можно открыть результаты в новом окне

    def reset(self):
        self.name_entry.delete(0, tk.END)
        self.year_entry.delete(0, tk.END)
        self.company_entry.delete(0, tk.END)