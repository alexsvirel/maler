"""
Создание и другие утилиты для работы с базой данных Почтовика
:create_database(db_name)
"""
import sqlite3

def create_database(db_name):
    """
    Создание базы данных Почтовика
    :param db_name: Имя файла базы данных
    """
    connection = sqlite3.connect(db_name)
    cursor = connection.cursor()

    # Создание таблицы BILLS
    cursor.execute('''CREATE TABLE IF NOT EXISTS BILLS (
                    ID INTEGER PRIMARY KEY,
                    DATETIME TEXT,
                    BILL_NUM TEXT,
                    ITEM TEXT,
                    MSG_COUNT INTEGER,
                    RECIPIENT_NAME TEXT,
                    RECIPIENT_EMAIL TEXT,
                    LAST_DATETIME TEXT,
                    PAYMENT_LINK TEXT)''')

    # Создание таблицы EMAILS
    cursor.execute('''CREATE TABLE IF NOT EXISTS EMAILS (
                    ID INTEGER PRIMARY KEY,
                    SENDER TEXT,
                    TOKEN TEXT)''')

    # Создание таблицы GOODS
    cursor.execute('''CREATE TABLE IF NOT EXISTS GOODS (
                    ID INTEGER PRIMARY KEY,
                    ITEM TEXT,
                    SENDER TEXT,
                    PERIOD TEXT,
                    APP_NAME TEXT,
                    APP_MODE TEXT,
                    APP_LVL TEXT,
                    ITEM_LINK TEXT,
                    MANUAL_LINK TEXT,
                    MSG_TEMPLATE_ID INTEGER,
                    USE_MAILING INTEGER,
                    PERIODS INTEGER)''')

    # Создание таблицы LOG
    cursor.execute('''CREATE TABLE IF NOT EXISTS LOG (
                    ID INTEGER PRIMARY KEY,
                    DATETIME TEXT,
                    CONTENT TEXT)''')

    # Создание таблицы MSG_TEMPLATES
    cursor.execute('''CREATE TABLE IF NOT EXISTS MSG_TEMPLATES (
                    ID INTEGER PRIMARY KEY,
                    NAME TEXT,
                    SENDER TEXT,
                    SUBJECT TEXT,
                    DATA TEXT)''')

    # Создание таблицы SEND_GOODS
    cursor.execute('''CREATE TABLE IF NOT EXISTS SEND_GOODS (
                    ID INTEGER PRIMARY KEY,
                    DATETIME TEXT,
                    SENDER TEXT,
                    RECIPIENT_NAME TEXT,
                    RECIPIENT_EMAIL TEXT,
                    ITEM TEXT,
                    SERVICE TEXT,
                    CODE TEXT,
                    VALID_TO TEXT)''')

    connection.commit()
    connection.close()

def add_template_to_db(template_name):
    """
    Добавление нового шаблона в таблицу MSG_TEMPLATES
    :param template_name: Название шаблона
    """
    connection = sqlite3.connect('bd_mailer.db')
    cursor = connection.cursor()
    cursor.execute('''INSERT INTO MSG_TEMPLATES (NAME) VALUES (?)''', (template_name,))
    connection.commit()
    connection.close()

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
