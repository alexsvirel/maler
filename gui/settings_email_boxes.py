from PyQt6.QtWidgets import QVBoxLayout, QLabel, QPushButton
from base.base_tab import BaseTab

class MailerSettingsEmailBoxesTab(BaseTab):
    """
    Класс для под-вкладки "Обучение" в "Настройки"
    """

    def __init__(self, controller):
        """
        Инициализация под-вкладки "Обучение"
        :param controller: Экземпляр контроллера MainController
        """
        super().__init__(controller)
        self.layout = QVBoxLayout()
        self.label = QLabel(self.tr("E-mail Boxes Content"))
        self.layout.addWidget(self.label)

        self.button = QPushButton(self.tr("E-mail Boxes button"))
        self.layout.addWidget(self.button)

        self.setLayout(self.layout)

    def retranslate_ui(self):
        """
        Обновление текстов виджетов при смене языка
        """
        self.label.setText(self.tr("E-mail Boxes Content"))
        self.button.setText(self.tr("E-mail Boxes button"))
