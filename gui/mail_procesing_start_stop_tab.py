"""

Вкладка "Начать опрос почты"

"""
from PyQt6.QtWidgets import QVBoxLayout, QLabel, QPushButton, QTextEdit, QHBoxLayout
from base.base_tab import BaseTab

class StartStopEmailProcessingTab(BaseTab):
    """
    Класс для под-вкладки "Начать опрос почты" в "Обработке писем"
    """

    def __init__(self, controller):
        """
        Инициализация под-вкладки "Начать опрос почты"
        :param controller: Экземпляр контроллера MainController
        """
        super().__init__(controller)
        # Основной макет
        self.layout = QVBoxLayout()

        # Горизонтальный макет для кнопок Старт и Стоп
        # Горизонтальный макет для метки, комбобокса и кнопок
        self.horizontal_layout = QHBoxLayout()

        self.start_button = QPushButton(self.tr("Start"))
        self.horizontal_layout.addWidget(self.start_button)
        self.stop_button = QPushButton(self.tr("Stop"))
        self.horizontal_layout.addWidget(self.stop_button)
        # Добавление горизонтального макета в основной макет
        self.layout.addLayout(self.horizontal_layout)

        self.label = QLabel(self.tr("E-mail processing result"))
        self.text_edit = QTextEdit()
        # self.layout.addWidget(self.start_button)
        # self.layout.addWidget(self.stop_button)
        self.layout.addWidget(self.label)
        self.layout.addWidget(self.text_edit)
        self.setLayout(self.layout)

    def retranslate_ui(self):
        """
        Обновление текстов виджетов при смене языка
        """
        self.label.setText(self.tr("E-mail processing result"))
        self.start_button.setText(self.tr("Start"))
        self.stop_button.setText(self.tr("Stop"))
