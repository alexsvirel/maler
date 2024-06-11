from PyQt6.QtWidgets import QVBoxLayout, QLabel
from base.base_tab import BaseTab

class MailerHelpTab(BaseTab):
    """
    Класс для под-вкладки "Обучение" в "Справка"
    """

    def __init__(self, controller):
        """
        Инициализация под-вкладки "Обучение"
        :param controller: Экземпляр контроллера MainController
        """
        super().__init__(controller)
        self.layout = QVBoxLayout()
        self.label = QLabel(self.tr("Training Help Content"))
        self.layout.addWidget(self.label)
        self.setLayout(self.layout)

    def retranslate_ui(self):
        """
        Обновление текстов виджетов при смене языка
        """
        self.label.setText(self.tr("Training Help Content"))
