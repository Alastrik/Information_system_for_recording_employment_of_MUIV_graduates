# Работа с файловой системой: создание папок, сохранение файлов

import os
import logging
from pathlib import Path

class FileManager:
    """Утилиты для работы с файловой системой."""

    @staticmethod
    def ensure_directory(path):
        """Создаёт директорию, если она не существует."""
        try:
            Path(path).mkdir(parents=True, exist_ok=True)
            return True
        except Exception as e:
            logging.error(f"Ошибка создания директории {path}: {e}")
            return False

    @staticmethod
    def save_file(filepath, content, mode='w'):
        """Сохраняет содержимое в файл."""
        try:
            FileManager.ensure_directory(os.path.dirname(filepath))
            with open(filepath, mode, encoding='utf-8' if 'b' not in mode else None) as f:
                f.write(content)
            return True
        except Exception as e:
            logging.error(f"Ошибка сохранения файла {filepath}: {e}")
            return False

    @staticmethod
    def get_default_report_dir():
        """Возвращает путь к папке по умолчанию для отчётов."""
        return os.path.join(os.path.expanduser("~"), "MUIV_Employment_Reports")