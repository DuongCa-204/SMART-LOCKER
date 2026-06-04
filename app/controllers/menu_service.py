from PyQt6.QtWidgets import QMainWindow, QMessageBox
from PyQt6 import uic

from app.utils.session import Session
from app.services.locker_service import LockerService
from app.services.auth_service import AuthService
from app.widgets.locker_button import LockerButton
from datetime import datetime
from PyQt6.QtCore import QTimer



class MenuServiceController(QMainWindow):

    def __init__(self, stacked_widget, loading_page, success_page):

        super().__init__()

        uic.loadUi("app/ui/MENU_SE.ui", self)

        self.loading_page = loading_page
        self.success_page = success_page
        self.stacked_widget = stacked_widget
        self.locker_service = LockerService()
        self.auth_service = AuthService()

        Session.selected_locker = None
        self.locker_buttons = []
        self.load_style()
        self.setup_locker_buttons()

        # self.load_locker_status()

        self.back.clicked.connect(self.go_back)
        self.chon_tu.clicked.connect(self.confirm_action)

    # ================= STYLE =================
    def load_style(self):
        with open("app/assets/styles/locker.qss", "r") as file:
            self.setStyleSheet(file.read())
    # ================= SETUP BUTTONS =================
    def setup_locker_buttons(self):
    # Loop từ 1 tới 9
        for i in range(1, 10):
            
            # 1. Lấy nút cũ từ UI (old_btn = self.tu1, self.tu2, ...)
            old_btn = getattr(self, f"tu{i}")
            
            # 2. Tạo LockerButton mới
            new_btn = LockerButton(i)
            
            # 3. Copy properties từ nút cũ sang nút mới
            #    - setParent()
            #    - setGeometry()
            #    - setFont()
            new_btn.setParent(old_btn.parent())
            new_btn.setGeometry(old_btn.geometry())
            new_btn.setFont(old_btn.font())
            new_btn.show()
            
            # 4. Xóa nút cũ
            old_btn.deleteLater()
            
            # 5. Gắn nút mới vào self (self.tu1 = new_btn)
            setattr(self, f"tu{i}", new_btn)
            
            # 6. Thêm vào danh sách
            self.locker_buttons.append(new_btn)
            
            # 7. Kết nối signal click
            new_btn.clicked.connect(
                lambda _, btn=new_btn:
                self.highlight_locker(btn.locker_id, btn)
            )
    # ================= LOAD STATUS =================
    def load_locker_status(self):
        """
        Setup các tủ để test
        Vì đây chỉ là test, tất cả tủ đều available
        """
        # Loop qua tất cả button đã tạo
        for button in self.locker_buttons:
            # Đặt tất cả button thành trạng thái available (xanh)
            button.set_available()
    # ================= EVENT =================
    def showEvent(self, event):
        """
        Gọi tự động khi trang được hiển thị
        """
        # Setup các tủ để test
        self.load_locker_status()
        
        # Gọi parent showEvent
        super().showEvent(event)


    def highlight_locker(self, locker_id, button_obj):
        """
        Xử lý khi user click chọn tủ
        """
        # Vì đây là test, tất cả button đều enabled, nên không cần check
        # Nhưng vẫn kiểm tra để an toàn
        if not button_obj.isEnabled():
            return
        
        # Reset tất cả button
        self.load_locker_status()
        
        # Highlight tủ được chọn
        Session.selected_locker = locker_id
        button_obj.set_selected()
        
        # Update thông báo (nếu có label)
        self.thong_bao_tu.setText(f"Đã chọn tủ {locker_id}")
        self.thong_bao_tu.setStyleSheet("color: #00796B;")
    
    def confirm_action(self):
        """
        Khi user nhấn nút OPEN - mở tủ ngay
        """
        
        # 1. Validation: Có chọn tủ chưa?
        if not Session.selected_locker:
            QMessageBox.warning(self, "Lỗi", "Vui lòng chọn tủ!")
            return
        
        # 2. ========== SỬAT CÁCH LẤY THÔNG TIN ==========
        # Dùng thông tin KTV từ Session (không phải user thường)
        locker_id = Session.selected_locker
        ktv_id = Session.ktv_id  # ✅ ID KTV (ví dụ: "KTV001")
        ktv_name = Session.ktv_name  # ✅ Tên KTV (ví dụ: "Kỹ Thuật Viên")
        
        # 3. Gọi service để mở tủ
        # ❓ TODO: Sửa dòng này - hiện tại nó dùng `user` và `name`
        # self.locker_service.set_status_locker(user, locker_id, name)
        # ✅ Sửa thành:
        self.locker_service.set_status_locker(ktv_id, locker_id, ktv_name)
        
        # 4. Show MessageBox thành công
        QMessageBox.information(
            self,
            "Thành công",
            f"Mở tủ {locker_id} thành công!"
        )
        
        # 5. Reset form
        self.reset_form()
        self.load_locker_status()
        # ==========================================
    
    def go_to_begin(self):
        """Quay lại trang BEGIN"""
        self.stacked_widget.setCurrentIndex(0)
        self.reset_form()

    def go_back(self):
        """Quay lại trang SERVICE (hoặc trang trước)"""
        # TODO: Điều chỉnh index tùy theo flow của bạn
        self.stacked_widget.setCurrentIndex(0)  # Xác định index
        self.reset_form()

    def reset_form(self):
        """Xóa dữ liệu khi thoát trang"""
        Session.selected_locker = None
        self.thong_bao_tu.clear()