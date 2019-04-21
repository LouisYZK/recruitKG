import sqlite3
import pandas as pd
from concurrent.futures import ThreadPoolExecutor
# query table info:
conn = sqlite3.connect('zhilian.db')
cur = conn.cursor()

"""
create new columns
"""
# cur.execute("PRAGMA table_info(zhilian)")
# cols = cur.fetchall()
# cols_name = set([item[1] for item in cols])
# if 'is_unique' not in cols_name:
#     cur.execute('alter table zhilian add column is_unique int;')

# 检查重复


def check_unique():
    data = next(gen)
    name, position = data[0], data[1], data[7] 
    if (name, position) not in seen:
        seen.add((name, position))
        print(name, position)
        print('Unique num:', len(seen))

with ThreadPoolExecutor(max_workers=4) as executor:
    seen = set()
    gen = cur.execute('select * from zhilian')
    t = 0
    while True:
        try:
            executor.submit(check_unique())
        except Exception as e:
            print(e)
            break
    