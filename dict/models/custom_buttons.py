'''Модуль с кастомными кнопками'''
from PyQt6.QtWidgets import (
    QPushButton
)
from ..consts import sub_str_btn

'''Класс для отдельной кнопки'''
class CustomButton(QPushButton):
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