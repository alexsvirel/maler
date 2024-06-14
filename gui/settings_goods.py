from PyQt6.QtWidgets import (QVBoxLayout, QLabel, QPushButton, QScrollArea,
                             QFrame, QVBoxLayout, QHBoxLayout, QLineEdit,
                             QComboBox, QCheckBox, QDialog, QMessageBox)
from base.base_tab import BaseTab
from utils.db_settings_goods import get_goods, get_template_names, save_good, delete_record_by_id

class MailerSettingsGoodsTab(BaseTab):
    """
    Класс для под-вкладки "Товары" в "Настройки"
    """

    def __init__(self, controller):
        """
        Инициализация под-вкладки "Товары"
        :param controller: Экземпляр контроллера MainController
        """
        super().__init__(controller)
        self.layout = QVBoxLayout()
        self.label = QLabel(self.tr("Click on the product name to edit its properties"))
        self.layout.addWidget(self.label)

        self.scroll_area = QScrollArea()
        self.scroll_area.setWidgetResizable(True)
        self.scroll_content = QFrame()
        self.scroll_layout = QVBoxLayout(self.scroll_content)
        self.scroll_area.setWidget(self.scroll_content)
        self.layout.addWidget(self.scroll_area)

        self.add_button = QPushButton(self.tr("Add"))
        self.layout.addWidget(self.add_button)
        self.setLayout(self.layout)

        self.add_button.clicked.connect(lambda: self.show_add_dialog())

        self.load_goods()

    def load_goods(self):
        """
        Загрузка товаров из базы данных и отображение их в интерфейсе
        """
        self.goods = get_goods()
        for good in self.goods:
            good_label = QLabel(f"{good['id']}: {good['item']}")
            good_label.setStyleSheet("cursor: pointer;")
            self.scroll_layout.addWidget(good_label)
            good_label.mousePressEvent = lambda event, good=good: self.show_add_dialog(good)

    def show_add_dialog(self, good=None):
        """
        Показ всплывающего окна для добавления или редактирования товара
        :param good: Словарь с данными товара, если редактируется, иначе None
        """
        dialog = QDialog(self)
        dialog.setWindowTitle("Product Properties")

        layout = QVBoxLayout()

        # Создание полей для ввода данных
        item_label = QLabel("Product Name:")
        item_edit = QLineEdit()
        sender_label = QLabel("Sender Email:")
        sender_edit = QLineEdit()
        app_name_label = QLabel("Application:")
        app_name_edit = QLineEdit()
        app_mode_label = QLabel("Application Mode:")
        app_mode_edit = QLineEdit()
        app_lvl_label = QLabel("Application Level:")
        app_lvl_edit = QLineEdit()
        period_label = QLabel("Period:")
        period_edit = QLineEdit()
        item_link_label = QLabel("Product Link:")
        item_link_edit = QLineEdit()
        manual_link_label = QLabel("Manual Link:")
        manual_link_edit = QLineEdit()
        msg_template_label = QLabel("Message Template:")
        msg_template_combo = QComboBox()

        # Получение шаблонов для комбобокса
        templates = get_template_names()
        for template in templates:
            msg_template_combo.addItem(template['name'], template['id'])

        # Заполнение полей, если редактируется существующий товар
        if good:
            item_edit.setText(good['item'])
            sender_edit.setText(good['sender'])
            app_name_edit.setText(good['app_name'])
            app_mode_edit.setText(good['app_mode'])
            app_lvl_edit.setText(good['app_lvl'])
            period_edit.setText(str(good['period']))  # Приведение значения к строке
            item_link_edit.setText(good['item_link'])
            manual_link_edit.setText(good['manual_link'])
            index = msg_template_combo.findData(good['msg_template_id'])
            if index != -1:
                msg_template_combo.setCurrentIndex(index)

        # Добавление полей в макет
        layout.addWidget(item_label)
        layout.addWidget(item_edit)
        layout.addWidget(sender_label)
        layout.addWidget(sender_edit)
        layout.addWidget(app_name_label)
        layout.addWidget(app_name_edit)
        layout.addWidget(app_mode_label)
        layout.addWidget(app_mode_edit)
        layout.addWidget(app_lvl_label)
        layout.addWidget(app_lvl_edit)
        layout.addWidget(period_label)
        layout.addWidget(period_edit)
        layout.addWidget(item_link_label)
        layout.addWidget(item_link_edit)
        layout.addWidget(manual_link_label)
        layout.addWidget(manual_link_edit)
        layout.addWidget(msg_template_label)
        layout.addWidget(msg_template_combo)

        # Кнопки сохранения и отмены
        button_layout = QHBoxLayout()
        save_button = QPushButton("Save")
        cancel_button = QPushButton("Cancel")
        button_layout.addWidget(save_button)
        button_layout.addWidget(cancel_button)
        if good:
            delete_button = QPushButton("Delete")
            button_layout.addWidget(delete_button)
        layout.addLayout(button_layout)

        dialog.setLayout(layout)

        save_button.clicked.connect(lambda: self.save_good(dialog, good, item_edit.text(), sender_edit.text(), app_name_edit.text(), app_mode_edit.text(), app_lvl_edit.text(), period_edit.text(), item_link_edit.text(), manual_link_edit.text(), msg_template_combo.currentData()))
        cancel_button.clicked.connect(dialog.close)

        def show_warning_dialog():
            """
            Предупреждение об удалении записи в базе
            :param self:
            :return:
            """
            msg_box = QMessageBox()
            msg_box.setIcon(QMessageBox.Icon.Warning)
            msg_box.setWindowTitle('Предупреждение')
            msg_box.setText('Вы уверены, что хотите удалить запись?')
            msg_box.setStandardButtons(QMessageBox.StandardButton.Yes | QMessageBox.StandardButton.No)
            msg_box.setDefaultButton(QMessageBox.StandardButton.No)
            response = msg_box.exec()

            if response == QMessageBox.StandardButton.Yes:
                # Вызов функции для удаления записи товара из таблицы GOODS
                delete_record_by_id(good)
                msg_box.close()
                dialog.close()
                self.refresh_goods_list()
            else:
                msg_box.close()

        if good:
            delete_button.clicked.connect(show_warning_dialog)

        dialog.exec()

    def save_good(self, dialog, good, item, sender, app_name, app_mode, app_lvl, period, item_link, manual_link, msg_template_id):
        """
        Сохранение товара в базу данных
        :param dialog: Всплывающее окно
        :param good: Словарь с данными товара, если редактируется, иначе None
        :param item: Наименование товара
        :param sender: E-mail отправителя
        :param app_name: Приложение
        :param app_mode: Режим приложения
        :param app_lvl: Уровень приложения
        :param period: Период действия
        :param item_link: Ссылка на товар
        :param manual_link: Ссылка на руководство
        :param msg_template_id: ID шаблона письма
        """
        # Если товар новый, присвоить ему новый ID
        if not good:
            new_id = max([g['id'] for g in self.goods], default=0) + 1
        else:
            new_id = good['id']

        good_data = {
            'id': new_id,
            'item': item,
            'sender': sender,
            'app_name': app_name,
            'app_mode': app_mode,
            'app_lvl': app_lvl,
            'period': period,
            'item_link': item_link,
            'manual_link': manual_link,
            'msg_template_id': msg_template_id
        }
        save_good(good_data)
        dialog.close()
        self.refresh_goods_list()

    def refresh_goods_list(self):
        """
        Обновление списка товаров
        """
        for i in reversed(range(self.scroll_layout.count())):
            widget = self.scroll_layout.itemAt(i).widget()
            if widget:
                widget.setParent(None)
        self.load_goods()