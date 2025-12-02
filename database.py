# Модуль подключения к PostgreSQL и выполнения SQL-запросов
# Используется библиотека psycopg2

import psycopg2
from psycopg2 import sql
from config import DB_CONFIG
import logging

# Настройка логирования
logging.basicConfig(level=logging.INFO)


class DatabaseConnection:
    """Класс для управления подключением к базе данных PostgreSQL."""

    def __init__(self):
        self.connection = None
        self.cursor = None

    def connect(self):
        """Устанавливает соединение с базой данных."""
        try:
            self.connection = psycopg2.connect(
                host=DB_CONFIG['host'],
                port=DB_CONFIG['port'],
                database=DB_CONFIG['database'],
                user=DB_CONFIG['user'],
                password=DB_CONFIG['password']
            )
            self.cursor = self.connection.cursor()
            logging.info("Успешное подключение к базе данных PostgreSQL.")
        except Exception as e:
            logging.error(f"Ошибка подключения к базе данных: {e}")
            raise

    def disconnect(self):
        """Закрывает соединение с базой данных."""
        if self.cursor:
            self.cursor.close()
        if self.connection:
            self.connection.close()
        logging.info("Соединение с базой данных закрыто.")

    def execute_query(self, query, params=None, fetch=False):
        """
        Выполняет SQL-запрос.
        :param query: SQL-запрос (строка или объект sql.Composed)
        :param params: Параметры для запроса (для защиты от SQL-инъекций)
        :param fetch: Если True — возвращает результат (fetchall)
        :return: Результат запроса или None
        """
        try:
            self.cursor.execute(query, params)
            if fetch:
                return self.cursor.fetchall()
            else:
                self.connection.commit()
                return True
        except Exception as e:
            self.connection.rollback()
            logging.error(f"Ошибка выполнения запроса: {e}")
            raise