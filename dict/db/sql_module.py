'''
Модуль для классов, связанных с базой данных
'''

'''Импорты'''
import sqlite3

from datetime import date
from pathlib import Path

from ..consts import Word
from ..config import DB_PATH

'''Класс для работы с БД'''
class Storage:
    ORDER_OPTIONS = {
        'date_asc': 'date ASC, id DESC',
        'date_desc': 'date DESC, id DESC',
        'w_asc': ' w ASC',
        'w_desc': 'w DESC'
    }

    LIMIT_OPTION = {
        '10w': '10',
        '20w': '20',
        '30w': '30'
    }

    def __init__(self, db_path: str | Path = DB_PATH):
        self.db_path = Path(db_path)
        self.db_path.parent.mkdir(parents=True, exist_ok=True)
        self.conn = sqlite3.connect(str(self.db_path))
        self.conn.row_factory = sqlite3.Row
        self.create_db()

    #создание БД
    def create_db(self):
        self.conn.executescript("""
            CREATE TABLE IF NOT EXISTS words (
                id   INTEGER PRIMARY KEY AUTOINCREMENT,
                w    TEXT NOT NULL,
                v1   TEXT NOT NULL,
                v2   TEXT NOT NULL,
                v3   TEXT NOT NULL,
                v4   TEXT NOT NULL,
                date TEXT NOT NULL
            );
            CREATE INDEX IF NOT EXISTS idx_date ON words(date);
        """)
        self.conn.commit()

    #запись
    def add(self, word: Word):
        with self.conn:
            cursor = self.conn.execute(
                """
                INSERT INTO words (w, v1, v2, v3, v4, date)
                VALUES (?, ?, ?, ?, ?, ?)
                """,
                (
                    word.w,
                    word.v1, word.v2, word.v3, word.v4,
                    word.date.isoformat(),
                ),
            )
            return cursor.lastrowid

    #удаление
    def delete(self, w_id: int):
        with self.conn:
            self.conn.execute(
                'DELETE FROM words WHERE id = ?', (w_id,)
            )

    #чтение всей БД
    def get_all(self, ord_by: str ='date_desc') -> list[Word]:
        ord_id = self.ORDER_OPTIONS.get(ord_by)
        if ord_id is None:
            raise ValueError('Ээээ бля пропиши как')
        cursor = self.conn.execute(
            f"SELECT id, w, v1, v2, v3, v4, date FROM words ORDER BY {ord_id}"
        )
        return [self.row_to_word(row) for row in cursor]

    #чтение не всей БД
    def get_by_date(self, start: date, end: date, lmt: str = '10d') -> list[Word]:
        lmt_id = self.LIMIT_OPTION.get(lmt)
        if lmt_id is None:
            raise ValueError('Дни укажи, сука')
        cursor = self.conn.execute(
            f"""
            SELECT id, w, v1, v2, v3, v4, date 
            FROM words
            WHERE date BETWEEN ? and ?
            LIMIT {lmt_id}
            """,
            (start.isoformat(), end.isoformat()),
        )
        return [self.row_to_word(row) for row in cursor]

    #конвертация
    def row_to_word(self, row: sqlite3.Row) -> Word:
        return Word(
            id=row['id'],
            w=row['w'],
            v1=row['v1'],
            v2=row['v2'],
            v3=row['v3'],
            v4=row['v4'],
            date=date.fromisoformat(row["date"]),
        )

    #закрытие
    def close(self):
        self.conn.close()