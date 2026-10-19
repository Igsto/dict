from ..consts import Word
from ..db.sql_module import Storage

class AddToDBController:
    def __init__(self, words_request_signal, storage: Storage):
        self.storage = storage
        words_request_signal.connect(self.to_add)

    def to_add(self, word: Word):
        self.storage.add(word)