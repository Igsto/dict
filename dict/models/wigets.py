
'''
Тута объявлены все виджеты для непосредственной работы. Название модуля написано с
ошибкой потому что так исторически сложилось
На текущий момент мусор, я просто игрался
'''

'''Импорты'''
from PyQt6.QtCore import pyqtSignal
from PyQt6.QtWidgets import (
    QWidget, QComboBox, QStackedLayout, QVBoxLayout, QLabel, QLineEdit
)


'''Главный виджет'''
class MainWidget(QWidget):
    def __init__(self):
        super().__init__()
        self.create_w()

    def create_w(self):
        #оформление
        self.setMinimumSize(450, 350)

        #выбираем действие
        choose_act = QComboBox()
        #choose_act.resize(50, 20)
        choose_act.addItem('Практика')
        choose_act.addItem('Добавление слова в словарь')

        #создаём слой для выбора и добавляем страницы
        self.acts = QStackedLayout()
        choose_word_page = ChooseWordWidget()
        add_to_db_page = AddToDBWiget()
        self.acts.addWidget(choose_word_page)
        self.acts.addWidget(add_to_db_page)

        #соединяем с комбо боксом
        choose_act.currentIndexChanged.connect(self.acts.setCurrentIndex)

        #создаём основной лэйаут
        main_layout = QVBoxLayout()
        main_layout.addWidget(choose_act)
        main_layout.addLayout(self.acts)
        self.setLayout(main_layout)


'''Выбор слова'''
'''Основной класс'''
class ChooseWordWidget(QWidget):
    def __init__(self):
        super().__init__()
        self.create_w()

    def create_w(self):
        check_is_work = QLabel('Эта херня работает',self)



'''Добавление в БД'''
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