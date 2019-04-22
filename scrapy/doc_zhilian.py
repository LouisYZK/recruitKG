import requests
import sqlite3
from pyquery import PyQuery as pq


def store_doc_to_base(*args):
    sql = '''create table if not exists 
             zhilian_doc(
                company_name varchar(50),
                position varchar(30),
                doc varchar(1000));
         '''
    conn = sqlite3.connect('zhilian.db')
    cur = conn.cursor()
    cur.execute(sql)
    sql = 'insert into zhilian_doc values(?, ?, ?);'
    cur.execute(sql, args)

conn = sqlite3.connect('zhilian.db')
cur = conn.cursor()
data = cur.execute('select * from zhilian;')

while True:
    info = next(data)   
    name = info[1]
    pos = info[7] 
    url = info[4]

    job_code = url.split('/')[3]
    try:
        url = 'https://m.zhaopin.com/jobs/' + job_code
        r = requests.get(url)

        d = pq(r.text)
        text = d('div .about-main').text().strip()
        print(name, pos)
        print(len(text))
        store_doc_to_base(name, pos, text)
    except Exception as e:
        print(e)