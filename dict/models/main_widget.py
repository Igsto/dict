'''
Главный виджет
'''

'''
Импорты
'''
from PyQt6.QtWidgets import (
    QWidget, QStackedLayout, QComboBox, QVBoxLayout
)
from .choose_word_widget import ChooseWordWidget
from .add_to_db_widget import AddToDBWiget

'''
Класс главного виджета
'''
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