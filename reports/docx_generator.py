# Генерация отчётов в формате .docx

from docx import Document
from docx.shared import Pt
from docx.enum.text import WD_ALIGN_PARAGRAPH
import os
from datetime import datetime
from config import AUTHOR_NAME


class DocxReportGenerator:
    """Генератор отчётов в формате Microsoft Word (.docx)."""

    @staticmethod
    def generate_employment_report(data, output_path):
        """
        Создаёт отчёт о трудоустройстве.
        :param data: список словарей с данными о выпускниках и трудоустройстве
        :param output_path: путь для сохранения .docx файла
        """
        doc = Document()

        # Заголовок
        title = doc.add_heading('Отчёт о трудоустройстве выпускников МУИВ', 0)
        title.alignment = WD_ALIGN_PARAGRAPH.CENTER

        # Подзаголовок
        subtitle = doc.add_paragraph(f'Сформировано: {datetime.now().strftime("%d.%m.%Y %H:%M")}')
        subtitle.alignment = WD_ALIGN_PARAGRAPH.CENTER
        subtitle.runs[0].font.size = Pt(10)

        doc.add_paragraph()  # пустая строка

        # Таблица
        if data:
            table = doc.add_table(rows=1, cols=5)
            table.style = 'Table Grid'
            hdr_cells = table.rows[0].cells
            headers = ["ФИО", "Год выпуска", "Компания", "Должность", "Статус"]
            for i, header in enumerate(headers):
                hdr_cells[i].text = header
                hdr_cells[i].paragraphs[0].runs[0].font.bold = True

            for item in data:
                row_cells = table.add_row().cells
                row_cells[0].text = item.get('full_name', '—')
                row_cells[1].text = str(item.get('graduation_year', '—'))
                row_cells[2].text = item.get('company', '—')
                row_cells[3].text = item.get('position', '—')
                row_cells[4].text = item.get('status', '—')
        else:
            doc.add_paragraph("Нет данных для отчёта.")

        # Подпись
        doc.add_paragraph()
        footer = doc.add_paragraph(f"Автор: {AUTHOR_NAME}")
        footer.alignment = WD_ALIGN_PARAGRAPH.RIGHT
        footer.runs[0].font.italic = True

        # Сохранение
        os.makedirs(os.path.dirname(output_path), exist_ok=True)
        doc.save(output_path)
        return output_path
