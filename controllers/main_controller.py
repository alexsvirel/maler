import os

from PyQt6.QtCore import QTranslator, QLocale, QSettings, pyqtSignal, QObject

class MainController(QObject):
    """
    Класс контроллера для управления главным окном и переводами
    """
    language_changed = pyqtSignal()
    font_size_changed = pyqtSignal()
    style_changed = pyqtSignal()

    def __init__(self, app, language_code):
        """
        Инициализация контроллера
        :param app: Экземпляр QApplication
        :param language_code: Код языка для загрузки при инициализации
        """
        super().__init__()
        self.app = app
        self.translator = QTranslator()
        self.main_window = None
        self.settings = QSettings("MyCompany", "MyApp")
        self.change_language(language_code, save=False)
        self.font_size = int(self.settings.value("font_size", 12))
        self.style = self.settings.value("style", "classic") # для отладки
        self.apply_font_size()
        self.apply_style()

    def set_main_window(self, window):
        """
        Установка главного окна
        :param window: Экземпляр QMainWindow
        """
        self.main_window = window

    def change_language(self, language_code, save=True):
        """
        Метод для смены языка интерфейса
        :param language_code: Код языка (например, 'en', 'es', 'ru')
        :param save: Флаг, указывающий, нужно ли сохранять выбор языка
        """
        if self.translator.load(f"translations/translations_{language_code}.qm"):
            self.app.installTranslator(self.translator)
            if self.main_window:
                self.main_window.retranslate_ui()
            self.language_changed.emit()
            if save:
                self.settings.setValue("language", language_code)

    def change_font_size(self, size):
        """
        Метод для изменения размера шрифта интерфейса
        :param size: Новый размер шрифта
        """
        self.font_size = size
        if self.main_window:
            self.main_window.update_font_size()
        self.font_size_changed.emit()
        self.settings.setValue("font_size", size)

    def get_font_size(self):
        """
        Получение текущего размера шрифта
        :return: Размер шрифта
        """
        return self.font_size

    def change_style(self, style):
        """
        Метод для изменения стиля интерфейса
        :param style: Новый стиль
        """
        self.style = style
        if self.main_window:
            self.main_window.update_style()
        self.style_changed.emit()
        self.settings.setValue("style", style)     # для отладки

    def get_style(self):
        """
        Получение текущего стиля
        :return: Стиль
        """
        style_file = f"styles/{self.style}.qss"
        if os.path.isfile(style_file):
            with open(style_file, "r") as f:
                return f.read()
        else:
            return ""

    def apply_font_size(self):
        """
        Применение текущего размера шрифта ко всему приложению
        """
        font = self.app.font()
        font.setPointSize(self.font_size)
        self.app.setFont(font)

    def apply_style(self):
        """
        Применение текущего стиля ко всему приложению
        """
        style = self.get_style()
        self.app.setStyleSheet(style)
