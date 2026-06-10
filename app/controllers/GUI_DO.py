from PyQt6.QtWidgets import QMainWindow
from PyQt6 import uic

from app.utils.session import Session
from app.services.auth_service import AuthService
from app.services.locker_service import LockerService
from PyQt6.QtCore import QTimer


class SelectMode_GUIDOController(QMainWindow):

    def __init__(self,stacked_widget, loading_page, success_page):

        super().__init__()

        uic.loadUi("app/ui/MODE_GUIDO.ui", self)
        self.stacked_widget = stacked_widget
        self.loading_page = loading_page
        self.success_page = success_page
        self.locker_service = LockerService()
        self.auth_service = AuthService()


        ########### SETUP BUTTON ###########
        self.gui_do.setCheckable(True)
        self.gui_do.setAutoExclusive(False)

        def create_release_handler(b=self.gui_do):
            def safe_clear():
                try:
                    if b and not b.isHidden():
                        b.setChecked(False)
                except RuntimeError:
                    pass
            QTimer.singleShot(150, safe_clear)

        self.gui_do.released.connect(create_release_handler)



        ########### EVENT ###########
        self.gui_do.clicked.connect(self.GUI_DO)


    def GUI_DO(self):

        user = Session.current_user


        success, message = (
            self.locker_service.borrow_locker(user)
        )

        if not success:

            self.thong_bao_tu.setStyleSheet(
                "color: red;"
            )

            self.thong_bao_tu.setText(message)

            return

        # ===== HIỆN LOADING =====
        else:
            self.loading_page.set_message(
                "Đang kiểm tra tủ trống..."
            )

            self.stacked_widget.setCurrentWidget(
                self.loading_page
            )

            # ===== SAU 1 GIÂY =====

            QTimer.singleShot(2000,lambda: self.show_success(
                "Kiểm tra thành công",
                self.go_to_select_locker
                )
            )

    def go_to_begin(self):
        self.stacked_widget.setCurrentIndex(0)
        self.reset_form()

    def go_to_select_locker(self):
        self.stacked_widget.setCurrentIndex(4)
        self.reset_form()

    def reset_form(self):
        self.thong_bao_tu.setText("")




    def show_success(
        self,
        message,
        next_function,
        delay= 2000
    ):

        self.success_page.set_message(
            message
        )

        self.stacked_widget.setCurrentWidget(
            self.success_page
        )

        QTimer.singleShot(
            delay,
            next_function
        )
