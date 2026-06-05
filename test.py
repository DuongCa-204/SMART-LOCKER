# File: create_service_log_table.py
import sqlite3
import os

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
DB_PATH = os.path.join(BASE_DIR, "app", "database", "IntelligentLocker.db")

def create_table():
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    
    # Tạo bảng với tên đúng: Service_engineer_log (S viết hoa)
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS Service_engineer_log (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            locker_id TEXT NOT NULL,
            ktv_id TEXT NOT NULL,
            ktv_name TEXT NOT NULL,
            action TEXT NOT NULL,
            timestamp DATETIME DEFAULT CURRENT_TIMESTAMP,
            notes TEXT
        );
    """)
    
    conn.commit()
    
    # Kiểm tra
    cursor.execute("SELECT name FROM sqlite_master WHERE type='table' AND name='Service_engineer_log';")
    result = cursor.fetchone()
    
    if result:
        print("✅ Bảng Service_engineer_log đã tạo thành công!")
        
        # Hiển thị các bảng
        cursor.execute("SELECT name FROM sqlite_master WHERE type='table';")
        tables = cursor.fetchall()
        print("\n📋 Tất cả bảng trong database:")
        for table in tables:
            print(f"   - {table[0]}")
    else:
        print("❌ Lỗi tạo bảng")
    
    conn.close()

if __name__ == "__main__":
    create_table()