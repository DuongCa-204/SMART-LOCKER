from app.database.user_repository import UserRepository


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

