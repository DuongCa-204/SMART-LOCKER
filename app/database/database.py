import os
import sqlite3


class Database:

    def __init__(self):

        BASE_DIR = os.path.dirname(
            os.path.dirname(
                os.path.abspath(__file__)
            )
        )

        self.path = os.path.join(
            BASE_DIR,
            "database",
            "IntelligentLocker.db"
        )


    def connect(self):

        return sqlite3.connect(self.path)