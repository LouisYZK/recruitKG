import requests
import json
import sqlite3
import time
import argparse
from concurrent.futures import ThreadPoolExecutor

parser = argparse.ArgumentParser()
parser.add_argument('start', type=int, help='define the start page num')
args = parser.parse_args()

BASE_URL = 'https://fe-api.zhaopin.com/c/i/sou'
KW_ALL = [
    'Java开发', 'UI设计师', 'Web前端', 'PHP',
    'Python', 'Andriod', '美工', '深度学习',
    '算法工程师', 'Hadoop', 'Node.js', '数据开发',
    '数据分析师', '数据架构', '人工智能', '区块链'
]
headers = {
        'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/70.0.3538.77 Safari/537.36'
    }
params = {
    'start': 0,
    'pageSize': 100,
    'cityId': 489,
    'workExperience': -1,
    'education': -1,
    'companyType': -1,
    'employmentType': -1,
    'jobWelfareTag': -1,
    'kw': '',
    'kt': 3,
    '_v': 0.16654023,
    'x-zp-page-request-id': '6ff2621296c64c258713bb528f3de860-1555684559346-459410',
}


def store_to_json(data):
    with open('zhilian.json', 'a') as fp:
        json.dump(data, fp)

def store_to_base(data):
    conn = sqlite3.connect('zhilian.db')
    cursor = conn.cursor()
    sql = '''create table if not exists 
             zhilian(
                kw varchar(20),
                company_name varchar(50),
                company_size varchar(10),
                city varchar(10),
                info_url varchar(60),
                welfare varchar(80),
                salary varchar(20),
                position varchar(30),
                job_type varchar(50));
         '''
    cursor.execute(sql)
    insert_sql = "insert into zhilian values (?, ?, ?, ?, ?, ?, ?, ?, ?);"
    cursor.executemany(insert_sql, data)
    conn.commit()
    conn.close()

def count_base_table():
    conn = sqlite3.connect('zhilian.db')
    cursor = conn.cursor()
    cursor.execute('select count(*) from zhilian')
    num = cursor.fetchall()
    return num[0][0]

def get_data(params): 
    global seen
    res_item = []
    r = requests.get(BASE_URL, params=params, headers=headers)
    results = r.json()['data']['results']
    for res in results:
        if (res['company']['name'], res['jobName']) not in seen:
            # res_dct.append(
            #     {
            #         'company_name': res['company']['name'],
            #         'company_size': res['company']['size']['name'],
            #         'city': res['city']['display'],
            #         'info_url': res['positionURL'],
            #         'welfare': '/'.join(res['welfare']),
            #         'salary': res['salary'],
            #         'position': res['jobName'],
            #         'job_type': res['jobType']['display']
            #     }
            # )
            res_item.append((params['kw'],
                            res['company']['name'],
                            res['company']['size']['name'],
                            res['city']['display'],
                            res['positionURL'],
                            '/'.join(res['welfare']),
                            res['salary'],
                            res['jobName'],
                            res['jobType']['display']))
            seen.add((res['company']['name'], res['jobName']))
        print(res['company']['name'], res['jobName'], '......')
    store_to_base(res_item)

with ThreadPoolExecutor(max_workers=4) as executor:
    seen = set()
    for kw in KW_ALL:
        params['kw'] = kw
        for i in range(9):
            params['start'] = args.start * 900 + i * 100
            try:
                executor.submit(get_data(params))
            except Exception as e:
                print(e)
                time.sleep(10)
                continue
            finally:
                i += 1
                print(len(seen))
        print('Thera have been', count_base_table(), 'in the database!')


        

