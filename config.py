# Конфигурационный файл приложения
# Содержит настройки подключения к БД и учётные данные для демонстрации

# Подключение к PostgreSQL
DB_CONFIG = {
    'host': 'localhost',
    'port': 5432,
    'database': 'muiv_employment',
    'user': 'postgres',
    'password': '1111'
}

# Учётные записи пользователей для проверки (будут добавлены в БД при первом запуске или через миграции)
DEMO_USERS = [
    {
        'username': 'admin',
        'password': 'admin123',
        'role': 'admin',
        'faculty_id': None
    },
    {
        'username': 'hr_muiiv',
        'password': 'hrpass2025',
        'role': 'manager',
        'faculty_id': 1
    },
    {
        'username': 'graduate_001',
        'password': 'grad2025',
        'role': 'graduate',
        'faculty_id': 1
    }
]


AUTHOR_NAME = "Монахов Артем Сергеевич"