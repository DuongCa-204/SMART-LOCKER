from app.database.user_repository import UserRepository
from datetime import datetime, timedelta
from app.utils.session import Session
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
        
        if user[3] == 0:
            return (
                False, "Tài khoản đang chờ phê duyệt"
            )
        
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
                "Đăng kí tài khoảng thành công"
            )


        return(
            False,
            "TÀI KHOẢNG ĐÃ TỒN TẠI"
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

        # Gửi mã otp về Email
        # sử dụng app_password của gamil gửi
        # catanduong78@gmail.com
        from app.config import (
            EMAIL_SENDER,
            EMAIL_PASSWORD
        )

        sender = EMAIL_SENDER
        password = EMAIL_PASSWORD

        # câu trúc f" " -> cho phép chèn biến vào trong chuỗi  => ở đây chèn thêm otp
        msg = f"Subject: Smart Locker\n\nYour locker PIN is {otp}"

        # tạo kết nối đến mail server
        # cấu trúc smtplib.SMTP(server_address, port)
        # erver_address : địa chỉ server SMTP của Gmail
        # port          : cổng gửi email
        server = smtplib.SMTP("smtp.gmail.com",587)
        # bật mã hóa TLS ( mục đích: mã hóa dữ liệu trước khi gửi email)
        server.starttls()
        # đăng nhập gmail => gg không cho đăng nhập bằng mật khẩu của tk thật
        server.login(sender,password)
        server.sendmail(sender,email,msg)
        # ngắt kết nối SMTP server
        server.quit() 

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
            "Xác thực thành công",


        )