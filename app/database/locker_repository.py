from app.database.database import Database
from datetime import datetime
from app.utils.session import Session
class LockerRepository:

    def __init__(self):

        self.db = Database()
    

    
    def get_user_locker(self, mssv):

        conn = self.db.connect()

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
        conn.close()

        if result:
            return result[0]
        
        
        return None
        


    
    def has_available_locker(self):

        conn = self.db.connect()

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

        conn.close()

        return result is not None



    def insert_access_log(
        self,
        locker_id,
        mssv,
        action,
        name
    ):

        conn = self.db.connect()

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

        conn.close()

    def get_all_lockers(self):

        conn = self.db.connect()

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
            conn = self.db.connect()

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
            conn.commit()

            return True
        
        except Exception as e:
            print(e)

            return False
        
        finally:
            conn.close()       

    def TRATU (self, user, locker_id, name):

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
        # cursor.execute("""
        #                UPDATE LOCKER_USAGE SET
        #                END_TIME = ?, 
        #                STATUS = "Completed"
        #                WHERE LOCKER_ID = ?
        #                AND MSSV = ?
        #                AND END_TIME IS NULL """,
        #                (now, locker_id, user)
        #                )
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

        conn.close()