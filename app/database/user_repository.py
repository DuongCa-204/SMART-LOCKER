from app.database.database import Database
from datetime import datetime
class UserRepository:

    def __init__(self):

        self.db = Database()

    def find_user(self, mssv):

        with self.db.connect() as conn:

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

            return result[0]

    def get_email_by_mssv(self, mssv):

        conn = self.db.connect()

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

        conn.close()

        if result:
            return result[0]

        return None

