import sys

from PyQt6.QtCore import QSettings, QLocale
from PyQt6.QtWidgets import QApplication

from controllers.main_controller import MainController
from gui.main_window import MainWindow


def main():
    app = QApplication(sys.argv)

    settings = QSettings("MyCompany", "MyApp")
    language_code = settings.value("language", QLocale.system().name())
    controller = MainController(app, language_code)

    window = MainWindow(controller)
    controller.set_main_window(window)

    window.show()
    sys.exit(app.exec())


if __name__ == "__main__":
    main()
