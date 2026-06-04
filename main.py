import traceback, sys

# def excepthook(exc_type, exc_value, exc_tb):
#     traceback.print_exception(exc_type, exc_value, exc_tb)
#     input("Nhấn Enter để thoát...")  # giữ cửa sổ lại

# sys.excepthook = excepthook

# import sys

from PyQt6.QtWidgets import QApplication, QStackedWidget
from PyQt6.QtCore import QTimer, pyqtSignal, QUrl, QObject, QEvent

from app.controllers.login_controller import LoginController
from app.controllers.begin_controller import BeginController
from app.controllers.select_locker_controller import SelectLockerController
from app.controllers.register_controller import RegisterController
from app.controllers.select_mode import SelectModeController
from app.controllers.loading_controller import LoadingController
from app.controllers.success_controller import SuccessController
from app.controllers.video import VideoScreenController
from app.controllers.auth_method_controller import AuthMethodController 
from app.controllers.password_controller import PassWordController
from app.controllers.service_controller import ServiceController
from app.controllers.GUI_DO import SelectMode_GUIDOController
from app.controllers.send_otp_controller import SendEmailController
from app.controllers.enter_otp_controller import EnterEmailController
from app.controllers.service_controller import ServiceController
from app.controllers.menu_service import MenuServiceController
from app.database.database import Database
from app.database.locker_repository import LockerRepository
from PyQt6.QtGui import QMovie



app = QApplication(sys.argv)



######   TIMERS
idle_timer = QTimer()
timer_cleanup = QTimer()

######   GLOBAL EVENT FILTER
class GlobalFilter(QObject):

    def eventFilter(self, obj, event):

        if event.type() in [
            QEvent.Type.MouseButtonPress,
            QEvent.Type.KeyPress
        ]:
            idle_timer.start(60000)
        return super().eventFilter(obj, event)
    
######   INSTALL FILTER
filter = GlobalFilter()
# cài vào app
app.installEventFilter(filter)   







# STACK WIDGET
stacked_widget = QStackedWidget()


# CREATE PAGES


begin_page = BeginController(stacked_widget)
login_page = LoginController(stacked_widget)
register_page = RegisterController(stacked_widget)
loading_page = LoadingController()
success_page = SuccessController()
select_page = SelectLockerController(stacked_widget, loading_page, success_page)
select_mode = SelectModeController(stacked_widget, loading_page, success_page)
video_page = VideoScreenController(stacked_widget)
auth_method_page = AuthMethodController(stacked_widget)
password_page = PassWordController(stacked_widget)
service_page = ServiceController(stacked_widget)
select_guido = SelectMode_GUIDOController(stacked_widget, loading_page, success_page)
sendOTP_page = SendEmailController(stacked_widget)
enterOTP_page = EnterEmailController(stacked_widget)
service_page = ServiceController(stacked_widget)
menu_service = MenuServiceController(stacked_widget, loading_page, success_page)
# ADD PAGE TO STACK


stacked_widget.addWidget(begin_page)                #0
stacked_widget.addWidget(login_page)                #1
stacked_widget.addWidget(register_page)             #2
stacked_widget.addWidget(select_mode)               #3
stacked_widget.addWidget(select_page)               #4
stacked_widget.addWidget(loading_page)              #5
stacked_widget.addWidget(success_page)              #6
stacked_widget.addWidget(video_page)                #7
stacked_widget.addWidget(auth_method_page)          #8
stacked_widget.addWidget(password_page)             #9
stacked_widget.addWidget(select_guido)              #10
stacked_widget.addWidget(sendOTP_page)              #11
stacked_widget.addWidget(enterOTP_page)             #12
stacked_widget.addWidget(service_page)              #13
stacked_widget.addWidget(menu_service)              #14
##############################

def back_to_video():

    idle_timer.stop()
    stacked_widget.setCurrentWidget(
        video_page
    )

    video_page.player.setPosition(0)

    video_page.player.play()

def show_begin():

    stacked_widget.setCurrentWidget(begin_page)
    idle_timer.start(60000)


# ===== TIMER CLEANUP =====
# cleanup_users()
video_page.touched.connect(show_begin)
idle_timer.timeout.connect(back_to_video)
# timer_cleanup.timeout.connect(cleanup_users)



timer_cleanup.start(60000)  # 60s (ms)
# giữ reference để không bị mất
# stacked_widget.cleanup_timer = timer_cleanup


# WINDOW SETTING
stacked_widget.setFixedHeight(600)

stacked_widget.setFixedWidth(1024)


# START PAGE
stacked_widget.setCurrentIndex(7)


stacked_widget.show()


sys.exit(app.exec())