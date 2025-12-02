# Окно "Справка по системе"

import tkinter as tk
from tkinter import ttk
from config import AUTHOR_NAME

class HelpWindow:
    """Окно справки с описанием функционала и информацией об авторе."""

    def __init__(self, parent):
        self.window = tk.Toplevel(parent)
        self.window.title("Справка по системе")
        self.window.geometry("600x400")
        self.window.resizable(False, False)
        self.center_window(parent)

        # Заголовок
        title_label = tk.Label(
            self.window,
            text="Справка по информационной системе\n«Учёт трудоустройства выпускников МУИВ»",
            font=("Arial", 14, "bold"),
            justify="center"
        )
        title_label.pack(pady=(15, 10))

        # Текст справки
        help_text = (
            "Система предназначена для учёта и анализа трудоустройства выпускников\n"
            "Частного образовательного учреждения высшего образования\n"
            "«Московский университет имени С.Ю. Витте» (МУИВ).\n\n"
            "Основные функции:\n"
            "• Ввод и редактирование данных о трудоустройстве\n"
            "• Формирование отчётов в форматах .docx и .xlsx\n"
            "• Разграничение доступа по ролям (администратор, HR, выпускник)\n"
            "• Просмотр статистики и экспорта данных\n"
            "• Личный кабинет выпускника\n"
            "• Панель управления для администратора\n\n"
            "Автор программного обеспечения:\n"
            f"{AUTHOR_NAME}\n"
            "© 2025. Все права защищены."
        )

        text_label = tk.Label(
            self.window,
            text=help_text,
            font=("Arial", 10),
            justify="left",
            padx=20,
            pady=10
        )
        text_label.pack(anchor="w")

        # Кнопка закрытия
        close_button = tk.Button(
            self.window,
            text="Закрыть",
            command=self.window.destroy,
            font=("Arial", 11),
            width=12
        )
        close_button.pack(pady=15)

    def center_window(self, parent):
        """Центрирует окно относительно родительского."""
        parent_x = parent.winfo_rootx()
        parent_y = parent.winfo_rooty()
        parent_width = parent.winfo_width()
        parent_height = parent.winfo_height()

        x = parent_x + (parent_width // 2) - 300
        y = parent_y + (parent_height // 2) - 200
        self.window.geometry(f"600x400+{x}+{y}")