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

        self.pass_select.clicked.connect(self.go_to_password)
        self.recog_select.clicked.connect(self.go_to_sign_in)

    def go_to_password(self):

        self.stacked_widget.setCurrentIndex(9)

    def go_to_sign_in(self):

        self.stacked_widget.setCurrentIndex(2)







    



