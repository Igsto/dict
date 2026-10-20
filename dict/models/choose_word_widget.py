'''
Виджеты выбора слова
'''

'''Импорты'''
from PyQt6.QtWidgets import (
    QWidget, QLabel, QStackedWidget, QPushButton, QVBoxLayout
)
from PyQt6.QtCore import pyqtSignal, Qt
from PyQt6.QtGui import QCursor
from ..consts import Word, sub_str_btn, sub_str_label, VARIANTS
import random


'''
Основной класс
'''
class ChooseWordWidget(QWidget):
    def __init__(self, word: Word):
        self.word = word
        super().__init__()
        self.create_w()

    def create_w(self):
        layout = QVBoxLayout()
        word_label = QLabel(self.word.w.capitalize())
        word_label.setStyleSheet("font-size: 20px;")
        layout.addWidget(word_label)
        vars_label = QLabel('Варианты')
        vars_label.setStyleSheet("font-size: 20px;")
        layout.addWidget(word_label)
        self.vars = ChooseVariants(self.word.to_dict_vars())
        layout.addWidget(self.vars)
        layout.setSpacing(10)
        layout.addStretch()
        self.setLayout(layout)


# '''Класс с кнопкой начать'''
# class BeginWidget(QWidget):
#     def __init__(self):
#         super().__init__()
#         self.set_up_w()
#
#     def set_up_w(self):
#         pass


'''Класс одна линия'''
class SingleLine(QLabel):
    clicked_request = pyqtSignal()
    def __init__(self, v_label: str, v_word: str):
        self.v_label = v_label
        self.v_word = v_word
        super().__init__(self.v_word)
        self.set_graphics()

    def set_graphics(self):
        self.setFixedSize(170, 20)
        self.setCursor(QCursor(Qt.CursorShape.PointingHandCursor))
        if self.v_label == 'v1':
            self.base_style = sub_str_label()
        else:
            self.base_style = sub_str_label(v_c='#fc0303')
        self.setStyleSheet(self.base_style)

    def mousePressEvent(self, event):
        if event.button == Qt.MouseButton.LeftButton:
            self.clicked_request.emit()
        super().mousePressEvent(event)


'''Класс с выбором'''
class ChooseVariants(QWidget):
    def __init__(self, w_dict: dict):
        lst = list(w_dict.items())
        random.shuffle(lst)
        # self.w_vars = dict(
        #     random.shuffle(list(w_dict.items()))
        # )
        self.w_vars = dict(lst)
        super().__init__()
        self.set_up_w()

    def set_up_w(self):
        layout = QVBoxLayout()
        self.lines = [SingleLine(v_label=v, v_word=w) for v, w in self.w_vars.items()]
        for l in self.lines:
            layout.addWidget(l)
        layout.setSpacing(0)
        layout.setContentsMargins(0, 0, 0, 0)
        self.setLayout(layout)

# '''Кнопка начать'''
# class BeginButton(QPushButton):
#     begin_request = pyqtSignal(bool)
#     def __init__(self):
#         super().__init__()
#         self.set_graphics()
#
#     def set_graphics(self):
#         self.setFixedSize(75, 20)
#         self.setStyleSheet(sub_str_btn())
#         self.cl