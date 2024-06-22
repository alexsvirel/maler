from PyQt6.QtWidgets import (QLabel, QPushButton, QScrollArea,
                             QFrame, QVBoxLayout, QHBoxLayout, QLineEdit,
                             QComboBox, QCheckBox, QDialog, QMessageBox, QSpinBox)

from base.base_tab import BaseTab
from utils.db_settings_goods import get_goods, get_template_names, save_good, delete_good_by_id


class MailerSettingsGoodsTab(BaseTab):
    """
    Класс для под-вкладки 'Товары' в 'Настройки'
    """

    def __init__(self, controller):
        """
        Инициализация под-вкладки 'Товары'
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

        self.add_button = QPushButton(self.tr("Add a product"))
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
        Показ всплывающего окна для добавления или редактирования товара.
        :param good: Словарь с данными товара, если редактируется, иначе None.
        """
        dialog = QDialog(self)
        dialog.setWindowTitle(self.tr("Product Properties"))

        dialog_layout = QVBoxLayout(dialog)
        dialog_scroll_area = QScrollArea(dialog)
        dialog_scroll_area.setWidgetResizable(True)
        dialog_scroll_content = QFrame(dialog_scroll_area)
        dialog_scroll_layout = QVBoxLayout(dialog_scroll_content)
        dialog_scroll_area.setWidget(dialog_scroll_content)
        dialog_layout.addWidget(dialog_scroll_area)

        # Создание полей для ввода данных
        fields = {
            'item': (self.tr("Product Name:"), QLineEdit()),
            'sender': (self.tr("Sender Email:"), QLineEdit()),
            'app_name': (self.tr("Application:"), QLineEdit()),
            'app_mode': (self.tr("Application Mode:"), QLineEdit()),
            'app_lvl': (self.tr("Application Level:"), QLineEdit()),
            'period': (self.tr("Period:"), QLineEdit()),
            'item_link': (self.tr("Product Link:"), QLineEdit()),
            'manual_link': (self.tr("Manual Link:"), QLineEdit()),
            'msg_template_id': (self.tr("Message Template:"), QComboBox())
        }

        for key, (label, widget) in fields.items():
            dialog_scroll_layout.addWidget(QLabel(label))
            dialog_scroll_layout.addWidget(widget)

        # Получение шаблонов для комбобокса
        templates = get_template_names()
        for template in templates:
            fields['msg_template_id'][1].addItem(template['name'], template['id'])

        # Заполнение полей, если редактируется существующий товар
        if good:
            fields['item'][1].setText(good['item'])
            fields['sender'][1].setText(good['sender'])
            fields['app_name'][1].setText(good['app_name'])
            fields['app_mode'][1].setText(good['app_mode'])
            fields['app_lvl'][1].setText(good['app_lvl'])
            fields['period'][1].setText(str(good['period']))  # Приведение значения к строке
            fields['item_link'][1].setText(good['item_link'])
            fields['manual_link'][1].setText(good['manual_link'])
            index = fields['msg_template_id'][1].findData(good['msg_template_id'])
            if index != -1:
                fields['msg_template_id'][1].setCurrentIndex(index)

        # Чекбокс "Использовать рассылку"
        use_mailing_checkbox = QCheckBox(self.tr("Use mailing"))
        dialog_scroll_layout.addWidget(use_mailing_checkbox)

        # Метки "День" и "Шаблон"
        day_template_layout = QHBoxLayout()
        day_template_layout.addWidget(QLabel(self.tr("Day")))
        day_template_layout.addWidget(QLabel(self.tr("Template")))
        dialog_scroll_layout.addLayout(day_template_layout)

        # Контейнер для хранения строк с полями для выбора числа и шаблона
        self.mailing_lines = []

        def add_mailing_line(day=None, template_id=None):
            """
            Добавление строки с полями для выбора числа, шаблона, и кнопками добавления/удаления.
            """
            mailing_line_layout = QHBoxLayout()

            day_spinbox = QSpinBox()
            day_spinbox.setRange(1, 100)
            if day:
                day_spinbox.setValue(day)

            template_combo = QComboBox()
            for template in templates:
                template_combo.addItem(template['name'], template['id'])
            if template_id:
                index = template_combo.findData(template_id)
                if index != -1:
                    template_combo.setCurrentIndex(index)

            add_button = QPushButton(self.tr("Add"))
            delete_button = QPushButton(self.tr("Delete"))

            mailing_line_layout.addWidget(day_spinbox)
            mailing_line_layout.addWidget(template_combo)
            mailing_line_layout.addWidget(add_button)
            mailing_line_layout.addWidget(delete_button)

            # Добавление в список для управления активностью
            self.mailing_lines.append(mailing_line_layout)

            # Связывание кнопок с функциями добавления и удаления
            add_button.clicked.connect(add_mailing_line)
            delete_button.clicked.connect(lambda: delete_mailing_line(mailing_line_layout))

            dialog_scroll_layout.insertLayout(dialog_scroll_layout.count() - 1, mailing_line_layout)

            # Обновление активности элементов в строке
            update_mailing_line_state()

        def delete_mailing_line(mailing_line_layout):
            """
            Удаление строки с полями для выбора числа, шаблона, и кнопками добавления/удаления.
            """
            if len(self.mailing_lines) > 1:
                for i in range(mailing_line_layout.count()):
                    widget = mailing_line_layout.itemAt(i).widget()
                    if widget:
                        widget.deleteLater()
                self.mailing_lines.remove(mailing_line_layout)
                dialog_scroll_layout.removeItem(mailing_line_layout)
                mailing_line_layout.deleteLater()

        def update_mailing_line_state():
            """
            Обновление активности строк в зависимости от состояния чек-бокса.
            """
            is_enabled = use_mailing_checkbox.isChecked()
            for mailing_line_layout in self.mailing_lines:
                for i in range(mailing_line_layout.count()):
                    widget = mailing_line_layout.itemAt(i).widget()
                    if widget:
                        widget.setEnabled(is_enabled)

        # # Начальная строка с полями для выбора числа и шаблона
        # add_mailing_line()

        # Связывание чек-бокса с функцией обновления активности строк
        use_mailing_checkbox.stateChanged.connect(update_mailing_line_state)

        # Заполнение строк с полями для выбора числа и шаблона, если редактируется существующий товар
        if good and 'periods' in good and good['periods']:
            use_mailing_checkbox.setChecked(True)
            for day, template_id in good['periods'].items():
                add_mailing_line(int(day), int(template_id))
        else:
            # Начальная строка с полями для выбора числа и шаблона
            add_mailing_line()

        # Кнопки сохранения и отмены
        button_layout = QHBoxLayout()
        save_button = QPushButton(self.tr("Save"))
        cancel_button = QPushButton(self.tr("Cancel"))
        button_layout.addWidget(save_button)
        button_layout.addWidget(cancel_button)
        if good:
            delete_button = QPushButton(self.tr("Delete"))
            button_layout.addWidget(delete_button)
        dialog_layout.addLayout(button_layout)

        def collect_periods():
            """
            Сбор данных из строк с полями для выбора числа и шаблона.
            :return: Словарь с данными периода и шаблонов.
            """
            periods = {}
            for mailing_line_layout in self.mailing_lines:
                day_spinbox = mailing_line_layout.itemAt(0).widget()
                template_combo = mailing_line_layout.itemAt(1).widget()
                if day_spinbox and template_combo:
                    day = day_spinbox.value()
                    template_id = template_combo.currentData()
                    periods[day] = str(template_id)
            return periods

        save_button.clicked.connect(lambda: self.save_good(
            dialog,
            good,
            fields['item'][1].text(),
            fields['sender'][1].text(),
            fields['app_name'][1].text(),
            fields['app_mode'][1].text(),
            fields['app_lvl'][1].text(),
            fields['period'][1].text(),
            fields['item_link'][1].text(),
            fields['manual_link'][1].text(),
            fields['msg_template_id'][1].currentData(),
            use_mailing_checkbox.isChecked(),
            collect_periods()
        ))

        cancel_button.clicked.connect(dialog.close)

        def show_warning_dialog():
            """
            Предупреждение об удалении записи в базе.
            """
            msg_box = QMessageBox()
            msg_box.setIcon(QMessageBox.Icon.Warning)
            msg_box.setWindowTitle(self.tr("Warning"))
            msg_box.setText(self.tr("Are you sure you want to delete the record?"))
            msg_box.setStandardButtons(QMessageBox.StandardButton.Yes | QMessageBox.StandardButton.No)
            msg_box.setDefaultButton(QMessageBox.StandardButton.No)
            response = msg_box.exec()

            if response == QMessageBox.StandardButton.Yes:
                # Вызов функции для удаления записи товара из таблицы GOODS
                delete_good_by_id(good)
                msg_box.close()
                dialog.close()
                self.refresh_goods_list()
            else:
                msg_box.close()

        if good:
            delete_button.clicked.connect(show_warning_dialog)

        dialog.exec()

    def save_good(self, dialog, good, item, sender, app_name, app_mode, app_lvl, period, item_link, manual_link, msg_template_id, use_mailing, periods):
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
        :param use_mailing: Флаг использования рассылки
        :param periods: Словарь периодов и шаблонов
        """
        # Если товар новый, присвоить ему новый ID
        if not good:
            new_id = max([g['id'] for g in self.goods], default=0) + 1
        else:
            new_id = good['id']

        # Запись в PERIODS для управления рассылкой
        if use_mailing:
            mailing_control = periods       # чек-бокс активирован
        else:
            mailing_control = {}            # чек-бокс НЕ активирован

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
            'msg_template_id': msg_template_id,
            'use_mailing': use_mailing,
            'periods': mailing_control
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

    def retranslate_ui(self):
        """
        Обновление текстов виджетов при смене языка
        """
        self.label.setText(self.tr("Click on the product name to edit its properties"))
        self.add_button.setText(self.tr("Add a product"))
