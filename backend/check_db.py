import sqlite3

# ربط بالقاعدة
conn = sqlite3.connect("travelspeek.db")
cursor = conn.cursor()

# شوف الجداول
cursor.execute("SELECT name FROM sqlite_master WHERE type='table';")
tables = cursor.fetchall()
print("Tables:", tables)

# شوف محتوى كل جدول
for table in tables:
    print(f"\nContents of table {table[0]}:")
    cursor.execute(f"SELECT * FROM {table[0]}")
    rows = cursor.fetchall()
    for row in rows:
        print(row)

conn.close()
