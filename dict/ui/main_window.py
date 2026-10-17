
'''
Модуль чисто для создания главного окна.
Комментарии минимальны потому что понятно чо да как.
По крайней мере пока
'''

from PyQt6.QtWidgets import (
    QMainWindow
)
from dict.models.main_widget import MainWidget

class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setup_ui()

    def setup_ui(self):
        main_w = MainWidget()
        self.setCentralWidget(main_w)