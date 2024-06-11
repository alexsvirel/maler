from PyQt6.QtWidgets import QVBoxLayout, QLabel
from base.base_tab import BaseTab

class GeneralHelpTab(BaseTab):
    """
    Класс для под-вкладки "Общие" в "Справка"
    """

    def __init__(self, controller):
        """
        Инициализация под-вкладки "Общие"
        :param controller: Экземпляр контроллера MainController
        """
        super().__init__(controller)
        self.layout = QVBoxLayout()
        self.label = QLabel(self.tr("General Help Content"))
        self.layout.addWidget(self.label)
        self.setLayout(self.layout)

    def retranslate_ui(self):
        """
        Обновление текстов виджетов при смене языка
        """
        self.label.setText(self.tr("General Help Content"))
