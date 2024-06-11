import sys
import os.path

from PyQt6.QtCore import QSettings, QLocale
from PyQt6.QtWidgets import QApplication

from controllers.main_controller import MainController
from gui.main_window import MainWindow
from utils.utils_db import create_database


def check_for_database_availability():
    """
    Проверка наличия базы данных. Если базы нет, то вызвать функцию для её создания
    :return:
    """
    db_name = "bd_mailer.db"
    if not os.path.exists(db_name):
        create_database(db_name)
    else:
        print('база данных была создана ранее и при этом запуске Почтовика не создавалась.')


def main():
    """
    Запуск главного окна Почтовика
    :return:
    """
    app = QApplication(sys.argv)

    settings = QSettings("MyCompany", "MyApp")
    language_code = settings.value("language", QLocale.system().name())
    controller = MainController(app, language_code)

    window = MainWindow(controller)
    controller.set_main_window(window)

    window.show()
    sys.exit(app.exec())


if __name__ == "__main__":
    check_for_database_availability()
    main()
