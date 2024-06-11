"""
Вкладка "Исходящее письмо" при ручной обработке писем
"""
from PyQt6.QtWidgets import QVBoxLayout, QLabel, QPushButton, QTextEdit
from base.base_tab import BaseTab

class OutgoingMailTab(BaseTab):
    """
    Класс для под-вкладки "Исходящее письмо" в "Обработке писем"
    """

    def __init__(self, controller):
        """
        Инициализация под-вкладки "Исходящее письмо"
        :param controller: Экземпляр контроллера MainController
        """
        super().__init__(controller)
        self.layout = QVBoxLayout()
        self.label = QLabel(self.tr("Outgoing Mail Content"))
        self.text_edit = QTextEdit()
        self.button = QPushButton()
        self.layout.addWidget(self.label)
        self.layout.addWidget(self.text_edit)
        self.setLayout(self.layout)

    def retranslate_ui(self):
        """
        Обновление текстов виджетов при смене языка
        """
        self.label.setText(self.tr("Outgoing Mail Content"))
