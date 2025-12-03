# Конфигурационный файл приложения
# Содержит настройки подключения к БД и учётные данные для демонстрации (только для практики!)

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


# Цветовые схемы
THEMES = {
    "Светлая": {
        "bg": "#ffffff",
        "fg": "#000000",
        "button_bg": "#e0e0e0",
        "button_fg": "#000000",
        "entry_bg": "#ffffff",
        "frame_bg": "#f5f5f5"
    },
    "Тёмная": {
        "bg": "#2d2d2d",
        "fg": "#ffffff",
        "button_bg": "#444444",
        "button_fg": "#ffffff",
        "entry_bg": "#3c3c3c",
        "frame_bg": "#252525"
    }
}

CURRENT_THEME = "Светлая"