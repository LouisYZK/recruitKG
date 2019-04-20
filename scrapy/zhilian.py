import requests
import json
import sqlite3
from concurrent.futures import ThreadPoolExecutor

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
    'pageSize': 90,
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
                company_name varchar(50),
                company_size varchar(10),
                city varchar(10),
                info_url varchar(60),
                welfare varchar(80),
                salary varchar(20),
                position varchar(30),
                job_type varchar(50));'''
    cursor.execute(sql)
    insert_sql = "insert into zhilian values (?, ?, ?, ?, ?, ?, ?, ?);"
    cursor.executemany(insert_sql, data)
    conn.commit()
    conn.close()

def get_data(params): 
    global seen
    res_item = []
    try:
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
                res_item.append((res['company']['name'],
                                res['company']['size']['name'],
                                res['city']['display'],
                                res['positionURL'],
                                '/'.join(res['welfare']),
                                res['salary'],
                                res['jobName'],
                                res['jobType']['display']))
                seen.add((res['company']['name'], res['jobName']))
            print(res['company']['name'], res['jobName'], '......')
    except Exception as e:
        print(e)
        store_to_base(res_item)
    finally:
        store_to_base(res_item)
        print(len(seen))

with ThreadPoolExecutor(max_workers=4) as e:
    seen = set()
    for kw in KW_ALL:
        i = 0
        params['kw'] = kw
        while True:
            params['start'] = i * 90
            try:
                e.submit(get_data(params))
                i += 1
                print('i:', i)
            except Exception as e:
                continue

        

