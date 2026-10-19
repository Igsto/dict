'''
В данном файле лежат важные константы
'''

from dataclasses import dataclass
from datetime import date
import sqlite3

VARIANTS = [f'v{i+1}' for i in range(4)]

@dataclass
class Word:
    w: str
    v1: str
    v2: str
    v3: str
    v4: str
    date: date
    id: int | None = None

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

    @classmethod
    def from_row(cls, row: sqlite3.Row) -> 'Word':
        return cls.from_dict(dict(row))