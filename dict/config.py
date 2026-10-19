from pathlib import Path

APP_NAME = "Dict"

BASE_DIR = Path(__file__).resolve().parent
DB_DIR = BASE_DIR / 'db'
DB_PATH = DB_DIR / 'data.db'