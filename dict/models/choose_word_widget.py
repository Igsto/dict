'''
Виджет выбора слова
'''

from PyQt6.QtWidgets import (
    QWidget, QLabel
)

'''
Основной класс
'''
class ChooseWordWidget(QWidget):
    def __init__(self):
        super().__init__()
        self.create_w()

    def create_w(self):
        check_is_work = QLabel('Эта херня работает',self)