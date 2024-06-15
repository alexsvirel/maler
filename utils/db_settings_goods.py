import sqlite3
import json

def get_goods():
    """
    Получение списка товаров из базы данных
    :return: Список товаров
    """
    connection = sqlite3.connect('bd_mailer.db')
    cursor = connection.cursor()
    cursor.execute(
        '''SELECT ID, ITEM, SENDER, APP_NAME, APP_MODE, APP_LVL, PERIOD, ITEM_LINK, MANUAL_LINK, MSG_TEMPLATE_ID, USE_MAILING, PERIODS FROM GOODS''')
    goods = cursor.fetchall()
    connection.close()
    return [{'id': good[0], 'item': good[1], 'sender': good[2], 'app_name': good[3], 'app_mode': good[4],
             'app_lvl': good[5], 'period': good[6], 'item_link':

 good[7], 'manual_link': good[8],
             'msg_template_id': good[9], 'use_mailing': bool(good[10]), 'periods': json.loads(good[11]) if good[11] else {}} for good in goods]

def get_template_names():
    """
    Получение списка названий шаблонов из таблицы MSG_TEMPLATES
    :return: Список названий шаблонов
    """
    connection = sqlite3.connect('bd_mailer.db')
    cursor = connection.cursor()
    cursor.execute('''SELECT ID, NAME FROM MSG_TEMPLATES''')
    templates = cursor.fetchall()
    connection.close()
    return [{'id': template[0], 'name': template[1]} for template in templates]

def save_good(good):
    """
    Сохранение товара в базу данных
    :param good: Словарь с данными товара
    """
    connection = sqlite3.connect('bd_mailer.db')
    cursor = connection.cursor()
    # Проверяем, существует ли в таблице GOODS товар с полученным ID
    cursor.execute("SELECT COUNT(*) FROM GOODS WHERE id = ?", (good['id'],))
    result = cursor.fetchone()

    # Преобразование словаря периодов в JSON-строку
    periods_json = json.dumps(good['periods'])

    if result[0] > 0:
        cursor.execute('''UPDATE GOODS
                          SET ITEM = ?, SENDER = ?, APP_NAME = ?, APP_MODE = ?, APP_LVL = ?, PERIOD = ?, ITEM_LINK = ?, MANUAL_LINK = ?, MSG_TEMPLATE_ID = ?, USE_MAILING = ?, PERIODS = ? WHERE ID = ?''',
                       (good['item'], good['sender'], good['app_name'], good['app_mode'], good['app_lvl'], good['period'], good['item_link'], good['manual_link'], good['msg_template_id'], int(good['use_mailing']), periods_json, good['id']))
    else:
        cursor.execute('''INSERT INTO GOODS (ID, ITEM, SENDER, APP_NAME, APP_MODE, APP_LVL, PERIOD, ITEM_LINK, MANUAL_LINK, MSG_TEMPLATE_ID, USE_MAILING, PERIODS)
                          VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)''',
                       (good['id'], good['item'], good['sender'], good['app_name'], good['app_mode'], good['app_lvl'], good['period'], good['item_link'], good['manual_link'], good['msg_template_id'], int(good['use_mailing']), periods_json))
    connection.commit()
    connection.close()

def delete_record_by_id(good):
    record_id = good['id']
    try:
        # Подключение к базе данных
        conn = sqlite3.connect('bd_mailer.db')
        cursor = conn.cursor()

        # SQL-запрос для удаления строки по ID
        sql_delete_query = f"DELETE FROM GOODS WHERE ID = {record_id};"

        # Выполнение SQL-запроса
        cursor.execute(sql_delete_query)
        conn.commit()

    except sqlite3.Error as error:
        print(f"Ошибка при удалении записи из таблицы GOODS: {error}")

    finally:
        if conn:
            conn.close()
