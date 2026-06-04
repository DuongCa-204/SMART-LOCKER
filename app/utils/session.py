import sys
import os
class Session:

    current_user = None

    user_name = None
    user_email = None

    current_mode = None

    selected_locker = None


    current_otp = None
    otp_expire_time = None
    
    ktv_pin = None          # PIN của KTV đã xác thực
    ktv_name = None         # Tên KTV (ví dụ: "Kỹ Thuật Viên")
    ktv_id = None           # ID KTV (ví dụ: "KTV001")