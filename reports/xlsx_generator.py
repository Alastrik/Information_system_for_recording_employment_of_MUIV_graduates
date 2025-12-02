# Генерация отчётов в формате .xlsx

import openpyxl
from openpyxl.styles import Font, Alignment, Border, Side
from datetime import datetime
import os

class XlsxReportGenerator:
    """Генератор отчётов в формате Excel (.xlsx)."""

    @staticmethod
    def generate_employment_report(data, output_path):
        """
        Создаёт Excel-отчёт о трудоустройстве.
        :param data: список словарей с данными
        :param output_path: путь для сохранения .xlsx файла
        """
        wb = openpyxl.Workbook()
        ws = wb.active
        ws.title = "Трудоустройство"

        # Заголовок
        ws.merge_cells('A1:E1')
        ws['A1'] = 'Отчёт о трудоустройстве выпускников МУИВ'
        ws['A1'].font = Font(size=14, bold=True)
        ws['A1'].alignment = Alignment(horizontal="center")

        ws.merge_cells('A2:E2')
        ws['A2'] = f'Сформировано: {datetime.now().strftime("%d.%m.%Y %H:%M")}'
        ws['A2'].font = Font(size=10, italic=True)
        ws['A2'].alignment = Alignment(horizontal="center")

        # Пустая строка
        ws.append([])

        # Заголовки таблицы
        headers = ["ФИО", "Год выпуска", "Компания", "Должность", "Статус"]
        ws.append(headers)
        header_font = Font(bold=True)
        for col in range(1, 6):
            ws.cell(row=4, column=col).font = header_font
            ws.cell(row=4, column=col).alignment = Alignment(horizontal="center")

        # Данные
        for item in data:
            ws.append([
                item.get('full_name', '—'),
                item.get('graduation_year', '—'),
                item.get('company', '—'),
                item.get('position', '—'),
                item.get('status', '—')
            ])

        # Автоподбор ширины
        for col in ws.columns:
            max_length = 0
            column = col[0].column_letter
            for cell in col:
                try:
                    if len(str(cell.value)) > max_length:
                        max_length = len(str(cell.value))
                except:
                    pass
            adjusted_width = min(max_length + 2, 50)
            ws.column_dimensions[column].width = adjusted_width

        # Сохранение
        os.makedirs(os.path.dirname(output_path), exist_ok=True)
        wb.save(output_path)
        return output_path