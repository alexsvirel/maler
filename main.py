import sys
from PyQt6.QtWidgets import QApplication, QMainWindow, QTabWidget
from PyQt6.QtCore import QSettings, QLocale

from settings.settings_general import GeneralSettingsTab
from settings.settings_mailer import TrainingSettingsTab
from help.help_general import GeneralHelpTab
from help.help_mailer import TrainingHelpTab
from mail_processing.incoming_mail_tab import TrainingTabOne
from mail_processing.outgoing_mail_tab import TrainingTabTwo
from controllers.main_controller import MainController


class MainWindow(QMainWindow):
    """
    Класс главного окна приложения "Почтовик"
    """

    def __init__(self, controller):
        """lin
        Инициализация главного окна
        """
        super().__init__()

        self.controller = controller

        # Установка заголовка окна
        self.setWindowTitle(self.tr("Mailer"))

        # Создание виджета для вкладок
        self.tabs = QTabWidget()
        self.setCentralWidget(self.tabs)

        # Создание и добавление вкладок
        self.create_tabs()

        # Применение размера шрифта и стиля после создания вкладок
        self.update_font_size()
        self.update_style()

        # Восстановление размера и положения окна
        self.restore_window_settings()

    def create_tabs(self):
        """
        Создание вкладок и добавление их в QTabWidget
        """

        # Вкладка "Обучение"
        self.mail_processing = QTabWidget()
        self.tabs.addTab(self.mail_processing, self.tr("Mail Processing"))

        self.incoming_mail_tab = TrainingTabOne(self.controller)
        self.mail_processing.addTab(self.incoming_mail_tab, self.tr("Incoming Mail"))

        self.outgoing_mail_tab = TrainingTabTwo(self.controller)
        self.mail_processing.addTab(self.outgoing_mail_tab, self.tr("Outgoing Mail"))

        # Вкладка "Настройки"
        self.tab_settings = QTabWidget()
        self.tabs.addTab(self.tab_settings, self.tr("Settings"))

        self.tab_settings_general = GeneralSettingsTab(self.controller)
        self.tab_settings.addTab(self.tab_settings_general, self.tr("General"))

        self.tab_settings_training = TrainingSettingsTab(self.controller)
        self.tab_settings.addTab(self.tab_settings_training, self.tr("Mailer"))

        # Вкладка "Справка"
        self.tab_help = QTabWidget()
        self.tabs.addTab(self.tab_help, self.tr("Help"))

        self.tab_help_general = GeneralHelpTab(self.controller)
        self.tab_help.addTab(self.tab_help_general, self.tr("General"))

        self.tab_help_training = TrainingHelpTab(self.controller)
        self.tab_help.addTab(self.tab_help_training, self.tr("Mailer"))

    def restore_window_settings(self):
        """
        Восстановление настроек окна
        """
        settings = self.controller.settings
        self.resize(settings.value("window_size", self.size()))
        self.move(settings.value("window_position", self.pos()))

    def closeEvent(self, event):
        """
        Обработчик события закрытия окна для сохранения настроек окна
        """
        self.save_window_settings()
        event.accept()

    def save_window_settings(self):
        """
        Сохранение настроек окна
        """
        settings = self.controller.settings
        settings.setValue("window_size", self.size())
        settings.setValue("window_position", self.pos())

    def retranslate_ui(self):
        """
        Метод для обновления текстов интерфейса при смене языка
        """
        self.setWindowTitle(self.tr("Mailer"))

        self.tabs.setTabText(self.tabs.indexOf(self.mail_processing), self.tr("Mail Processing"))

        self.mail_processing.setTabText(self.mail_processing.indexOf(self.incoming_mail_tab), self.tr("Incoming Mail"))
        self.mail_processing.setTabText(self.mail_processing.indexOf(self.outgoing_mail_tab), self.tr("Outgoing Mail"))

        self.tabs.setTabText(self.tabs.indexOf(self.tab_settings), self.tr("Settings"))
        self.tab_settings.setTabText(self.tab_settings.indexOf(self.tab_settings_general), self.tr("General"))
        self.tab_settings.setTabText(self.tab_settings.indexOf(self.tab_settings_training), self.tr("Mailer"))

        self.tabs.setTabText(self.tabs.indexOf(self.tab_help), self.tr("Help"))
        self.tab_help.setTabText(self.tab_help.indexOf(self.tab_help_general), self.tr("General"))
        self.tab_help.setTabText(self.tab_help.indexOf(self.tab_help_training), self.tr("Mailer"))

        # Обновление текстов на всех вкладках
        for tab in [self.incoming_mail_tab, self.outgoing_mail_tab,
                    self.tab_settings_general, self.tab_settings_training,
                    self.tab_help_general, self.tab_help_training]:
            tab.retranslate_ui()

    def update_font_size(self):
        """
        Обновление размера шрифта для всех виджетов в главном окне
        """
        font = self.font()
        font.setPointSize(self.controller.get_font_size())
        self.setFont(font)
        # Обновить размер шрифта для всех вкладок
        for tab in [self.incoming_mail_tab, self.outgoing_mail_tab,
                    self.tab_settings_general, self.tab_settings_training,
                    self.tab_help_general, self.tab_help_training]:
            tab.update_font_size()

    def update_style(self):
        """
        Обновление стиля для всех виджетов в главном окне
        """
        style = self.controller.get_style()
        self.setStyleSheet(style)
        # Обновить стиль для всех вкладок
        for tab in [self.incoming_mail_tab, self.outgoing_mail_tab,
                    self.tab_settings_general, self.tab_settings_training,
                    self.tab_help_general, self.tab_help_training]:
            tab.update_style()


if __name__ == "__main__":
    app = QApplication(sys.argv)

    settings = QSettings("MyCompany", "MyApp")
    language_code = settings.value("language", QLocale.system().name())

    controller = MainController(app, language_code)

    window = MainWindow(controller)
    controller.set_main_window(window)

    window.show()
    sys.exit(app.exec())