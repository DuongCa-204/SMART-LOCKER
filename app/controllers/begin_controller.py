from PyQt6 import uic
from PyQt6.QtWidgets import QMainWindow
from PyQt6.QtCore import QTimer


class BeginController(QMainWindow):

    def __init__(self, stacked_widget):
        super().__init__()

        uic.loadUi("app/ui/test_bg.ui", self)
        self.stacked_widget = stacked_widget

        # EVENT
        self.login_b.clicked.connect(self.go_to_login)
        self.sign_in.clicked.connect(self.go_to_sign_in)
        self.service_button.clicked.connect(self.go_to_service)

    def go_to_login(self):
        QTimer.singleShot(150, lambda: self.stacked_widget.setCurrentIndex(1))

    def go_to_sign_in(self):
        QTimer.singleShot(150, lambda: self.stacked_widget.setCurrentIndex(2))

    def go_to_service(self):
        QTimer.singleShot(150, lambda: self.stacked_widget.setCurrentIndex(13))