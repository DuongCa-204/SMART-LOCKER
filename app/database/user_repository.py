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
                AND warned_at IS NOT NULL
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