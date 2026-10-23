'''
Виджет добавления нового слова в словарь
'''

'''Импорты'''
from PyQt6.QtWidgets import (
    QWidget, QLabel, QLineEdit, QHBoxLayout, QVBoxLayout, QPushButton
)
from PyQt6.QtCore import pyqtSignal, QTimer
from .custom_buttons import CustomButton
from dict.consts import VARIANTS, Word, sub_str_btn, sub_str
from datetime import date

'''Основной класс'''
class AddToDBWiget(QWidget):
    words_request = pyqtSignal(Word)
    def __init__(self):
        super().__init__()
        self.create_w()
        #self.setGeometry()

    #Создание виждета
    def create_w(self):
        #основной лэйаут
        layout = QVBoxLayout()
        #надпись
        new_world_label = QLabel('Слово')
        new_world_label.setStyleSheet("font-size: 20px;")
        layout.addWidget(new_world_label)
        #новое слово
        self.new_world = WordLine()
        layout.addWidget(self.new_world)
        # надпись
        var_label = QLabel('Варианты')
        var_label.setStyleSheet("font-size: 20px;")
        layout.addWidget(var_label)
        #четыре слова
        self.var_list = VarList()
        layout.addWidget(self.var_list)
        #кнопки
        self.buttons = AddNClearButtons()
        self.buttons.add_button.setEnabled(False)
        layout.addWidget(self.buttons)
        #настройка основного лэйаута
        layout.setSpacing(10)
        layout.addStretch()
        self.setLayout(layout)

        #изменение состояния кнопки
        self.new_word_filled = False
        self.new_world.is_word_filled_request.connect(self.new_word_update)
        self.var_list_filled = False
        self.var_list.is_filled_request.connect(self.var_list_update)

        self.buttons.add_button.clicked.connect(self.get_words)
        self.buttons.clear_button.clicked.connect(self.clear_words)

    #Функция для получения словаря с данными
    def get_words(self):
        word_dict = {'w': self.new_world.text()} | \
            {vl.field_id: vl.text() for vl in self.var_list.var_lines} | \
            {'date': date.today()}
        curr_word = Word.from_dict(word_dict)
        self.words_request.emit(curr_word)
        self.buttons.add_button.setText('Добавлено!')
        self.buttons.add_button.setEnabled(False)
        QTimer.singleShot(1500, self.after_add)

    #функция для действий после нажатия кнопки
    def after_add(self):
        self.clear_words()
        self.buttons.add_button.return_to_orig_label()
        self.update_stage()

    #Очистка
    def clear_words(self):
        self.new_world.clear()
        for vl in self.var_list.var_lines:
            vl.clear()

    #функции изменение переменных состояний кнопки
    def new_word_update(self, nw_up):
        self.new_word_filled = nw_up
        self.update_stage()

    def var_list_update(self, vl_up):
        self.var_list_filled = vl_up
        self.update_stage()

    #Изменение состояния кнопки добавить
    def update_stage(self):
        self.buttons.add_button.setEnabled(
            self.new_word_filled and self.var_list_filled
        )


'''Класс для задаваемого слова'''
class WordLine(QLineEdit):
    is_word_filled_request = pyqtSignal(bool)
    def __init__(self):
        super().__init__()
        self.set_outline()
        self.set_up_w()

    #графика
    def set_outline(self):
        self.setFixedSize(170, 20)
        self.setFrame(False)
        self.setStyleSheet(sub_str(w_c='#000000'))

    #настройка виджета
    def set_up_w(self):
        self.textChanged.connect(self.is_word_filled)

    #проверка на заполнение
    def is_changed(self):
        return bool(self.text())

    #эмит заполнения
    def is_word_filled(self):
        self.is_word_filled_request.emit(self.is_changed())


'''Класс для вариантов, одна линия заполнения'''
class VarLine(QLineEdit):
    def __init__(self, field_id: str):
        super().__init__()
        self.field_id = field_id
        self.set_outline()

    #создаём рамку
    def set_outline(self):
        self.setFixedSize(170, 20)
        self.setFrame(False)

        if self.field_id == 'v1':
            self.setStyleSheet(sub_str())
        else:
            self.setStyleSheet(sub_str(w_c='#fc0303'))

    #проверка заполнено ли
    def is_filled_line(self) -> bool:
        return bool(self.text())


'''Объединяющий класс с вариантами'''
class VarList(QWidget):
    is_filled_request = pyqtSignal(bool)
    def __init__(self):
        super().__init__()
        self.set_up_w()

    #создание виждета
    def set_up_w(self):
        lines_layout = QVBoxLayout()
        self.var_lines = [VarLine(v) for v in VARIANTS]
        for v in self.var_lines:
            v.textChanged.connect(self.is_filled)
            lines_layout.addWidget(v)
        lines_layout.setSpacing(0)
        lines_layout.setContentsMargins(0, 0, 0, 0)
        self.setLayout(lines_layout)

    #эмит сигнала если есть текст
    def is_filled(self, *_):
        self.is_filled_request.emit(
            all(v.is_filled_line() for v in self.var_lines)
        )

'''Класс для отдельной кнопки'''
class CustomButtonDB(QPushButton):
    def __init__(self, lbl = ''):
        super().__init__()
        self.lbl = lbl
        self.set_graphics()
        self.set_up_w()

    #графика
    def set_graphics(self):
        self.setFixedSize(75, 20)
        self.setStyleSheet(sub_str_btn())

    #создание виджета
    def set_up_w(self):
        self.setText(self.lbl)

    def return_to_orig_label(self):
        self.setText(self.lbl)

'''Класс с кнопками'''
class AddNClearButtons(QWidget):
    def __init__(self):
        super().__init__()
        self.set_up_w()

    def set_up_w(self):
        self.setFixedSize(170, 20)
        layout = QHBoxLayout()
        self.add_button = CustomButtonDB('Добавить')
        layout.addWidget(self.add_button)
        self.clear_button = CustomButtonDB('Очистить')
        layout.addWidget(self.clear_button)
        layout.setSpacing(0)
        layout.setContentsMargins(0, 0, 0, 0)
        self.setLayout(layout)


