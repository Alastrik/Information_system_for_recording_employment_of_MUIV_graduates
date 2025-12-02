# Модуль аутентификации и управления ролями пользователей

from database import DatabaseConnection


class AuthService:
    """Сервис аутентификации пользователей в системе."""

    def __init__(self):
        self.db = DatabaseConnection()
        self.db.connect()

    def authenticate(self, username, password):
        """
        Проверяет учётные данные пользователя.
        Возвращает словарь с данными пользователя или None.
        """
        query = """
            SELECT u.id, u.username, up.role, up.faculty_id
            FROM auth_user u
            JOIN user_profile up ON u.id = up.user_id
            WHERE u.username = %s AND u.password = %s AND u.is_active = TRUE
        """
        result = self.db.execute_query(query, (username, password), fetch=True)
        if result:
            row = result[0]
            return {
                'user_id': row[0],
                'username': row[1],
                'role': row[2],
                'faculty_id': row[3]
            }
        return None

    def close(self):
        """Закрывает соединение с БД."""
        self.db.disconnect()