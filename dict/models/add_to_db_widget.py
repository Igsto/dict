'''
Виджет добавления нового слова в словарь
'''

'''
Импорты
'''
from PyQt6.QtWidgets import (
    QWidget, QLabel, QLineEdit
)

'''Основной класс'''
class AddToDBWiget(QWidget):
    def __init__(self):
        super().__init__()
        self.create_w()
        #self.setGeometry()

    def create_w(self):
        #check_is_work = QLabel('Эта херня тоже работает',self)
        new_world_label = QLabel('Слово')
        new_world = QLineEdit()
        var_label = QLabel('Варианты')
        var_list = [VarLine(f'v{i}') for i in range(1,5)]

'''Класс для вариантов'''
class VarLine(QLineEdit):
    def __init__(self, field_id: str):
        super().__init__()
        self.field_id = field_id