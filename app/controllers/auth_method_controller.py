from PyQt6 import QtCore, QtGui, QtWidgets, uic
from PyQt6.QtWidgets import *
from PyQt6.QtCore import QTimer, pyqtSignal, QUrl, QObject
from PyQt6.uic import loadUi


from app.utils.session import Session
from app.services.locker_service import LockerService
from app.controllers.login_controller import LoginController
from app.controllers.register_controller import RegisterController



class AuthMethodController(QMainWindow):

    def __init__(self,stacked_widget):

        super().__init__()

        uic.loadUi("app/ui/AUTH_METHOD.ui", self)
        self.stacked_widget = stacked_widget

        self.locker_service = LockerService()


        ########### SETUP BUTTON ###########
        for btn in [self.pass_select, self.recog_select]:
            btn.setCheckable(True)
            btn.setAutoExclusive(False)

            def create_release_handler(b=btn):
                def safe_clear():
                    try:
                        if b and not b.isHidden():
                            b.setChecked(False)
                    except RuntimeError:
                        pass
                QTimer.singleShot(150, safe_clear)

            btn.released.connect(create_release_handler)


        ########### EVENT ############
        self.pass_select.clicked.connect(self.go_to_password)
        self.recog_select.clicked.connect(self.go_to_sign_in)

    def go_to_password(self):

        QTimer.singleShot(150, lambda: self.stacked_widget.setCurrentIndex(9))

    def go_to_sign_in(self):

        QTimer.singleShot(150, lambda: self.stacked_widget.setCurrentIndex(2))
 





    



