import sys
from PyQt6.QtWidgets import QApplication, QMainWindow, QTabWidget
from PyQt6.QtCore import QSettings, QLocale

from gui.settings_general import GeneralSettingsTab
from gui.settings_mailer_Install import MailerSettingsInitialTab
from gui.settings_email_boxes import MailerSettingsEmailBoxesTab
from gui.settings_goods import MailerSettingsGoodsTab
from gui.settings_outgoing_msgs import MailerSettingsOutgoingMsgsTab
from gui.help_general import GeneralHelpTab
from gui.help_mailer import MailerHelpTab
from gui.incoming_mail_tab import IncomingMailTab
from gui.outgoing_mail_tab import OutgoingMailTab
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

        self.incoming_mail_tab = IncomingMailTab(self.controller)
        self.mail_processing.addTab(self.incoming_mail_tab, self.tr("Incoming Mail"))

        self.outgoing_mail_tab = OutgoingMailTab(self.controller)
        self.mail_processing.addTab(self.outgoing_mail_tab, self.tr("Outgoing Mail"))

        # Вкладка "Настройки"
        self.tab_settings = QTabWidget()
        self.tabs.addTab(self.tab_settings, self.tr("Settings"))

        self.tab_settings_general = GeneralSettingsTab(self.controller)
        self.tab_settings.addTab(self.tab_settings_general, self.tr("General"))

        self.tab_settings_initial = MailerSettingsInitialTab(self.controller)
        self.tab_settings.addTab(self.tab_settings_initial, self.tr("Initial"))

        self.tab_settings_emailboxes = MailerSettingsEmailBoxesTab(self.controller)
        self.tab_settings.addTab(self.tab_settings_emailboxes, self.tr("E-mail Boxes"))

        self.tab_settings_goods = MailerSettingsGoodsTab(self.controller)
        self.tab_settings.addTab(self.tab_settings_goods, self.tr("Goods"))

        self.tab_settings_outgoinmsgs = MailerSettingsOutgoingMsgsTab(self.controller)
        self.tab_settings.addTab(self.tab_settings_outgoinmsgs, self.tr("Outgoin Msgs"))

        # Вкладка "Справка"
        self.tab_help = QTabWidget()
        self.tabs.addTab(self.tab_help, self.tr("Help"))

        self.tab_help_general = GeneralHelpTab(self.controller)
        self.tab_help.addTab(self.tab_help_general, self.tr("General"))

        self.tab_help_training = MailerHelpTab(self.controller)
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
        self.tab_settings.setTabText(self.tab_settings.indexOf(self.tab_settings_initial), self.tr("Initial"))
        self.tab_settings.setTabText(self.tab_settings.indexOf(self.tab_settings_emailboxes), self.tr("E-mail Boxes"))
        self.tab_settings.setTabText(self.tab_settings.indexOf(self.tab_settings_goods), self.tr("Goods"))
        self.tab_settings.setTabText(self.tab_settings.indexOf(self.tab_settings_outgoinmsgs), self.tr("Outgoin Msgs"))

        self.tabs.setTabText(self.tabs.indexOf(self.tab_help), self.tr("Help"))
        self.tab_help.setTabText(self.tab_help.indexOf(self.tab_help_general), self.tr("General"))
        self.tab_help.setTabText(self.tab_help.indexOf(self.tab_help_training), self.tr("Mailer"))

        # Обновление текстов на всех вкладках
        for tab in [self.incoming_mail_tab, self.outgoing_mail_tab, self.tab_settings_general,
                    self.tab_settings_initial, self.tab_settings_emailboxes, self.tab_settings_goods,
                    self.tab_settings_outgoinmsgs, self.tab_help_general, self.tab_help_training]:
            tab.retranslate_ui()

    def update_font_size(self):
        """
        Обновление размера шрифта для всех виджетов в главном окне
        """
        font = self.font()
        font.setPointSize(self.controller.get_font_size())
        self.setFont(font)
        # Обновить размер шрифта для всех вкладок
        for tab in [self.incoming_mail_tab, self.outgoing_mail_tab, self.tab_settings_general,
                    self.tab_settings_initial, self.tab_settings_emailboxes, self.tab_settings_goods,
                    self.tab_settings_outgoinmsgs, self.tab_help_general, self.tab_help_training]:
            tab.update_font_size()

    def update_style(self):
        """
        Обновление стиля для всех виджетов в главном окне
        """
        style = self.controller.get_style()
        self.setStyleSheet(style)
        # Обновить стиль для всех вкладок
        for tab in [self.incoming_mail_tab, self.outgoing_mail_tab, self.tab_settings_general,
                    self.tab_settings_initial, self.tab_settings_emailboxes, self.tab_settings_goods,
                    self.tab_settings_outgoinmsgs, self.tab_help_general, self.tab_help_training]:
            tab.update_style()


