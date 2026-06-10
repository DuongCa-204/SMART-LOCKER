import os
import sqlite3

# Dùng Path cho rõ ràng và an toàn hơn
from pathlib import Path

class Database:
    def __init__(self):
        self.path = Path(__file__).parent / "IntelligentLocker.db"
    
    def connect(self):
        conn = sqlite3.connect(self.path)
        conn.execute("PRAGMA foreign_keys = ON")  # Bật kiểm tra FK
        return conn


# Path là lớp giúp thao tác đường dẫn file một cách hiện đại hơn os.path.

# self.path = Path(__file__).parent / "IntelligentLocker.db" => Đây là dòng tạo đường dẫn tới file database.

#####################################################################
#########################   HÀM INIT    #############################
#####################################################################

############ BƯỚC 1 ##############
# __file__ : là một biến đặt biệt của python 
# Giả sử file đang nằm ở: SML/app/database/database.py => nếu print(__file__) sẽ ra SML/app/database/database.py

############ BƯỚC 2 ##############
# Path(__file__) => chuyển chuỗi đường dẫn thành đối tượng Path
# Kết quả => Path("SML/app/database/database.py")

############ BƯỚC 3 ##############
# Path(__file__).parent => lấy thư mục chứa file hiện tại
# Từ SML/app/database/database.py => SML/app/database/database.py

############ BƯỚC 4 ##############
# Path(__file__).parent / "IntelligentLocker.db"  =>  Trong Pathlib nó dùng để nối đường dẫn.
# kết quả => SML/app/database/IntelligentLocker.db

############ BƯỚC CUỐI ##############
# self.path => SML/app/database/IntelligentLocker.db


#####################################################################
#########################   HÀM CONNECT    ##########################
#####################################################################


############ B1 ##############
# conn = sqlite3.connect(self.path) => tạo kết nối tới SQLite theo đường dẫn self.path
# **** NOTE **** : nếu file database chưa tồn tại  IntelligentLocker.db => SQLite sẽ tự tạo file mới

############ B2 ##############
# conn.execute("PRAGMA foreign_keys = ON") => lênh đặt biệt của SQLite ( kiểm tra khóa ngoại)
# => dùng để cấu hình cách SQLite hoạt động

# ví dụ có 2 bảng
# | USER_ID | NAME  |    | ID | USER_ID |
# | ------- | ----- |    | -- | ------- |
# | 1       | Duong |    | 1  | 1       |
# | 2       | An    |    | 2  | 2       |

# trong bảng BORROW_HISTORY có USER_ID => tham chiếu đến USER.USER_ID
# nếu bạn ghi dữ liệu INSERT INTO BORROW_HISTORY  VALUES (3, 999);
# Trong đó USER_ID = 999  => không tồn tại (nhưng SQLite lại mặc đinh cho lưu)
# ====> database bị sai dữ liệu
# nếu bật PRAGMA => nó sẽ báo lại là:
# sqlite3.IntegrityError:
# FOREIGN KEY constraint failed

