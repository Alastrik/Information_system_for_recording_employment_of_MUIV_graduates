-- database_schema.sql
-- Схема базы данных для информационной системы учёта трудоустройства выпускников МУИВ
-- Автор: Монахов Артем Сергеевич

-- Факультеты
CREATE TABLE faculty (
    id SERIAL PRIMARY KEY,
    name VARCHAR(255) NOT NULL UNIQUE
);
COMMENT ON TABLE faculty IS 'Справочник факультетов МУИВ';
COMMENT ON COLUMN faculty.name IS 'Название факультета';

-- Отрасли экономики
CREATE TABLE industry (
    id SERIAL PRIMARY KEY,
    name VARCHAR(255) NOT NULL UNIQUE
);
COMMENT ON TABLE industry IS 'Справочник отраслей';
COMMENT ON COLUMN industry.name IS 'Название отрасли';

-- Должности
CREATE TABLE position (
    id SERIAL PRIMARY KEY,
    title VARCHAR(255) NOT NULL
);
COMMENT ON TABLE position IS 'Справочник должностей';
COMMENT ON COLUMN position.title IS 'Наименование должности';

-- Статусы трудоустройства
CREATE TABLE employment_status (
    id SERIAL PRIMARY KEY,
    status_name VARCHAR(100) NOT NULL UNIQUE
);
COMMENT ON TABLE employment_status IS 'Статусы трудоустройства (работает, уволен, ищет и т.д.)';
COMMENT ON COLUMN employment_status.status_name IS 'Название статуса';

-- Компании
CREATE TABLE company (
    id SERIAL PRIMARY KEY,
    name VARCHAR(255) NOT NULL,
    industry_id INTEGER NOT NULL REFERENCES industry(id) ON DELETE RESTRICT
);
COMMENT ON TABLE company IS 'Организации-работодатели';
COMMENT ON COLUMN company.name IS 'Полное наименование организации';

-- Пользователи (авторизация)
CREATE TABLE auth_user (
    id SERIAL PRIMARY KEY,
    username VARCHAR(150) UNIQUE NOT NULL,
    password VARCHAR(128) NOT NULL,
    is_active BOOLEAN DEFAULT TRUE NOT NULL
);
COMMENT ON TABLE auth_user IS 'Учётные записи пользователей системы';
CREATE INDEX idx_auth_user_username ON auth_user(username);

-- Профили пользователей (связь с ролью и факультетом)
CREATE TABLE user_profile (
    id SERIAL PRIMARY KEY,
    user_id INTEGER NOT NULL REFERENCES auth_user(id) ON DELETE CASCADE,
    role VARCHAR(50) NOT NULL CHECK (role IN ('admin', 'manager', 'graduate')),
    faculty_id INTEGER REFERENCES faculty(id) ON DELETE SET NULL
);
COMMENT ON TABLE user_profile IS 'Профили пользователей с ролями и привязкой к факультету';
CREATE UNIQUE INDEX idx_user_profile_user_id ON user_profile(user_id);

-- Выпускники
CREATE TABLE graduate (
    id SERIAL PRIMARY KEY,
    user_profile_id INTEGER NOT NULL REFERENCES user_profile(id) ON DELETE CASCADE,
    full_name VARCHAR(255) NOT NULL,
    graduation_year INTEGER NOT NULL CHECK (graduation_year > 1990 AND graduation_year <= EXTRACT(YEAR FROM CURRENT_DATE)),
    email VARCHAR(255) CHECK (email ~* '^[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Za-z]{2,}$')
);
COMMENT ON TABLE graduate IS 'Информация о выпускниках МУИВ';
CREATE INDEX idx_graduate_graduation_year ON graduate(graduation_year);

-- Данные о трудоустройстве
CREATE TABLE employment (
    id SERIAL PRIMARY KEY,
    graduate_id INTEGER NOT NULL REFERENCES graduate(id) ON DELETE CASCADE,
    company_id INTEGER REFERENCES company(id) ON DELETE SET NULL,
    position_id INTEGER REFERENCES position(id) ON DELETE SET NULL,
    status_id INTEGER NOT NULL REFERENCES employment_status(id) ON DELETE RESTRICT,
    start_date DATE,
    salary NUMERIC(10,2) CHECK (salary >= 0),
    is_current BOOLEAN DEFAULT TRUE NOT NULL,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP NOT NULL
);
COMMENT ON TABLE employment IS 'Информация о трудоустройстве выпускников';

-- Отчёты
CREATE TABLE report (
    id SERIAL PRIMARY KEY,
    title VARCHAR(255) NOT NULL,
    generated_by INTEGER NOT NULL REFERENCES auth_user(id) ON DELETE RESTRICT,
    generated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP NOT NULL,
    filters JSONB
);
COMMENT ON TABLE report IS 'Журнал сгенерированных отчётов';

-- Документы (сканы договоров и т.п.)
CREATE TABLE document (
    id SERIAL PRIMARY KEY,
    employment_id INTEGER NOT NULL REFERENCES employment(id) ON DELETE CASCADE,
    file_path VARCHAR(500) NOT NULL,
    uploaded_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP NOT NULL
);
COMMENT ON TABLE document IS 'Пути к загруженным документам';

-- Системный журнал
CREATE TABLE system_log (
    id SERIAL PRIMARY KEY,
    user_id INTEGER REFERENCES auth_user(id) ON DELETE SET NULL,
    action VARCHAR(255) NOT null,
    timestamp TIMESTAMP DEFAULT CURRENT_TIMESTAMP NOT NULL,
    details TEXT
);
CREATE UNIQUE INDEX idx_graduate_email_unique
ON graduate (email)
WHERE email IS NOT NULL;
COMMENT ON TABLE system_log IS 'Лог действий пользователей в системе';
CREATE INDEX idx_system_log_user ON system_log(user_id);
CREATE INDEX idx_system_log_timestamp ON system_log(timestamp);
INSERT INTO faculty (name) VALUES ('Информационных технологий'), ('Экономики и управления');
INSERT INTO industry (name) VALUES ('IT'), ('Финансы'), ('Другое');
INSERT INTO employment_status (status_name) VALUES ('Работает'), ('Уволен'), ('Ищет работу');
INSERT INTO position (title) VALUES ('Программист'), ('Аналитик');