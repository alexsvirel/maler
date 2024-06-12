import sys
from PyQt6.QtWidgets import QApplication, QMainWindow, QTabWidget, QWidget, QVBoxLayout

class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()

        self.setWindowTitle("Главное окно с вкладками")

        main_widget = QWidget()
        main_layout = QVBoxLayout()

        self.tabs = QTabWidget()
        self.tab1 = QWidget()
        self.tab2 = QWidget()
        self.tab3 = QWidget()

        self.tabs.addTab(self.tab1, "Один")
        self.tabs.addTab(self.tab2, "Два")
        self.tabs.addTab(self.tab3, "Три")

        self.tab1_sub_tabs = QTabWidget()
        self.tab2_sub_tabs = QTabWidget()
        self.tab3_sub_tabs = QTabWidget()

        self.tab1_red = QWidget()
        self.tab1_blue = QWidget()
        self.tab1_green = QWidget()

        self.tab1_sub_tabs.addTab(self.tab1_red, "Один Красный")
        self.tab1_sub_tabs.addTab(self.tab1_blue, "Один Синий")
        self.tab1_sub_tabs.addTab(self.tab1_green, "Один Зеленый")

        self.tab2_red = QWidget()
        self.tab2_blue = QTabWidget()  # Изменено на QTabWidget
        self.tab2_green = QWidget()

        self.tab2_sub_tabs.addTab(self.tab2_red, "Два Красный")
        self.tab2_sub_tabs.addTab(self.tab2_blue, "Два Синий")
        self.tab2_sub_tabs.addTab(self.tab2_green, "Два Зеленый")

        self.tab2_light_blue = QWidget()
        self.tab2_dark_blue = QWidget()

        self.tab2_blue.addTab(self.tab2_light_blue, "Два Синий Голубой")
        self.tab2_blue.addTab(self.tab2_dark_blue, "Два Синий Темно-синий")

        self.tab3_red = QWidget()
        self.tab3_blue = QWidget()
        self.tab3_green = QWidget()

        self.tab3_sub_tabs.addTab(self.tab3_red, "Три Красный")
        self.tab3_sub_tabs.addTab(self.tab3_blue, "Три Синий")
        self.tab3_sub_tabs.addTab(self.tab3_green, "Три Зеленый")

        self.tab1_layout = QVBoxLayout(self.tab1)
        self.tab2_layout = QVBoxLayout(self.tab2)
        self.tab3_layout = QVBoxLayout(self.tab3)

        self.tab1_layout.addWidget(self.tab1_sub_tabs)
        self.tab2_layout.addWidget(self.tab2_sub_tabs)
        self.tab3_layout.addWidget(self.tab3_sub_tabs)

        main_layout.addWidget(self.tabs)
        main_widget.setLayout(main_layout)
        self.setCentralWidget(main_widget)


if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = MainWindow()
    window.resize(600, 400)
    window.show()
    sys.exit(app.exec())