import sys
from PyQt6.QtWidgets import QApplication
from dict.ui.main_window import MainWindow
from .db.sql_module import Storage

def run():
    app = QApplication(sys.argv)
    app.setApplicationName('Dict')

    storage = Storage()
    window = MainWindow(storage)
    window.show()

    app.aboutToQuit.connect(storage.close)
    return app.exec()