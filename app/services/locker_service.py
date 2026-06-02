from PyQt6 import QtCore, QtGui, QtWidgets, uic
from PyQt6.QtWidgets import *
from PyQt6.QtCore import QTimer, pyqtSignal, QUrl, QObject
from PyQt6.uic import loadUi
import sys
import MySQLdb as mdb
import random
import secrets
import smtplib
import os
import sqlite3

from app.database.locker_repository import LockerRepository
from app.database.user_repository import UserRepository
from app.utils.session import Session

class LockerService:


    def __init__(self):

        self.locker_repo = LockerRepository()
        self.user_repo = UserRepository()


    def check_user_has_locker(self, mssv):
        locker = self.locker_repo.get_user_locker(mssv)

        if locker:
            return locker[0]

        return None



    def borrow_locker(self, mssv):

        locker_id = self.check_user_has_locker(mssv)

        if locker_id:
            return (
                False,
                f"Bạn đang sử dụng tủ {locker_id}. Vui lòng trả tủ trước!!!"
            )


        available_locker = (
            self.locker_repo.has_available_locker()
        )

        if not available_locker:

            return (
                False,
                "Không còn tủ trống!"
            )
        

        return (
            True,
            "Đang vào giao diện chọn tủ "
        )





    def open_locker(self, mssv, name):

        locker_id = self.check_user_has_locker(mssv)
    
        if not locker_id:

            return (
                False,
                "Bạn chưa sử dụng tủ nào!"
            )

        # TODO:
        # gửi lệnh mở tủ cho ESP32

        self.locker_repo.insert_access_log(
            locker_id,
            mssv,
            "OPEN",
            name
        )

        return (
            True,
            f"Mở tủ {locker_id} thành công!"
        )
    



    def return_locker(self, mssv, name):

        locker_id = (
            self.check_user_has_locker(mssv)
        )

        if not locker_id:

            return (
                False,
                "Không tìm thấy tủ!"
            )

        # TODO:
        # kiểm tra trạng thái đóng cửa

        self.locker_repo.TRATU(mssv, locker_id, name)



        return (
            True,
            f"Trả tủ {locker_id} thành công!"
        )

    # def update_LockerLog(self, mssv, name):

    #     locker_id = self.check_user_has_locker(mssv)

    #     self.locker_repo.insert_access_log(
    #         locker_id,
    #         mssv,
    #         "OPEN",
    #         name
    #     )

    def get_available_lockers(self):
        return self.locker_repo.get_available_lockers()
    


    def borrow_specific_locker(
        self,
        locker_id,
        user
    ):

        status = self.locker_repo.get_locker_status(
            locker_id
        )

        if status == "Busy":
            return False, "Tủ đã có người dùng"

        # self.locker_repo.assign_locker(
        #     locker_id,
        #     user
        # )

        return True, "Mượn tủ thành công"


    def get_locker_status(self, locker_id):
        lockers = self.get_all_lockers()

        for id_, status, holder in lockers:
            if id_ == locker_id:
                return status, holder

        return None, None

    def get_all_lockers(self):

        return self.locker_repo.get_all_lockers()
    
    def set_status_locker(self, user, locker_id, name):

        return self.locker_repo.set_status_locker(user, locker_id, name)
    
    def last_active_time(self,mssv, locker_id, name):

        return self.locker_repo.insert_access_log(
            locker_id,
            mssv,
            "BORROW",
            name)
