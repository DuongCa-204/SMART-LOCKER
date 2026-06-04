from PyQt6 import uic
from PyQt6.QtWidgets import QMainWindow
from PyQt6.QtCore import QTimer, Qt
from app.services.locker_service import LockerService
from app.controllers.button import ClickableLabel
import os
from PyQt6.QtGui import QPixmap

BASE_DIR = os.path.dirname(os.path.abspath(__file__))  # thư mục chứa begin_controller.py

class BeginController(QMainWindow):

    def __init__(self, stacked_widget):
        super().__init__()

        uic.loadUi("app/ui/test_bg.ui", self)
        self.stacked_widget = stacked_widget
        self.locker_service = LockerService()

        # Ép kiểu QLabel từ file .ui thành ClickableLabel
        for attr in ["login_b", "sign_in"]:
            label = getattr(self, attr)
            label.__class__ = ClickableLabel
            label.setCursor(Qt.CursorShape.PointingHandCursor)
            label.original_style = label.styleSheet()

        # self.service_button.clicked.connect(self.go_to_service)
        self.login_b.clicked.connect(self.go_to_login)
        self.sign_in.clicked.connect(self.go_to_sign_in)

        # Load QSS
        try:
            with open("app/assets/styles/keyboard.qss", "r", encoding="utf-8") as f:
                self.setStyleSheet(f.read())
        except FileNotFoundError:
            print("Lưu ý: Không tìm thấy file QSS!")

    # def go_to_service(self):
    #     QTimer.singleShot(150, lambda: self.stacked_widget.setCurrentIndex(10))

    def go_to_login(self):
        QTimer.singleShot(150, lambda: self.stacked_widget.setCurrentIndex(1))

    def go_to_sign_in(self):
        QTimer.singleShot(150, lambda: self.stacked_widget.setCurrentIndex(2))


        # Load SVG vào label — chỉnh width/height theo kích thước thực tế
        self._set_icon(self.login_b,  "D:/SML/app/assets/icon/feather-main/icons/airplay.svg",  120, 40)
        self._set_icon(self.sign_in,  "D:/SML/app/assets/icon/feather-main/icons/activity.svg", 120, 40)

    def _set_icon(self, label, relative_path, width, height):
        path = os.path.join(BASE_DIR, relative_path)
        if not os.path.exists(path):
            print(f"Không tìm thấy icon: {path}")
            return
        pixmap = QPixmap(path)
        label.setPixmap(
            pixmap.scaled(
                width, height,
                Qt.AspectRatioMode.KeepAspectRatio,
                Qt.TransformationMode.SmoothTransformation
            )
        )