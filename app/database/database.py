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