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
from ..controllers.all_controllers import AddToDBController
from ..db.sql_module import Storage
from ..consts import Word
from datetime import date

'''
Класс главного виджета
'''
class MainWidget(QWidget):
    def __init__(self, storage: Storage):
        super().__init__()
        self.storage = storage
        self.create_w()

    def create_w(self):
        #оформление
        self.setMinimumSize(450, 350)

        #выбираем действие
        choose_act = QComboBox()
        choose_act.addItem('Практика')
        choose_act.addItem('Добавление слова в словарь')

        #создаём слой для выбора и добавляем страницы
        self.acts = QStackedLayout()
        #для теста
        w = Word.from_dict(
            {
                'w': 'word',
                'v1': 'слово', 'v2': 'кошка', 'v3': 'беспилотник', 'v4': 'онанизм',
                'date': date.today()
            }
        )
        #print(w.to_dict_vars())
        choose_word_page = ChooseWordWidget(w)
        self.add_to_db_page = AddToDBWiget()
        self.add_to_db_controller = AddToDBController(
            self.add_to_db_page.words_request, self.storage
        )
        self.acts.addWidget(choose_word_page)
        self.acts.addWidget(self.add_to_db_page)

        #соединяем с комбо боксом
        choose_act.currentIndexChanged.connect(self.acts.setCurrentIndex)

        #создаём основной лэйаут
        main_layout = QVBoxLayout()
        main_layout.addWidget(choose_act)
        main_layout.addLayout(self.acts)
        self.setLayout(main_layout)

        #коннектим с кнопкой
        self.add_to_db_page.words_request.connect(self.print_words)

    def print_words(self, values):
        print(values)