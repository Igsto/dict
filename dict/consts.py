'''
В данном файле лежат важные константы и всякие функции
'''

from dataclasses import dataclass
from datetime import date
import sqlite3
#from collections import deque

VARIANTS = [f'v{i+1}' for i in range(4)]


'''Кастомная очередь'''
class ChooseWordQueue:
    def __init__(self):
        pass


'''Класс для одного слова'''
@dataclass
class Word:
    w: str
    v1: str
    v2: str
    v3: str
    v4: str
    date: date
    id: int | None = None

    #перевод в словарь
    def to_dict(self) -> dict:
        return {
            'id': self.id,
            'w': self.w,
            'v1': self.v1,
            'v2': self.v2,
            'v3': self.v3,
            'v4': self.v4,
            'date': self.date.isoformat()
        }

    def to_dict_vars(self) -> dict:
        w_v = self.to_dict()
        return {k: w_v[k] for k in VARIANTS}

    def to_dict_w(self) -> dict:
        return {'w' : self.w} | self.to_dict_vars()

    #из словаря в класс
    @classmethod
    def from_dict(cls, data: dict) -> 'Word':
        d = data['date']
        if isinstance(d, str):
            d = date.fromisoformat(d)
        return cls(
            id=data.get('id'),
            w=data['w'],
            v1=data['v1'],
            v2=data['v2'],
            v3=data['v3'],
            v4=data['v4'],
            date=d
        )

    #из sql в класс
    @classmethod
    def from_row(cls, row: sqlite3.Row) -> 'Word':
        return cls.from_dict(dict(row))


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
    QPushButton:disabled {{
        background-color: #cccccc;
    }}
    """


'''Вспомогательная функция для рамок'''
def sub_str(outline_c='#3c30e3', w_c='#07fc03'):
    return f""" 
    QLineEdit {{
        border: 1px solid {outline_c};
        color: {w_c};
    }}
    """

'''Вспомогательная функция для лэйблов'''
def sub_str_label(v_c='#3c30e3', c='#000000'):
    return f"""
    QLabel {{
        background-color: #ffffff;
        color: {c};
        font-size: 14px;
        border: 2px solid {v_c};
    }}
    QLabel:hover {{
        color: #3c30e3;
    }}
    QLabel:pressed {{
        color: {v_c};
    }}
    """