"""
main_window.py
by Charles V
Picatso main window layout.
"""

import random

import requests
from PySide6.QtCore import Qt
from PySide6.QtGui import QPixmap
from PySide6.QtWidgets import (
    QFrame,
    QHBoxLayout,
    QLabel,
    QMainWindow,
    QPushButton,
    QVBoxLayout,
    QWidget,
)
from utils import controller


class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Picatso")
        self.setContentsMargins(12, 12, 12, 12)
        self.resize(480, 400)
        self.fetching = False

        layout = QVBoxLayout()

        # Image + Palette row
        image_row = QHBoxLayout()

        self.image_label = QLabel()
        self.image_label.setFixedSize(280, 280)
        self.image_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.image_label.setText("No image yet")

        # color palette
        palette_layout = QVBoxLayout()
        palette_layout.setSpacing(6)
        self.swatches = []
        for _ in range(4):
            swatch = QLabel()
            swatch.setFixedSize(80, 80)
            swatch.setStyleSheet("background-color: #000")
            self.swatches.append(swatch)
            palette_layout.addWidget(swatch)

        image_row.addWidget(self.image_label)
        image_row.addLayout(palette_layout)

        # button
        self.fetch_button = QPushButton("Give me a cat!")
        self.fetch_button.clicked.connect(self.fetch_image)

        layout.addLayout(image_row)
        layout.addWidget(self.fetch_button)
        layout.addStretch()

        widget = QWidget()
        widget.setLayout(layout)
        self.setCentralWidget(widget)

    def fetch_image(self):
        # checks if image is already being fetched and disables if so, otherwise allows and fetches
        if self.fetching:
            return
        self.fetching = True
        self.fetch_button.setEnabled(False)
        self.image_label.setText("Catching...")

        result = controller.make_api_call(
            "https://cataas.com/", "cat", "?type=square&position=center&json=true"
        )
        if result.startswith("ERROR"):
            self.image_label.setText(result)
        else:
            image_url = controller.get_image_url_from_json(result)
            response = requests.get(image_url)
            pixmap = QPixmap()
            pixmap.loadFromData(response.content)
            self.image_label.setPixmap(
                pixmap.scaled(
                    280,
                    280,
                )
            )
        self.fetching = False
        self.fetch_button.setEnabled(True)
