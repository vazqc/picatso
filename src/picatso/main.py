"""
Picatso
By Charles V
Make your own Picatso with this random cat and color palette generator!
"""

import sys

from PySide6.QtWidgets import QApplication
from ui.main_window import MainWindow

if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = MainWindow()
    window.show()

    app.exec()
