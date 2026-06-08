from PyQt6.QtWidgets import *
from PyQt6.uic import loadUi
from app.database.locker_repository import LockerRepository
from app.database.user_repository import UserRepository


class LockerService:


    def __init__(self):

        self.locker_repo = LockerRepository()
        self.user_repo = UserRepository()


    def check_user_has_locker(self, mssv):
        return self.locker_repo.get_user_locker(mssv)


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

        self.user_repo.update_account_status(mssv)

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

        self.user_repo.update_account_status(mssv)

        self.locker_repo.return_locker(mssv, locker_id, name)

        return (
            True,
            f"Trả tủ {locker_id} thành công!"
        )





    def get_locker_status(self, locker_id):
        lockers = self.get_all_lockers()

        for id_, status, holder in lockers:
            if id_ == locker_id:
                return status, holder

        return None, None

    def get_all_lockers(self):

        return self.locker_repo.get_all_lockers()
    
    def set_status_locker(self, user, locker_id, name):
        
        print("SERVICE RUNNING")

        return self.locker_repo.set_status_locker(user, locker_id, name)
    

####################################################################
########################  SERVICE ENGINEER  ########################
####################################################################


    def insert_service_log(self, locker_id, ktv_id, ktv_name, action):
        """
        Ghi log hành động của service engineer
        """
        return self.locker_repo.insert_service_log(
            locker_id, ktv_id, ktv_name, action
        )
    
    
    def update_locker_maintenance(self, locker_id, status):
        """
        Gọi repository để cập nhật trạng thái bảo trì
        """
        return self.locker_repo.update_locker_maintenance(locker_id, status)

