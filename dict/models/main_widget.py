'''
Главный виджет
'''

'''
Импорты
'''
from PyQt6.QtWidgets import (
    QWidget, QStackedLayout, QComboBox, QVBoxLayout
)
from PyQt6.QtCore import pyqtSignal, QObject
from .choose_word_widget import ChooseWordWidget
from .add_to_db_widget import AddToDBWiget
from ..controllers.all_controllers import AddToDBController, ChooseWordController
from ..db.sql_module import Storage
from ..consts import Word
from datetime import date
from collections import deque

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
        self.choose_word_page = ChooseWordWidget()
        self.acts.addWidget(self.choose_word_page)
        self.choose_word_controller = ChooseWordController(self.storage)
        words = [w.to_dict_w() for w in self.choose_word_controller.get_words()]
        print(words)
        self.choose_word_queue = ChooseWordQueue(words)

        #аналогично для добавления
        self.add_to_db_page = AddToDBWiget()
        self.add_to_db_controller = AddToDBController(
            self.add_to_db_page.words_request, self.storage
        )
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

        self.choose_word_queue.queue_empty_request.connect(self.reset)
        self.choose_word_page.vars.click_occured.connect(self.get_next_word)

        self.get_next_word()

    #новое слово из очереди
    def get_next_word(self):
        print(f"[DEBUG] get_next_word, queue len={len(self.choose_word_queue.queue)}")
        next_word = self.choose_word_queue.next_word()
        print(f"[DEBUG] next_word = {next_word}")
        if next_word is not None:
            self.choose_word_page.show_next(next_word)

    #ресет
    def reset(self):
        print("[DEBUG] reset вызван")
        self.choose_word_page.reset_all()

    #для теста выводим заполненное
    def print_words(self, values):
        print(values)


'''Кастомная очередь'''
class ChooseWordQueue(QObject):
    queue_empty_request = pyqtSignal()
    def __init__(self, words):
        super().__init__()
        self.queue = deque(words)

    def next_word(self):
        #next = self.queue.pop()
        if not self.queue:
            self.queue_empty_request.emit()
            return None
        return self.queue.pop()

    def clear(self):
        self.queue.clear()

    def is_empty(self):
        return bool(self.queue)