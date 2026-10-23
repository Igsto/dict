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
        #self.not_begin_flag = True
        self.create_w()

    def create_w(self):
        #оформление
        self.setMinimumSize(450, 350)

        #выбираем действие
        choose_act = QComboBox()
        choose_act.addItem('Практика')
        choose_act.addItem('Добавление слова')

        #создаём слой для выбора и добавляем страницы
        self.acts = QStackedLayout()
        self.choose_word_page = ChooseWordWidget()
        self.choose_word_page.buttons.interrupt_button.setEnabled(False)
        self.acts.addWidget(self.choose_word_page)
        self.choose_word_controller = ChooseWordController(self.storage)
        self.choose_word_queue = ChooseWordQueue()

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

        #self.choose_word_page.buttons.begin_button.setEnabled(True)
        self.choose_word_page.buttons.begin_button.clicked.connect(self.get_start)
        self.choose_word_page.buttons.begin_button.clicked.connect(self.interrupt_button_enabeled)
        self.choose_word_page.buttons.interrupt_button.clicked.connect(self.reset)

        self.choose_word_queue.queue_empty_request.connect(self.get_interrupt)
        self.choose_word_page.vars.click_occured.connect(self.get_next_word)
        self.choose_word_queue.queue_empty_request.connect(self.begin_button_enabeled)


    #если нажата кнопка начать
    def get_start(self):
        words = [w.to_dict_w() for w in self.choose_word_controller.get_words()]
        self.choose_word_queue.fill(words)
        self.choose_word_page.buttons.begin_button.setEnabled(False)

        self.get_next_word()

    #включаем кнопку начать если очередь пуста
    def begin_button_enabeled(self):
        self.choose_word_page.buttons.begin_button.setEnabled(True)

    def interrupt_button_enabeled(self):
        self.choose_word_page.buttons.interrupt_button.setEnabled(True)

    def interrupt_button_unenabeled(self):
        self.choose_word_page.buttons.interrupt_button.setEnabled(False)

    #новое слово из очереди
    def get_next_word(self):
        next_word = self.choose_word_queue.next_word()
        if next_word is not None:
            self.choose_word_page.show_next(next_word)

    #ресет
    def reset(self):
        self.choose_word_page.reset_all()

    def get_interrupt(self):
        self.choose_word_queue.clear()
        self.reset()


'''Кастомная очередь'''
class ChooseWordQueue(QObject):
    queue_empty_request = pyqtSignal()
    def __init__(self):
        super().__init__()
        #self.queue = deque(words)

    def next_word(self):
        #next = self.queue.pop()
        if not self.is_empty():
            self.queue_empty_request.emit()
            return None
        return self.queue.pop()

    def fill(self, words):
        self.queue = deque(words)

    def clear(self):
        self.queue.clear()

    def is_empty(self):
        return bool(self.queue)