"""
Создание и другие утилиты для работы с базой данных Почтовика
:create_database(db_name)
"""
import sqlite3


def add_template_to_db(id, template_name):
    """
    Добавление нового шаблона в таблицу MSG_TEMPLATES
    :param template_name: Название шаблона
    """
    connection = sqlite3.connect('bd_mailer.db')
    cursor = connection.cursor()
    cursor.execute('''INSERT INTO MSG_TEMPLATES (ID, NAME) VALUES (?, ?)''', (id, template_name,))
    connection.commit()
    connection.close()

def get_template_id():
    """
    Получение списка названий шаблонов из таблицы MSG_TEMPLATES
    :return: Список названий шаблонов
    """
    connection = sqlite3.connect('bd_mailer.db')
    cursor = connection.cursor()
    cursor.execute('''SELECT ID FROM MSG_TEMPLATES''')
    ids = cursor.fetchall()
    connection.close()
    return [id[0] for id in ids]


def get_template_names():
    """
    Получение списка названий шаблонов из таблицы MSG_TEMPLATES
    :return: Список названий шаблонов
    """
    connection = sqlite3.connect('bd_mailer.db')
    cursor = connection.cursor()
    cursor.execute('''SELECT NAME FROM MSG_TEMPLATES''')
    templates = cursor.fetchall()
    connection.close()
    return [template[0] for template in templates]


def get_template_details(template_name):
    """
    Получение данных шаблона из таблицы MSG_TEMPLATES
    :param template_name: Название шаблона


    :return: Кортеж с данными шаблона (SENDER, SUBJECT, DATA)
    """
    connection = sqlite3.connect('bd_mailer.db')
    cursor = connection.cursor()
    cursor.execute('''SELECT SENDER, SUBJECT, DATA FROM MSG_TEMPLATES WHERE NAME = ?''', (template_name,))
    template_details = cursor.fetchone()
    connection.close()
    return template_details


def update_template_in_db(template_name, sender, subject, content):
    """
    Обновление данных шаблона в таблице MSG_TEMPLATES
    :param template_name: Название шаблона
    :param sender: Отправитель
    :param subject: Заголовок
    :param content: Содержимое
    """
    connection = sqlite3.connect('bd_mailer.db')
    cursor = connection.cursor()
    cursor.execute('''UPDATE MSG_TEMPLATES
                      SET SENDER = ?, SUBJECT = ?, DATA = ?
                      WHERE NAME = ?''', (sender, subject, content, template_name))
    connection.commit()
    connection.close()


def remove_template_from_db(template_name):
    """
    Удаление шаблона из таблицы MSG_TEMPLATES
    :param template_name: Название шаблона
    """
    connection = sqlite3.connect('bd_mailer.db')
    cursor = connection.cursor()
    cursor.execute('''DELETE FROM MSG_TEMPLATES WHERE NAME = ?''', (template_name,))
    connection.commit()
    connection.close()
