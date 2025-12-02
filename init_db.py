# Инициализация базы данных: создание демо-пользователей и справочников
# Запускать один раз при первом развёртывании

from database import DatabaseConnection
from config import DEMO_USERS

def init_database():
    db = DatabaseConnection()
    db.connect()

    try:
        # === 1. Базовые справочники ===
        print("Проверка и создание справочников...")

        # Факультеты
        db.execute_query("INSERT INTO faculty (name) VALUES ('Информационных технологий') ON CONFLICT DO NOTHING;")
        db.execute_query("INSERT INTO faculty (name) VALUES ('Экономики и управления') ON CONFLICT DO NOTHING;")

        # Отрасли
        db.execute_query("INSERT INTO industry (name) VALUES ('IT') ON CONFLICT DO NOTHING;")
        db.execute_query("INSERT INTO industry (name) VALUES ('Финансы') ON CONFLICT DO NOTHING;")

        # Статусы трудоустройства
        db.execute_query("INSERT INTO employment_status (status_name) VALUES ('Работает') ON CONFLICT DO NOTHING;")
        db.execute_query("INSERT INTO employment_status (status_name) VALUES ('Уволен') ON CONFLICT DO NOTHING;")
        db.execute_query("INSERT INTO employment_status (status_name) VALUES ('Ищет работу') ON CONFLICT DO NOTHING;")

        # Должности
        db.execute_query("INSERT INTO position (title) VALUES ('Программист') ON CONFLICT DO NOTHING;")
        db.execute_query("INSERT INTO position (title) VALUES ('Аналитик') ON CONFLICT DO NOTHING;")

        # Компании
        db.execute_query("""
            INSERT INTO company (name, industry_id)
            SELECT 'ООО ТехноПрогресс', id FROM industry WHERE name = 'IT'
            ON CONFLICT DO NOTHING;
        """)
        db.execute_query("""
            INSERT INTO company (name, industry_id)
            SELECT 'АО Финора', id FROM industry WHERE name = 'Финансы'
            ON CONFLICT DO NOTHING;
        """)

        # === 2. Демо-пользователи ===
        print("Создание демо-пользователей...")
        for user in DEMO_USERS:
            # Проверяем, существует ли пользователь
            check = db.execute_query(
                "SELECT id FROM auth_user WHERE username = %s",
                (user['username'],),
                fetch=True
            )
            if not check:
                # Создаём auth_user
                db.execute_query("""
                    INSERT INTO auth_user (username, password, is_active)
                    VALUES (%s, %s, TRUE)
                    RETURNING id;
                """, (user['username'], user['password']))
                user_id = db.cursor.fetchone()[0]

                # Определяем faculty_id (если указан)
                faculty_id = None
                if user['faculty_id']:
                    fac = db.execute_query(
                        "SELECT id FROM faculty WHERE id = %s",
                        (user['faculty_id'],),
                        fetch=True
                    )
                    if fac:
                        faculty_id = fac[0][0]

                # Создаём user_profile
                db.execute_query("""
                    INSERT INTO user_profile (user_id, role, faculty_id)
                    VALUES (%s, %s, %s);
                """, (user_id, user['role'], faculty_id))

                print(f"✅ Создан пользователь: {user['username']} ({user['role']})")
            else:
                print(f"⚠️ Пользователь {user['username']} уже существует.")

        print("✅ Инициализация базы данных завершена.")

    except Exception as e:
        print(f"❌ Ошибка инициализации: {e}")
    finally:
        db.disconnect()

if __name__ == "__main__":
    init_database()