# init_db.py
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
        db.execute_query("INSERT INTO industry (name) VALUES ('Другое') ON CONFLICT DO NOTHING;")

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
            # Проверяем, существует ли auth_user
            check_user = db.execute_query(
                "SELECT id FROM auth_user WHERE username = %s",
                (user['username'],),
                fetch=True
            )
            if not check_user:
                # Создаём auth_user
                db.execute_query("""
                    INSERT INTO auth_user (username, password, is_active)
                    VALUES (%s, %s, TRUE)
                """, (user['username'], user['password']))
                user_id = db.execute_query(
                    "SELECT id FROM auth_user WHERE username = %s",
                    (user['username'],), fetch=True
                )[0][0]
                print(f"✅ Создан auth_user: {user['username']} (ID={user_id})")
            else:
                user_id = check_user[0][0]
                print(f"⚠️ auth_user {user['username']} уже существует (ID={user_id})")

            # Проверяем, существует ли user_profile
            check_profile = db.execute_query(
                "SELECT id FROM user_profile WHERE user_id = %s",
                (user_id,), fetch=True
            )
            if not check_profile:
                # Определяем faculty_id
                faculty_id = None
                if user['faculty_id']:
                    fac = db.execute_query(
                        "SELECT id FROM faculty WHERE id = %s",
                        (user['faculty_id'],), fetch=True
                    )
                    if fac:
                        faculty_id = fac[0][0]

                # Создаём user_profile
                db.execute_query("""
                    INSERT INTO user_profile (user_id, role, faculty_id)
                    VALUES (%s, %s, %s)
                """, (user_id, user['role'], faculty_id))
                profile_id = db.execute_query(
                    "SELECT id FROM user_profile WHERE user_id = %s",
                    (user_id,), fetch=True
                )[0][0]
                print(f"✅ Создан user_profile для {user['username']} (ID={profile_id})")
            else:
                profile_id = check_profile[0][0]
                print(f"⚠️ user_profile для {user['username']} уже существует (ID={profile_id})")

            # Для выпускников — создаём запись в graduate (если ещё не создана)
            if user['role'] == 'graduate':
                check_graduate = db.execute_query(
                    "SELECT id FROM graduate WHERE user_profile_id = %s",
                    (profile_id,), fetch=True
                )
                if not check_graduate:
                    db.execute_query("""
                        INSERT INTO graduate (user_profile_id, full_name, graduation_year, email)
                        VALUES (%s, %s, %s, %s)
                    """, (profile_id, "Выпускник Тестовый", 2024, None))
                    grad_id = db.execute_query(
                        "SELECT id FROM graduate WHERE user_profile_id = %s",
                        (profile_id,), fetch=True
                    )[0][0]
                    print(f"✅ Создан graduate для {user['username']} (ID={grad_id})")
                else:
                    print(f"⚠️ graduate для {user['username']} уже существует")

        print("✅ Инициализация базы данных завершена.")

    except Exception as e:
        print(f"❌ Ошибка инициализации: {e}")
    finally:
        db.disconnect()

if __name__ == "__main__":
    init_database()