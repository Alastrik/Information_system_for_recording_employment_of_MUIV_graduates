# Диалоговое окно подтверждения

import tkinter as tk
from tkinter import messagebox

def show_confirmation(parent, title="Подтверждение", message="Вы уверены?"):
    """
    Показывает диалоговое окно подтверждения.
    Возвращает True, если пользователь нажал 'Да', иначе False.
    """
    result = messagebox.askyesno(title, message, parent=parent)
    return result