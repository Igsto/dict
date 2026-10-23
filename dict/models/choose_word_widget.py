'''
Виджеты выбора слова
'''

'''Импорты'''
from PyQt6.QtWidgets import (
    QWidget, QLabel, QStackedWidget, QPushButton, QVBoxLayout, QHBoxLayout
)
from PyQt6.QtCore import pyqtSignal, Qt, QTimer
from PyQt6.QtGui import QCursor
from .custom_buttons import CustomButton
from ..consts import Word, sub_str_btn, sub_str_label, VARIANTS
import random
import time


'''
Основной класс
'''
class ChooseWordWidget(QWidget):
    def __init__(self):
        super().__init__()
        self.create_w()

    def create_w(self):
        layout = QVBoxLayout()
        self.word_label = QLabel()
        self.word_label.setStyleSheet("font-size: 20px;")
        layout.addWidget(self.word_label)
        vars_label = QLabel('Варианты')
        vars_label.setStyleSheet("font-size: 20px;")
        layout.addWidget(vars_label)
        self.vars = ChooseVariants()
        layout.addWidget(self.vars)
        self.buttons = BeginNInterruptButtons()
        layout.addWidget(self.buttons)
        layout.setSpacing(10)
        layout.addStretch()
        self.setLayout(layout)

    def show_next(self, words: dict):
        self.word_label.setText(words['w'].strip().capitalize())
        var_dict = words.copy()
        var_dict.pop('w', None)
        self.vars.show_words(var_dict)

    def reset_all(self):
        self.word_label.setText('Усё')
        self.vars.reset_lines()
        self.buttons.begin_button.setEnabled(True)
        self.buttons.interrupt_button.setEnabled(False)


'''Класс одна линия'''
class SingleLine(QLabel):
    clicked_request = pyqtSignal()
    def __init__(self):
        self.v_label = ''
        self.v_word = ''
        super().__init__(self.v_word)
        self.reset_timer = QTimer()
        self.reset_timer.setSingleShot(True)
        self.reset_timer.timeout.connect(self.reset_style)
        self.set_graphics()

    def set_graphics(self):
        self.setFixedSize(170, 20)
        self.setCursor(QCursor(Qt.CursorShape.PointingHandCursor))
        self.base_style = sub_str_label()
        self.setStyleSheet(self.base_style)

    #если поступили слова
    def if_begun(self, v_l: str, v_w: str):
        self.v_label = v_l
        self.v_word = v_w
        self.setText(self.v_word)

        if self.v_word.strip():
            self.setEnabled(True)
        else:
            self.setEnabled(False)


    #функция для установки при нажатии
    def flash(self, c: str, ms: int = 1000):
        qss = sub_str_label(v_c=c)
        self.setStyleSheet(qss)
        self.reset_timer.start(ms)

    #возврат к базовому стилю
    def reset_style(self):
        self.setStyleSheet(self.base_style)

    #ресет всего
    def reset_to_base(self):
        self.reset_style()
        self.v_word = ''
        self.v_label = ''
        self.setText('')
        self.setEnabled(False)

    #нажато
    def mousePressEvent(self, event):
        if event.button() == Qt.MouseButton.LeftButton:
            #print(f"[DEBUG] клик по {self.v_label}")
            self.clicked_request.emit()
        super().mousePressEvent(event)


'''Класс с выбором'''
class ChooseVariants(QWidget):
    line_clicked_request = pyqtSignal(bool)
    click_occured = pyqtSignal()

    def __init__(self):
        super().__init__()

        self.unlock_timer = QTimer()
        self.unlock_timer.setSingleShot(True)
        self.unlock_timer.timeout.connect(self.unlock_lines)

        self.set_up_w()

    def set_up_w(self):
        layout = QVBoxLayout()
        self.lines = [SingleLine() for _ in range(4)]
        for l in self.lines:
            layout.addWidget(l)
            l.clicked_request.connect(lambda checked=False, line=l: self.on_line_clicked(line))
        layout.setSpacing(0)
        layout.setContentsMargins(0, 0, 0, 0)
        self.setLayout(layout)

    #показываем слова если есть
    def show_words(self, v_w: dict):
        lst = list(v_w.items())
        random.shuffle(lst)
        self.v_wars = dict(lst)

        for l, (v, w) in zip(self.lines, self.v_wars.items()):
            l.if_begun(v, w)

    #возврат к базе
    def reset_lines(self):
        for l in self.lines:
            l.reset_to_base()

    #дейстаия при нажатии
    def on_line_clicked(self, line: SingleLine):
        for l in self.lines:
            l.setEnabled(False)

        self.unlock_timer.start(1000)

        if line.v_label == 'v1':
            line.flash('#00aa00', 1000)
            self.line_clicked_request.emit(True)
        else:
            line.flash('#ff0000', 1000)

            for l in self.lines:
                if l.v_label == 'v1':
                    l.flash('#00aa00', 1000)
                    break

            self.line_clicked_request.emit(False)

        QTimer.singleShot(1000, self.click_occured.emit)

    #функция разблокировки линий
    def unlock_lines(self):
        for l in self.lines:
            l.setEnabled(True)


'''Кнопки начать и прервать'''
class BeginNInterruptButtons(QWidget):
    def __init__(self):
        super().__init__()
        self.set_up_w()

    def set_up_w(self):
        self.setFixedSize(170, 20)
        layout = QHBoxLayout()
        self.begin_button = CustomButton('Начать')
        layout.addWidget(self.begin_button)
        self.interrupt_button = CustomButton('Прервать')
        layout.addWidget(self.interrupt_button)
        layout.setSpacing(0)
        layout.setContentsMargins(0, 0, 0, 0)
        self.setLayout(layout)