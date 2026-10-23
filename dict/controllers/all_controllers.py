'''
Модуль с контроллерами
'''

'''Импорты'''
from ..consts import Word
from ..db.sql_module import Storage
from collections import deque
import random
from datetime import date, timedelta


'''Контроллер что сохраняет новое слово в БД'''
class AddToDBController:
    def __init__(self, words_request_signal, storage: Storage):
        self.storage = storage
        words_request_signal.connect(self.to_add)

    def to_add(self, word: Word):
        self.storage.add(word)


'''Контроллер для взятия слов из БД и добавление в очередь'''
class ChooseWordController:
    def __init__(self, storage: Storage):
        self.storage = storage

    def get_words(self):
        words = self.storage.get_by_date(date.today() - timedelta(days=10), date.today())
        #print(words)
        return words