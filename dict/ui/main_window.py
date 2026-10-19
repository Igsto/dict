
'''
Модуль чисто для создания главного окна.
Комментарии минимальны потому что понятно чо да как.
По крайней мере пока
'''

from PyQt6.QtWidgets import (
    QMainWindow
)
from dict.models.main_widget import MainWidget
from ..db.sql_module import Storage

class MainWindow(QMainWindow):
    def __init__(self, storage: Storage):
        super().__init__()
        self.storage = storage
        self.setup_ui()

    def setup_ui(self):
        main_w = MainWidget(self.storage)
        self.setCentralWidget(main_w)