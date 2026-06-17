from app.database.database import Database
from datetime import datetime
import sqlite3

class UserRepository:

    def __init__(self):

        self.db = Database()

    def find_user(self, mssv):

        with self.db.connect() as conn:

            conn.row_factory = sqlite3.Row
            cursor = conn.cursor()

            cursor.execute(
                """
                SELECT *
                FROM Users
                WHERE mssv = ?
                """,
                (mssv,)
            )

            return cursor.fetchone()

    def find_password(self, mssv, password):

        with self.db.connect() as conn:

            cursor = conn.cursor()

            cursor.execute(
                """
                SELECT *
                FROM Users
                WHERE mssv = ? AND password = ?
                """,
                (mssv, password)
            )

            return cursor.fetchone()
        
    def user_exists(self, mssv, email):

        with self.db.connect() as conn:

            cursor = conn.cursor()

            cursor.execute(
                """
                SELECT 1 FROM Users WHERE mssv=? OR email=?
                """,
                (
                    mssv,
                    email
                )
            )

            return cursor.fetchone()
        
    def create_user(self,mssv,name,email, password):

        with self.db.connect() as conn:

            cursor = conn.cursor()


            cursor.execute(
                """
                INSERT INTO Users
                (
                    mssv,
                    name,
                    email,
                    password
                )
                VALUES (?, ?, ?, ?)
                """,
                (
                    mssv,
                    name,
                    email,
                    password
                )
            )

            conn.commit()

    def get_name_by_mssv(self, mssv):

        with self.db.connect() as conn:

            cursor = conn.cursor()

            cursor.execute(
                """
                SELECT name
                FROM Users
                WHERE MSSV = ?
                """,
                (mssv,)
            )

            result = cursor.fetchone()

            return result[0] if result else None

    def get_email_by_mssv(self, mssv):

        with self.db.connect() as conn:

            cursor = conn.cursor()
            cursor.execute(
                """
                SELECT email
                FROM Users
                WHERE mssv = ?
                """,
                (mssv,)
            )

            result = cursor.fetchone()
            return result[0] if result else None


    ####################################################################
    ########################  CLEAN UP USER  ###########################
    ####################################################################


    def get_inactive_users(self):

        with self.db.connect() as conn:

            cursor = conn.cursor()

            cursor.execute("""
                SELECT email, mssv
                FROM Users
                WHERE datetime(last_active_time)
                    < datetime('now','localtime','-2 minutes')
                AND warned_at IS NULL
                AND account_status = 'ACTIVE'
            """)

            return cursor.fetchall()


    def mark_inactive(self):
        with self.db.connect() as conn:
            cursor = conn.cursor()
            cursor.execute("""
                UPDATE Users
                SET account_status = 'INACTIVE'
                WHERE account_status = 'ACTIVE'
                AND warned_at IS NOT NULL
                AND datetime(warned_at)
                    < datetime('now','localtime','-1 minutes')
            """)
            conn.commit()


    def delete_expired_users(self):

        with self.db.connect() as conn:

            cursor = conn.cursor()

            cursor.execute("""
                UPDATE Users
                SET account_status = 'DELETED'
                WHERE account_status = 'INACTIVE'
                AND datetime(warned_at)
                    < datetime('now','localtime','-4 minutes')
            """)

            conn.commit()


    def mark_warned(self, mssv):
        with self.db.connect() as conn:
            cursor = conn.cursor()
            now = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            cursor.execute("""
                UPDATE Users SET warned_at = ?
                WHERE mssv = ?
            """, (now, mssv))
            conn.commit()

    ####################################################################
    ########################  UPDATE ACCOUNT  ###########################
    ####################################################################


    def update_account_status(self,mssv):
        print(f"Updating status for: {mssv}")  # Thêm tạm để debug

        with self.db.connect() as conn:

            cursor = conn.cursor()

            now = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

            cursor.execute(
                """
                UPDATE Users SET
                account_status = 'ACTIVE',
                warned_at = NULL
                WHERE mssv = ?
                """,
                (
                    mssv,
                )
            )

            conn.commit()



#####################################################################
#########################   HÀM INIT    #############################
#####################################################################

#########   HÀM INIT    #############

# def __init__(self):
#    self.db = Database()  # Tạo 1 kết nối DB riêng cho Repository này


#########   with statement   #############

# with self.db.connect() as conn:
    # làm gì đó
# Khi ra khỏi with → conn tự động đóng ✅

# ===> tại sao lại dùng with?

# ❌ Không dùng with - nguy hiểm
# conn = self.db.connect()
# cursor.execute(...)  # Nếu lỗi ở đây
# conn.close()         # → Không bao giờ chạy đến đây → memory leak (rò rỉ bộ nhớ => lãng phí tài nguyên)

# VÍ DỤ:
# ❌ Không dùng with
# conn = self.db.connect()    # Mở kết nối
# cursor.execute(...)          # Nếu dòng này bị lỗi
# conn.close()                 # → Không bao giờ chạy đến đây!
# Kết nối vẫn còn mở ngầm trong bộ nhớ
# Chạy 100 lần → 100 kết nối bị treo → máy hết RAM → crash

# # ✅ Dùng with - an toàn
# with self.db.connect() as conn:
#     cursor.execute(...)  # Dù lỗi hay không → conn vẫn tự đóng


#########   CURSOR ROLE   #############

# conn   = Quyển sổ (Database connection)
# cursor = Cái bút để viết/đọc trên quyển sổ đó

# conn = sqlite3.connect("DB.db")  
# # → Mở quyển sổ ra

# cursor = conn.cursor()           
# # → Cầm bút lên, sẵn sàng đọc/ghi

# cursor.execute("SELECT ...")     
# # → Dùng bút để đọc thông tin

# cursor.execute("INSERT ...")     
# # → Dùng bút để ghi thông tin

# cursor.fetchone()                
# # → Đọc 1 dòng vừa tìm được

# conn.commit()                    
# # → Đóng dấu xác nhận những gì vừa ghi

# =======> tại sao cần cursor mà không dùng thẳng conn 
# conn quản lý KẾT NỐI (mở/đóng/commit)
# cursor quản lý TRUY VẤN (execute/fetch)

# Có thể tạo nhiều cursor từ 1 conn
# cursor1 = conn.cursor()  # Đọc bảng Users
# cursor2 = conn.cursor()  # Đọc bảng Lockers
# # → 2 truy vấn độc lập trên cùng 1 kết nối

#########    SQL Injection là gì?   #############

# ❌ Dùng f-string - NGUY HIỂM
# mssv = "' OR '1'='1"  # Hacker nhập vào

# cursor.execute(f"SELECT * FROM Users WHERE mssv = '{mssv}'")

# # Câu SQL tạo ra:
# "SELECT * FROM Users WHERE mssv = '' OR '1'='1'"
# #                                  ↑
# #                        Điều kiện luôn đúng!
# #                        '1'='1' → True
# #                        → Lấy TOÀN BỘ Users trong DB!

# ============> giải thích chi tiết
# SELECT * FROM Users 
# WHERE mssv = ''     -- mssv rỗng → False
# OR '1' = '1'        -- 1=1 → luôn True!
# -- False OR True → True
# -- → Trả về TẤT CẢ users!


# ✅ Dùng ? - AN TOÀN
# mssv = "' OR '1'='1"  # Hacker nhập vào

# cursor.execute(
#     "SELECT * FROM Users WHERE mssv = ?",
#     (mssv,)  # SQLite tự xử lý
# )

# SQLite hiểu đây là GIÁ TRỊ, không phải CÂU LỆNH
# → Tìm user có mssv = "' OR '1'='1" (chuỗi thông thường)
# → Không tìm thấy → trả về None ✅


#########     row_factory = sqlite3.Row   #############

# NOTE
# Không có row_factory:
# user = cursor.fetchone()
# user[0]  # mssv
# user[3]  # is_approved ← Phải nhớ số thứ tự cột, dễ sai!

# Có row_factory:
# user = cursor.fetchone()
# user['mssv']        # ← Dùng tên cột, rõ ràng hơn ✅
# user['is_approved'] # ← Không sợ sai dù thêm/bớt cột


#########     fetchone vs fetchall   #############

# cursor.fetchone()   # Lấy 1 dòng → trả về tuple/Row hoặc None
# cursor.fetchall()   # Lấy tất cả → trả về list of tuple/Row

# find_user → chỉ cần 1 user → fetchone
# result = cursor.fetchone()
# # → ("22110001", "Nguyen Van A", ...) hoặc None

# # get_inactive_users → nhiều user → fetchall
# result = cursor.fetchall()
# → [("a@gmail.com", "22110001"), ("b@gmail.com", "22110002"), ...]


#########    result[0] if result else None   #############

# VÍ DỤ:
# def get_name_by_mssv(self, mssv):
#     result = cursor.fetchone()
#     return result[0] if result else None

# # Nếu không tìm thấy user
# result = cursor.fetchone()  # → None

# result[0]  # ❌ None[0] → crash IndexError!

# # ✅ Kiểm tra trước
# return result[0] if result else None
# # → Nếu result có giá trị → lấy result[0]
# # → Nếu result = None → trả về None an toàn



#####################################################################
#########################   HÀM     #############################
#####################################################################

#=================    find_user()   =================#

# def find_user(self, mssv):
# # Định nghĩa hàm nhận vào mssv (VD: "22110001")

# with self.db.connect() as conn:
# # Mở kết nối DB, tự đóng khi xong

# conn.row_factory = sqlite3.Row
# # Cho phép truy cập kết quả bằng tên cột
# # user['mssv'] thay vì user[0]

# cursor = conn.cursor()
# # Tạo "bút" để thực hiện truy vấn

# cursor.execute(
#     "SELECT * FROM Users WHERE mssv = ?",
#     (mssv,)
# )
# # Tìm user có mssv khớp
# # (mssv,) → tuple 1 phần tử, truyền vào ?

# return cursor.fetchone()
# # Trả về 1 dòng kết quả hoặc None

# NOTE: KẾT QUẢ TRẢ VỀ
# Tìm thấy:
# user = find_user("22110001")
# user['mssv']           # "22110001"
# user['name']           # "Nguyen Van A"
# user['is_approved']    # 1
# user['account_status'] # "ACTIVE"

# # Không tìm thấy:
# user = find_user("99999999")
######## → None


#=================    find_password()   =================#

# "SELECT * FROM Users WHERE mssv = ? AND password = ?"
# Tìm user có ĐỒNG THỜI mssv VÀ password khớp
# AND → cả 2 điều kiện phải đúng

# (mssv, password)
# Tuple 2 phần tử → truyền vào 2 dấu ?
# ? thứ 1 = mssv
# ? thứ 2 = password

# NOTE: KẾT QUẢ TRẢ VỀ
# Đúng cả mssv lẫn password → trả về user
# Sai 1 trong 2 → trả về None


#=================    user_exists()   =================#
# SELECT * → Lấy toàn bộ thông tin user (tốn tài nguyên)
# SELECT 1 → Chỉ trả về số 1 nếu tìm thấy (nhanh hơn)

# Mục đích chỉ là KIỂM TRA TỒN TẠI
# Không cần biết thông tin user là gì
# → SELECT 1 đủ rồi ✅


#=================    create_user()   =================#

# INSERT INTO Users (mssv, name, email, password)
# # Chỉ định rõ cột nào được insert
# # Các cột không liệt kê → dùng giá trị DEFAULT

# VALUES (?, ?, ?, ?)
# # 4 dấu ? → 4 giá trị
# # ? thứ 1 = mssv
# # ? thứ 2 = name
# # ? thứ 3 = email
# # ? thứ 4 = password

# conn.commit()
# # Xác nhận lưu vào DB
# # Không có dòng này → dữ liệu mất khi tắt app!

#=================    get_name_by_mssv() & get_email_by_mssv()   =================#

# Tại sao SELECT name thay vì SELECT *?
# Chỉ cần lấy tên → không cần lấy toàn bộ thông tin
# Tiết kiệm tài nguyên ✅

# result = ("Nguyen Van A",)  → tuple 1 phần tử
# result[0] = "Nguyen Van A"  → lấy phần tử đầu tiên

#=================    update_account_status()   =================#

# UPDATE Users          # Cập nhật bảng Users
# SET account_status = 'ACTIVE'  # Đặt trạng thái = ACTIVE
# WHERE mssv = ?        # Chỉ cập nhật user có mssv này

# Được gọi khi:
# - User gửi đồ ✅
# - User mở tủ ✅  
# - User trả tủ ✅


#####################################################################
#########################  CLEANUP    #############################
#####################################################################


#=================    get_inactive_users()   =================#

# datetime(last_active_time) < datetime('now','localtime','-2 minutes')
# # last_active_time < (thời gian hiện tại - 2 phút)
# # → Không active hơn 2 phút

# AND warned_at IS NULL
# # Chưa được gửi mail cảnh báo

# AND account_status = 'ACTIVE'
# # Tài khoản đang active (không phải INACTIVE/DELETED)

# Tóm lại: Lấy những user ACTIVE
#           không dùng hơn 2 phút
#           và chưa được cảnh báo


#=================    mark_warned()   =================#

# now = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
# # datetime.now() → thời gian hiện tại
# # .strftime(...)  → định dạng thành chuỗi
# # VD: "2024-01-15 14:30:00"

# UPDATE Users SET warned_at = ?
# # Ghi thời gian gửi mail vào cột warned_at
# # Mục đích: Không gửi mail lần 2 cho cùng 1 user


#=================    mark_inactive()  =================#

# account_status = 'ACTIVE'     # Đang active
# AND warned_at IS NOT NULL      # Đã được gửi mail
# AND datetime(warned_at) < datetime('now','localtime','-1 minutes')
# Đã gửi mail hơn 1 phút rồi

# → Chuyển INACTIVE + reset warned_at = NULL
# (reset để lần sau active lại vẫn nhận được mail)

#=================    mark_inactive()  =================#

# DELETE thật → lỗi FK vì các bảng khác tham chiếu đến Users
# VD: Locker_access_log có cột mssv → tham chiếu Users.mssv
# Xóa user → Locker_access_log mất tham chiếu → lỗi!

# → Dùng UPDATE SET account_status = 'DELETED'
# → Giữ lại dữ liệu, chỉ đánh dấu đã "xóa" ✅







