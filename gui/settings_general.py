from PyQt6.QtWidgets import QVBoxLayout, QLabel, QComboBox, QSlider
from PyQt6.QtCore import QLocale, Qt
from base.base_tab import BaseTab

class GeneralSettingsTab(BaseTab):
    """
    Класс для под-вкладки "Общие" в "Настройки"
    """

    def __init__(self, controller):
        """
        Инициализация под-вкладки "Общие"
        :param controller: Экземпляр контроллера MainController
        """
        super().__init__(controller)
        self.layout = QVBoxLayout()
        self.label = QLabel(self.tr("General Settings Content"))
        self.layout.addWidget(self.label)

        # Элементы для выбора языка
        self.language_label = QLabel(self.tr("Select Language"))
        self.layout.addWidget(self.language_label)

        self.language_combobox = QComboBox()
        self.language_combobox.addItems([self.tr("English"), self.tr("Spanish"), self.tr("Russian")])
        self.language_combobox.setCurrentIndex(self.get_current_language_index())
        self.language_combobox.currentIndexChanged.connect(self.on_language_changed)
        self.layout.addWidget(self.language_combobox)

        # Элементы для изменения размера шрифта
        self.font_size_label = QLabel(self.tr("Font Size Setting"))
        self.layout.addWidget(self.font_size_label)

        self.font_size_slider = QSlider(Qt.Orientation.Horizontal)
        self.font_size_slider.setRange(8, 32)
        self.font_size_slider.setValue(self.get_current_font_size())
        self.font_size_slider.valueChanged.connect(self.on_font_size_changed)
        self.layout.addWidget(self.font_size_slider)

        # Элементы для выбора стиля
        self.style_label = QLabel(self.tr("Select Style"))
        self.layout.addWidget(self.style_label)

        self.style_combobox = QComboBox()
        self.style_combobox.addItems([self.tr("Classic"), self.tr("Blue"), self.tr("Green")])
        self.style_combobox.setCurrentIndex(self.get_current_style_index())
        self.style_combobox.currentIndexChanged.connect(self.on_style_changed)
        self.layout.addWidget(self.style_combobox)

        self.setLayout(self.layout)

    def get_current_language_index(self):
        """
        Получение индекса текущего выбранного языка
        :return: Индекс выбранного языка
        """
        language_code = self.controller.settings.value("language", QLocale.system().name())
        return {
            "en": 0,  # English
            "es": 1,  # Spanish
            "ru": 2   # Russian
        }.get(language_code, 0)

    def get_current_font_size(self):
        """
        Получение текущего размера шрифта
        :return: Размер шрифта
        """
        return int(self.controller.settings.value("font_size", 12))

    def get_current_style_index(self):
        """
        Получение индекса текущего выбранного стиля
        :return: Индекс выбранного стиля
        """
        style = self.controller.settings.value("style", "classic")
        return {
            "classic": 0,
            "blue": 1,
            "green": 2
        }.get(style, 0)

    def on_language_changed(self, index):
        """
        Обработчик изменения языка
        :param index: Индекс выбранного языка
        """
        language_code = {
            0: "en",  # English
            1: "es",  # Spanish
            2: "ru"   # Russian
        }.get(index, "en")
        self.controller.change_language(language_code)

    def on_font_size_changed(self, value):
        """
        Обработчик изменения размера шрифта
        :param value: Новый размер шрифта
        """
        self.controller.change_font_size(value)

    def on_style_changed(self, index):
        """
        Обработчик изменения стиля
        :param index: Индекс выбранного стиля
        """
        style = {
            0: "classic",
            1: "blue",
            2: "green"
        }.get(index, "classic")
        self.controller.change_style(style)

    def retranslate_ui(self):
        """
        Обновление текстов виджетов при смене языка
        """
        self.label.setText(self.tr("General Settings Content"))
        self.language_label.setText(self.tr("Select Language"))
        self.language_combobox.setItemText(0, self.tr("English"))
        self.language_combobox.setItemText(1, self.tr("Spanish"))
        self.language_combobox.setItemText(2, self.tr("Russian"))
        self.font_size_label.setText(self.tr("Font Size Setting"))
        self.style_label.setText(self.tr("Select Style"))
        self.style_combobox.setItemText(0, self.tr("Classic"))
        self.style_combobox.setItemText(1, self.tr("Blue"))
        self.style_combobox.setItemText(2, self.tr("Green"))
