from app.database.database import Database
from datetime import datetime

class LockerRepository:

    def __init__(self):

        self.db = Database()
    

    def get_user_locker(self, mssv):
        with self.db.connect() as conn:
            cursor = conn.cursor()
            cursor.execute(
                """
                SELECT locker_id
                FROM Lockers
                WHERE current_mssv = ?
                """,
                (mssv,)
            )
            result = cursor.fetchone()
            return result[0] if result else None
        
    
    def has_available_locker(self):
        with self.db.connect() as conn:
            cursor = conn.cursor()
            cursor.execute(
                """
                SELECT 1
                FROM Lockers
                WHERE status = 'empty'
                LIMIT 1
                """
            )
            result = cursor.fetchone()
            return result is not None


    def insert_access_log(
        self,
        locker_id,
        mssv,
        action,
        name
    ):

        with self.db.connect() as conn:

            cursor = conn.cursor()

            now = datetime.now().strftime("%Y-%m-%d %H:%M:%S")


            cursor.execute(
                """
                INSERT INTO Locker_access_log
                (
                    locker_id,
                    mssv,
                    event,
                    timestamp,
                    name
        
                )
                VALUES (?, ?, ?, ?, ?)
                """,
                (
                    locker_id,
                    mssv,
                    action,
                    now,
                    name
                )
            )


            cursor.execute(
                """
                UPDATE Users SET
                last_active_time = ?
                WHERE mssv = ?
                """,
                (
                    now,
                    mssv
                )
            )


            conn.commit()

     

    def get_all_lockers(self):

        with self.db.connect() as conn:

            cursor = conn.cursor()

            cursor.execute("""
                SELECT
                    locker_id,
                    status,
                    current_mssv
                FROM Lockers
            """)

            return cursor.fetchall()
    
    def set_status_locker(self, user, locker_id, name):
        try:
            with self.db.connect() as conn:

                cursor = conn.cursor()
                now = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

                cursor.execute("""
                            UPDATE Lockers SET 
                            status ='Busy', 
                            current_mssv=? 
                            WHERE locker_id =?""", 
                            (user, locker_id)
                            )
                    
                cursor.execute("""
                            INSERT INTO Locker_access_log 
                            (locker_id, mssv, timestamp, event, name)
                            VALUES (?, ?, ?, ?, ?)""", 
                            (locker_id, user, now, 'BORROW', name))
                cursor.execute("""
                            UPDATE Users SET 
                            last_active_time = ? 
                            WHERE mssv =? """,
                            (now, user,)
                            )
                conn.commit()

                return True
        
        except Exception as e:
            print(e)

            return False
            

    def return_locker (self, user, locker_id, name):
        try:
            with self.db.connect() as conn:

                conn = self.db.connect()

                cursor = conn.cursor()
                now = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

                cursor.execute("""
                            UPDATE Lockers SET
                            status = "empty", 
                            current_mssv = NULL
                            WHERE locker_id = ? """,
                            (locker_id,)
                            )

                cursor.execute("""
                            UPDATE Users SET 
                            last_active_time = ? 
                            WHERE mssv =? """,
                            (now, user,)
                            )
                cursor.execute("""INSERT INTO Locker_access_log 
                            (locker_id, mssv, timestamp, event, name)
                                VALUES (?, ?, ?, ?, ?)""", 
                                (locker_id, user, now, 'RETURN', name))
                
                conn.commit()

                return True
        except Exception as e:
            print(e)
            return False

####################################################################
########################  SERVICE ENGINEER  ########################
####################################################################

    def insert_service_log(self, locker_id, ktv_id, ktv_name, action):
        """
        Ghi log khi KTV thực hiện hành động (mở/khóa/test tủ)
        
        Args:
            locker_id: ID tủ (ví dụ: "L01")
            ktv_id: ID KTV (ví dụ: "KTV001")
            ktv_name: Tên KTV
            action: Hành động (OPEN, LOCK, TEST)
        """
        try:
            conn = self.db.connect()
            cursor = conn.cursor()
            now = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            
            cursor.execute(
                """
                INSERT INTO Service_engineer_log
                (locker_id, ktv_id, ktv_name, action, timestamp)
                VALUES (?, ?, ?, ?, ?)
                """,
                (locker_id, ktv_id, ktv_name, action, now)
            )
            
            conn.commit()
            conn.close()
            return True
            
        except Exception as e:
            print(f"Error inserting service log: {e}")
            return False
    def update_locker_maintenance(self, locker_id, status):
        """
        Cập nhật trạng thái bảo trì của tủ
        
        Args:
            locker_id: ID tủ (ví dụ: "L01")
            status: "maintenance" hoặc "available"
        """
        try:
            conn = self.db.connect()
            cursor = conn.cursor()
            
            cursor.execute(
                """
                UPDATE Lockers SET status = ?
                WHERE locker_id = ?
                """,
                (status, locker_id)
            )
            
            conn.commit()
            conn.close()
            return True
            
        except Exception as e:
            print(f"Error updating locker maintenance: {e}")
            return False

