# Точка входа в приложение
# Запускает главное окно — окно авторизации

from ui.login_window import LoginWindow
import tkinter as tk

if __name__ == "__main__":
    # Создаём главное окно Tkinter
    root = tk.Tk()
    # Инициализируем и открываем окно входа
    app = LoginWindow(root)
    # Запускаем главный цикл обработки событий
    root.mainloop()