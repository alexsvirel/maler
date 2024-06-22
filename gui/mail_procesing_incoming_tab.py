"""

Вкладка "Входящее письмо" при ручной обработке писем

"""
from PyQt6.QtWidgets import QVBoxLayout, QLabel, QPushButton, QTextEdit
from base.base_tab import BaseTab

class IncomingMailTab(BaseTab):
    """
    Класс для под-вкладки "Входящее письмо" в "Обработке писем"
    """

    def __init__(self, controller):
        """
        Инициализация под-вкладки "Входящее письмо"
        :param controller: Экземпляр контроллера MainController
        """
        super().__init__(controller)
        self.layout = QVBoxLayout()
        self.label = QLabel(self.tr("Incoming Mail Content"))
        self.text_edit = QTextEdit()
        self.button = QPushButton(self.tr("Process"))
        self.layout.addWidget(self.label)
        self.layout.addWidget(self.text_edit)
        self.layout.addWidget(self.button)
        self.setLayout(self.layout)

    def retranslate_ui(self):
        """
        Обновление текстов виджетов при смене языка
        """
        self.label.setText(self.tr("Incoming Mail Content"))
        self.button.setText(self.tr("Process"))
