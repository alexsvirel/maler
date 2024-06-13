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