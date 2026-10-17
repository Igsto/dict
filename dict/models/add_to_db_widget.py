'''
Виджет добавления нового слова в словарь
'''

'''Импорты'''
from PyQt6.QtWidgets import (
    QWidget, QLabel, QLineEdit, QHBoxLayout, QVBoxLayout, QPushButton
)
from PyQt6.QtCore import pyqtSignal

'''Константы'''
VARIANTS = [f'v{i+1}' for i in range(4)]

'''Основной класс'''
class AddToDBWiget(QWidget):
    words_request = pyqtSignal(list)
    def __init__(self):
        super().__init__()
        self.create_w()
        #self.setGeometry()

    def create_w(self):
        layout = QVBoxLayout()
        new_world_label = QLabel('Слово')
        new_world_label.setStyleSheet("font-size: 20px;")
        layout.addWidget(new_world_label)
        self.new_world = WordLine()
        layout.addWidget(self.new_world)
        var_label = QLabel('Варианты')
        var_label.setStyleSheet("font-size: 20px;")
        layout.addWidget(var_label)
        self.var_list = VarList()
        layout.addWidget(self.var_list)
        self.buttons = AddNClearButtons()
        layout.addWidget(self.buttons)
        layout.setSpacing(10)
        layout.addStretch()
        self.setLayout(layout)
        self.buttons.add_button.clicked.connect(self.get_words)
        self.buttons.clear_button.clicked.connect(self.clear_words)

    def get_words(self):
        #values =
        self.words_request.emit(
            [vl.text() for vl in self.var_list.var_lines]
        )

    def clear_words(self):
        self.new_world.clear()
        for vl in self.var_list.var_lines:
            vl.clear()


'''Класс для задаваемого слова'''
class WordLine(QLineEdit):
    def __init__(self):
        super().__init__()
        self.set_outline()

    def set_outline(self):
        self.setFixedSize(170, 20)
        self.setFrame(False)
        self.setStyleSheet(sub_str(w_c='#000000'))


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


'''Объединяющий класс с вариантами'''
class VarList(QWidget):
    def __init__(self):
        super().__init__()
        self.set_up_w()

    def set_up_w(self):
        lines_layout = QVBoxLayout()
        self.var_lines = [VarLine(v) for v in VARIANTS]
        for i in range(4):
            lines_layout.addWidget(self.var_lines[i])
        lines_layout.setSpacing(0)
        lines_layout.setContentsMargins(0, 0, 0, 0)
        self.setLayout(lines_layout)


'''Класс для отдельной кнопки'''
class CustomButtonDB(QPushButton):
    def __init__(self):
        super().__init__()
        self.set_graphics()

    def set_graphics(self):
        self.setFixedSize(75, 20)
        self.setStyleSheet(sub_str_btn())


'''Класс с кнопками'''
class AddNClearButtons(QWidget):
    def __init__(self):
        super().__init__()
        self.set_up_w()

    def set_up_w(self):
        self.setFixedSize(170, 20)
        layout = QHBoxLayout()
        self.add_button = CustomButtonDB()
        self.add_button.setText('Добавить')
        layout.addWidget(self.add_button)
        self.clear_button = CustomButtonDB()
        self.clear_button.setText('Очистить')
        layout.addWidget(self.clear_button)
        layout.setSpacing(0)
        layout.setContentsMargins(0, 0, 0, 0)
        self.setLayout(layout)


'''Вспомогательная функция для рамок'''
def sub_str(outline_c='#3c30e3', w_c='#07fc03'):
    return f""" 
    QLineEdit {{
        border: 1px solid {outline_c};
        color: {w_c};
    }}
    """


'''Вспомогательная функция для кнопок'''
def sub_str_btn(brd_c='#3c30e3'):
    return f"""
    QPushButton {{ 
        background-color: #ffffff;
        color: #000000;
        border: 1px solid {brd_c};
        border-radius: 2px; 
        font-size: 14px;
    }}
    """