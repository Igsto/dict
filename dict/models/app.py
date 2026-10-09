import sys
from PyQt6.QtWidgets import QApplication
from dict.ui.main_window import MainWindow

def run():
    app = QApplication(sys.argv)
    app.setApplicationName('Dict')

    window = MainWindow()
    window.show()

    return app.exec()