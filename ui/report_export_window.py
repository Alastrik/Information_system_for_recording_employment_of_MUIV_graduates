# Диалог экспорта отчётов

import tkinter as tk
from tkinter import filedialog, messagebox
from reports.docx_generator import DocxReportGenerator
from reports.xlsx_generator import XlsxReportGenerator
from database import DatabaseConnection
from utils.file_manager import FileManager
import os

class ReportExportWindow:
    """Окно выбора формата и экспорта отчёта."""

    def __init__(self, parent, user_data):
        self.window = tk.Toplevel(parent)
        self.window.title("Экспорт отчёта")
        self.window.geometry("500x250")
        self.center_window(parent)

        self.user_data = user_data
        self.db = DatabaseConnection()
        self.db.connect()

        tk.Label(self.window, text="Выберите формат отчёта", font=("Arial", 12, "bold")).pack(pady=20)

        btn_frame = tk.Frame(self.window)
        btn_frame.pack(pady=10)
        tk.Button(btn_frame, text="Экспорт в Word (.docx)", command=self.export_docx, width=25, font=("Arial", 10)).pack(pady=5)
        tk.Button(btn_frame, text="Экспорт в Excel (.xlsx)", command=self.export_xlsx, width=25, font=("Arial", 10)).pack(pady=5)
        tk.Button(btn_frame, text="Отмена", command=self.window.destroy, width=25, font=("Arial", 10)).pack(pady=10)

    def center_window(self, parent):
        x = parent.winfo_rootx() + 100
        y = parent.winfo_rooty() + 100
        self.window.geometry(f"500x250+{x}+{y}")

    def fetch_employment_data(self):
        """Заглушка: возвращает демо-данные. В реальном проекте — запрос к БД."""
        return [
            {
                "full_name": "Иванов Иван Иванович",
                "graduation_year": 2024,
                "company": "ООО 'ТехноПрогресс'",
                "position": "Программист",
                "status": "Работает"
            },
            {
                "full_name": "Петрова Анна Сергеевна",
                "graduation_year": 2023,
                "company": "АО 'Финора'",
                "position": "Аналитик",
                "status": "Уволена"
            }
        ]

    def export_docx(self):
        self._export("docx")

    def export_xlsx(self):
        self._export("xlsx")

    def _export(self, fmt):
        try:
            data = self.fetch_employment_data()
            default_dir = FileManager.get_default_report_dir()
            os.makedirs(default_dir, exist_ok=True)

            if fmt == "docx":
                filepath = filedialog.asksaveasfilename(
                    initialdir=default_dir,
                    defaultextension=".docx",
                    filetypes=[("Word документ", "*.docx")]
                )
                if filepath:
                    DocxReportGenerator.generate_employment_report(data, filepath)
                    messagebox.showinfo("Успех", f"Отчёт сохранён:\n{filepath}")
            else:
                filepath = filedialog.asksaveasfilename(
                    initialdir=default_dir,
                    defaultextension=".xlsx",
                    filetypes=[("Excel файл", "*.xlsx")]
                )
                if filepath:
                    XlsxReportGenerator.generate_employment_report(data, filepath)
                    messagebox.showinfo("Успех", f"Отчёт сохранён:\n{filepath}")

            self.window.destroy()
        except Exception as e:
            messagebox.showerror("Ошибка", f"Не удалось сгенерировать отчёт:\n{e}")