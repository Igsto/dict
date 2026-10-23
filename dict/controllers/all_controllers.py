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




    #def fill_queue(self):



'''Контроллер для взятия слов из БД и добавление в очередь'''
class ChooseWordController:
    def __init__(self, storage: Storage):
        self.storage = storage

    def get_words(self):
        words = self.storage.get_by_date(date.today() - timedelta(days=10), date.today())
        #print(words)
        return words


# class ChooseWordController:
#     def __init__(self, storage: Storage, click_signal):
#         self.storage = storage
#         self.queue: deque[dict] = deque()
#
#     def strart(self) -> dict | None:
#         self.fill_queue()
#         return self.next_word()
#
#     def fill_queue(self):
#         words = self.storage.get_by_date(date.today(), date.today())
#         self.queue = deque(words)
#
#     def next_word(self) -> dict | None:
#         if not self.queue:
#             self.fill_queue()
#             if not self.queue:
#                 return None
#         return self.queue.popleft()
