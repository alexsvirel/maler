from PyQt6.QtWidgets import QWidget
from PyQt6.QtCore import pyqtSlot

class BaseTab(QWidget):
    """
    Базовый класс для всех вкладок, обрабатывающий изменения общих параметров
    """

    def __init__(self, controller):
        """
        Инициализация базового класса вкладки
        :param controller: Экземпляр контроллера MainController
        """
        super().__init__()
        self.controller = controller
        self.controller.language_changed.connect(self.retranslate_ui)
        self.controller.font_size_changed.connect(self.update_font_size)
        self.controller.style_changed.connect(self.update_style)

    @pyqtSlot()
    def retranslate_ui(self):
        """
        Обновление текстов виджетов при смене языка
        """
        raise NotImplementedError("Этот метод должен быть переопределен в дочернем классе")

    @pyqtSlot()
    def update_font_size(self):
        """
        Обновление размера шрифта виджетов
        """
        font = self.font()
        font.setPointSize(self.controller.get_font_size())
        self.setFont(font)
        # Обновить размер шрифта для всех дочерних виджетов
        for widget in self.findChildren(QWidget):
            widget.setFont(font)

    @pyqtSlot()
    def update_style(self):
        """
        Обновление стиля виджетов
        """
        style = self.controller.get_style()
        self.setStyleSheet(style)
        # Обновить стиль для всех дочерних виджетов
        for widget in self.findChildren(QWidget):
            widget.setStyleSheet(style)
