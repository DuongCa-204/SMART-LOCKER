from PyQt6.QtWidgets import QMainWindow
from PyQt6 import uic
from PyQt6.QtGui import QMovie
from PyQt6.QtCore import QSize

class SuccessController(QMainWindow):

    def __init__(self):

        super().__init__()

        uic.loadUi(
            "app/ui/SUCCESS.ui",
            self
        )

        self.movie = QMovie(
            "app/assets/gif/success.gif"
        )

        # self.movie.setScaledSize(
        #     QSize(180, 180)
        # )

        self.success_gif.setMovie(
            self.movie
        )

        self.movie.start()

    def set_message(self, text):

        self.success_text.setText(text)