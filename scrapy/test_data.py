import sqlite3

# query table info:
conn = sqlite3.connect('zhilian.db')
cur = conn.cursor()
# cur.execute("PRAGMA table_info(zhilian)")
# print(cur.fetchall())
cur.execute('select * from zhilian')
data = cur.fetchall()
for item in data:
    print(item[0])