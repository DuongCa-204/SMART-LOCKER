from app.database.user_repository import UserRepository
from datetime import datetime, timedelta
from app.utils.session import Session
from app.config import EMAIL_SENDER, EMAIL_PASSWORD
import secrets
import smtplib


class AuthService:

    def __init__(self):

        self.user_repo = UserRepository()


    def login(self, mssv):

        user = self.user_repo.find_user(mssv)

        if not user:
            return (
                False,
                "Chưa đăng ký tài khoản"
            )
        
        if user['is_approved'] == 0:
            return (
                False, "Tài khoản đang chờ phê duyệt"
            )


        ####  LỰA CHỌN KHI INACTIVE (USER ĐƯỢC TIẾP TỤC/ PHẢI BÁO ADMIN)
        if user['account_status'] == 'DELETED':
            return (False, "Tài khoản đã bị khóa, vui lòng liên hệ admin")
            
            
        return (
            True,
            "Đăng nhập thành công"
        )
    
    def password(self, mssv, pass_account):

        user = self.user_repo.find_password(mssv, pass_account)

        if not user:
            return (
                False,
                "NHẬP SAI MẬT KHẨU"
            )

        return (
            True,
            "Truy cập thành công"
        )

    def register(self, mssv, name, email, password):

        user = self.user_repo.user_exists(mssv, email)

        if not user:
            
            self.user_repo.create_user(mssv, name, email, password)

            return (
                True,
                "Đăng kí tài khoản thành công"
            )


        return(
            False,
            "TÀI KHOẢN ĐÃ TỒN TẠI"
        )
    
    def get_name_user(self, mssv):
        return self.user_repo.get_name_by_mssv(mssv)

    def get_email_user(self, mssv):

        return self.user_repo.get_email_by_mssv(mssv)

    def send_otp_to_email(self, email):
    
        # random otp
        otp = str(secrets.randbelow(9000)+1000)
        # tạo ra số nguyên ngẫu nhiên nhỏ hơn 9000
        # + 1000 để đảm bảo có đủ 4 chữ số
        # câu trúc f" " -> cho phép chèn biến vào trong chuỗi  => ở đây chèn thêm otp
        msg = f"Subject: Smart Locker\n\nYour locker PIN is {otp}"

        # Gửi mã otp về Email
        # sử dụng app_password của gamil gửi
        # catanduong78@gmail.com
        # tạo kết nối đến mail server
        # cấu trúc smtplib.SMTP(server_address, port)
        # erver_address : địa chỉ server SMTP của Gmail
        # port          : cổng gửi email
        try:
            server = smtplib.SMTP("smtp.gmail.com", 587)
            server.starttls()
            server.login(EMAIL_SENDER, EMAIL_PASSWORD)
            server.sendmail(EMAIL_SENDER, email, msg)
            server.quit()
        except Exception as e:
            print(f"Lỗi gửi email: {e}")
            return (False, "Gửi OTP thất bại, vui lòng thử lại")


        Session.current_otp = otp

        Session.otp_expire_time = (
            datetime.now()
            + timedelta(seconds=30)
        )

        return (
            True,
            "Đã gửi OTP"
        )
        
    def verify_otp(self, otp_input):



        if Session.current_otp is None:

            return (
                False,
                "Chưa tạo OTP"
            )

        if datetime.now() > Session.otp_expire_time:

            Session.current_otp = None
            Session.otp_expire_time = None

            return (
                False,
                "OTP đã hết hạn"
            )

        if str(otp_input).strip() != str(Session.current_otp).strip():

            return (
                False,
                "OTP không đúng"
            )

        Session.current_otp = None
        Session.otp_expire_time = None


        return (
            True,
            "Xác thực thành công"

        )