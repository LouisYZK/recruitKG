import requests

query_set = {
    'lang': 'c',
    'stype': '',
    'postchannel': '0000',
    'workyear': 99,
    'cotype': 99,
    'degreefrom': 99,
    'jobterm': 99,
    'companysize': 99,
    'providesalary': 99,
    'lonlat': 0,
    'radius': -1,
    'ord_field': 0,
    'confirmdate': 9,
    'fromType': '',
    'dibiaoid': 0,
    'address': '' ,
    'line': '' ,
    'specialarea': '',
    'from': '',
    'welfare': '' 
}

url = 'https://search.51job.com/list/000000,000000,0000,01%252C37,9,99,%2520,2,1.html'

r = requests.get(url, params=query_set)
print(r.content.decode('gbk'))