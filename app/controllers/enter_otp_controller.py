from PyQt6.QtWidgets import QMainWindow
from PyQt6 import uic
from PyQt6.QtCore import QTimer

from app.utils.session import Session
from app.services.auth_service import AuthService
from app.services.locker_service import LockerService

class EnterEmailController(QMainWindow):

    def __init__(self, stacked_widget):

        super().__init__()

        uic.loadUi(
            "app/ui/ENTER_OTP.ui",
            self
        )

        self.stacked_widget = stacked_widget

        self.auth_service = AuthService()
        self.locker_service = LockerService()

        # EVENT

        self.pin =""

        # kết nối nút nhấn 
        self.b1.clicked.connect(lambda: self.add_number("1"))
        self.b2.clicked.connect(lambda: self.add_number("2"))
        self.b3.clicked.connect(lambda: self.add_number("3"))
        self.b4.clicked.connect(lambda: self.add_number("4"))
        self.b5.clicked.connect(lambda: self.add_number("5"))
        self.b6.clicked.connect(lambda: self.add_number("6"))
        self.b7.clicked.connect(lambda: self.add_number("7"))
        self.b8.clicked.connect(lambda: self.add_number("8"))
        self.b9.clicked.connect(lambda: self.add_number("9"))
        self.b0.clicked.connect(lambda: self.add_number("0"))

        self.clear_b.clicked.connect(self.clear_def)
        self.enter_b.clicked.connect(self.check_otp)


    # hàm xóa mã pin
    def clear_def(self):
        self.pin =""
        self.update_lable()

    # (self,number): self nơi con trỏ chỉ tới và number là tham số được đưa vào
    def add_number(self, number):
        
        # giới hạn độ dài của mã pin
        if len(self.pin) < 4:
            self.pin += number
            self.update_lable()

    def update_lable(self):

        lable = [self.l1, self.l2, self.l3, self.l4]
        for i in range(4):
            if i < len(self.pin):
                lable[i].setText("*")
            else:
                lable[i].setText("-")

    def check_otp(self):

        otp_input = self.pin

        success, message = (
            self.auth_service.verify_otp(
                otp_input
            )
        )

        if success:

            self.thong_bao_otp.setStyleSheet(
                "color: green;"
            )

            self.thong_bao_otp.setText(message)
            QTimer.singleShot(1000, self.after_enterotp_success)

        else:

            self.thong_bao_otp.setStyleSheet(
                "color: red;"
            )

            self.thong_bao_otp.setText(message)

    def after_enterotp_success(self):

        locker = self.locker_service.check_user_has_locker(
            Session.current_user
        )

        # Đã có tủ
        if locker:

            self.stacked_widget.setCurrentIndex(3)
            # trang OPEN / RETURN

        # Chưa có tủ
        else:

            self.stacked_widget.setCurrentIndex(10)
            # trang SEND LOCKER


    def showEvent(self, event):

        self.pin = ""
        self.thong_bao_otp.setText("")

        self.update_lable()

        super().showEvent(event)