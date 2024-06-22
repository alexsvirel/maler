from PyQt6.QtWidgets import (QVBoxLayout, QHBoxLayout, QLabel, QComboBox,
                             QPushButton, QLineEdit, QTextEdit, QDialog,
                             QDialogButtonBox, QMessageBox)
from base.base_tab import BaseTab
from utils.db_settings_outgoing_msgs import (add_template_to_db, get_template_names,
                                             get_template_details, update_template_in_db,
                                             remove_template_from_db, get_template_id)


class MailerSettingsOutgoingMsgsTab(BaseTab):
    """
    Класс для под-вкладки "Исходящие сообщения" в "Настройки"
    """

    def __init__(self, controller):
        """
        Инициализация под-вкладки "Исходящие сообщения"
        :param controller: Экземпляр контроллера MainController
        """
        super().__init__(controller)

        # Основной макет
        self.layout = QVBoxLayout()

        # Горизонтальный макет для метки, комбобокса и кнопок
        self.horizontal_layout = QHBoxLayout()

        # Метка "Template"
        self.label = QLabel(self.tr("Template"))
        self.horizontal_layout.addWidget(self.label)

        # Комбобокс для выбора шаблонов
        self.combo_box = QComboBox()
        self.update_combo_box()
        self.combo_box.currentIndexChanged.connect(self.load_template_details)
        self.horizontal_layout.addWidget(self.combo_box)

        # Кнопка "Добавить"
        self.add_button = QPushButton(self.tr("Add"))
        self.add_button.clicked.connect(self.open_add_template_dialog)
        self.horizontal_layout.addWidget(self.add_button)

        # Кнопка "Удалить"
        self.remove_button = QPushButton(self.tr("Remove"))
        self.remove_button.clicked.connect(self.remove_template)
        self.horizontal_layout.addWidget(self.remove_button)

        # Добавление горизонтального макета в основной макет
        self.layout.addLayout(self.horizontal_layout)

        # Текстовая строка "Sender"
        self.sender_label = QLabel(self.tr("Sender"))
        self.layout.addWidget(self.sender_label)

        # Текстовое поле для отправителя
        self.sender_edit = QLineEdit()
        self.layout.addWidget(self.sender_edit)

        # Текстовая строка "Subject"
        self.subject_label = QLabel(self.tr("Subject"))
        self.layout.addWidget(self.subject_label)

        # Текстовое поле для заголовка
        self.subject_edit = QLineEdit()
        self.layout.addWidget(self.subject_edit)

        # Многострочное текстовое поле "Content"
        self.content_label = QLabel(self.tr("Content"))
        self.layout.addWidget(self.content_label)

        self.content_edit = QTextEdit()
        self.layout.addWidget(self.content_edit)

        # Кнопка "Save"
        self.save_button = QPushButton(self.tr("Save"))
        self.save_button.clicked.connect(self.save_template)
        self.layout.addWidget(self.save_button)

        # Установка основного макета
        self.setLayout(self.layout)


    def update_combo_box(self):
        """
        Обновление содержимого комбобокса с шаблонами из базы данных
        """
        template_names = get_template_names()
        self.combo_box.clear()
        self.combo_box.addItems(template_names)

    def open_add_template_dialog(self):
        """
        Открытие диалогового окна для добавления нового шаблона
        """
        dialog = QDialog()
        dialog.setWindowTitle(self.tr("Add Template"))

        dialog_layout = QVBoxLayout()
        dialog.setLayout(dialog_layout)

        label = QLabel(self.tr("Enter template name:"))
        dialog_layout.addWidget(label)

        self.template_name_edit = QLineEdit()
        dialog_layout.addWidget(self.template_name_edit)

        button_box = QDialogButtonBox(QDialogButtonBox.StandardButton.Ok | QDialogButtonBox.StandardButton.Cancel)
        button_box.accepted.connect(lambda: self.add_template(dialog))
        button_box.rejected.connect(dialog.reject)
        dialog_layout.addWidget(button_box)

        dialog.exec()

    def add_template(self, dialog):
        """
        Добавление нового шаблона в базу данных
        :param dialog: Диалоговое окно для добавления шаблона
        """
        template_ids = get_template_id()
        new_id = max(template_ids) + 1
        template_name = self.template_name_edit.text()
        if template_name:
            add_template_to_db(new_id, template_name)
            self.update_combo_box()
            dialog.accept()

    def save_template(self):
        """
        Сохранение текущего шаблона в базу данных
        """
        template_name = self.combo_box.currentText()
        if template_name:
            sender = self.sender_edit.text()
            subject = self.subject_edit.text()
            content = self.content_edit.toPlainText()
            update_template_in_db(template_name, sender, subject, content)
            QMessageBox.warning(self, self.tr("Warning"), "Шаблон сохранен")
        else:
            self.show_no_template_dialog()

    def show_no_template_dialog(self):
        """
        Показ диалогового окна при попытке сохранения без выбранного шаблона
        """
        QMessageBox.warning(self, self.tr("Warning"), self.tr("Please add and select a template before saving."))

    def load_template_details(self):
        """
        Загрузка данных шаблона при выборе его из комбобокса
        """
        template_name = self.combo_box.currentText()
        if template_name:
            template_details = get_template_details(template_name)
            if template_details:
                self.sender_edit.setText(template_details[0])
                self.subject_edit.setText(template_details[1])
                self.content_edit.setText(template_details[2])
            else:
                self.sender_edit.clear()
                self.subject_edit.clear()
                self.content_edit.clear()

    def remove_template(self):
        """
        Удаление выбранного шаблона из базы данных
        """
        template_name = self.combo_box.currentText()
        if template_name:
            reply = QMessageBox.question(self, self.tr("Remove Template"),
                                         (self.tr("Do you want to remove the template ")+(f"\n'{template_name}'?")),
                                         QMessageBox.StandardButton.Yes | QMessageBox.StandardButton.No)
            if reply == QMessageBox.StandardButton.Yes:
                remove_template_from_db(template_name)
                self.update_combo_box()
                self.sender_edit.clear()
                self.subject_edit.clear()
                self.content_edit.clear()
        else:
            self.show_no_template_dialog()

    def retranslate_ui(self):
        """
        Обновление текстов виджетов при смене языка
        """
        self.label.setText(self.tr("Template"))
        self.add_button.setText(self.tr("Add"))
        self.remove_button.setText(self.tr("Remove"))
        self.sender_label.setText(self.tr("Sender"))
        self.subject_label.setText(self.tr("Subject"))
        self.content_label.setText(self.tr("Content"))
        self.save_button.setText(self.tr("Save"))