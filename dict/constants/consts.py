'''
В данном файле лежат важные константы
'''

from dataclasses import dataclass
from datetime import date

VARIANTS = [f'v{i+1}' for i in range(4)]

@dataclass
class Entry:
    w: str
    v1: str
    v2: str
    v3: str
    v4: str
    date: date
    id: int | None = None