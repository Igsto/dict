
'''
Тута объявлены все виджеты для непосредственной работы. Название модуля написано с
ошибкой потому что так исторически сложилось
'''

'''Импорты'''
from PyQt6.QtWidgets import (
    QWidget, QComboBox, QStackedLayout, QVBoxLayout, QLabel
)


'''Главный виджет'''
class MainWidget(QWidget):
    def __init__(self):
        super().__init__()
        self.create_w()

    def create_w(self):
        #выбираем действие
        choose_act = QComboBox()
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
        main_layout.addWidget(self.acts)
        self.setLayout(main_layout)


'''Класс для выбора слова'''
class ChooseWordWidget(QWidget):
    def __init__(self):
        super().__init__()
        self.create_w()

    def create_w(self):
        check_is_work = QLabel('Эта херня работает',self)


'''Класс для добавления слова в БД'''
class AddToDBWiget(QWidget):
    def __init__(self):
        super().__init__()
        self.create_w()

    def create_w(self):
        check_is_work = QLabel('Эта херня тоже работает',self)