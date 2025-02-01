import requests
import csv
import numpy as np
import os

def init():
    if not os.path.exists('./navData.csv'):
        with open('./navData.csv','w',encoding='utf-8',newline='') as csvFile:
            writer = csv.writer((csvFile))
            writer.writerow([
                'typeName',
                'gid',
                'containerid'
            ])

def writerRow(row):
    if not os.path.exists('./navData.csv'):
        with open('./navData.csv','a',encoding='utf-8',newline='') as csvFile:
            writer = csv.writer((csvFile))
            writer.writerow(row)

def get_data(url):
    headers = {
        'Cookie':'XSRF-TOKEN=MybEb-aOOWn1QpHX0GPHOlEt; SCF=Aqje2BC3PQ1yQqISevKZUYvGBPN1qs-ONBt0a7tyWHyFdMbavIZoT9qg6GNb1W6NlLtMJ4bNebla6fLwnNRV5kQ.; SUB=_2A25Kf-YyDeRhGeNI7FYU8SzFzziIHXVp9Wf6rDV8PUNbmtAbLRH1kW9NSCLIZQoT81_v3HpPPiALOwoCrfsCj7Ny; SUBP=0033WrSXqPxfM725Ws9jqgMF55529P9D9WWw0.curRv72MEQPi3LPLQf5JpX5KzhUgL.Fo-cS0BfeKz4ShB2dJLoIEBLxKqL1KqL1hMLxKqLBo5L1KnLxKBLB.qL1K5LxKBLB.qL1K5t; ALF=02_1738744676; WBPSESS=S2MSu44btTPR38ch3vySt6A9Edp4Fl4QBzcmQlZgldPNcn0G_8MBTP6T8svc9NTpvEaaVoniW30cYyxAxqGMiOdtgcpnhF6RWBxaAvmKJS_CqmJI5OR3kyLlbRXPOMj0SJvWGojT-JG8Ak2osQ_Vvg==',
        'User-Agent':'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/131.0.0.0 Safari/537.36 Edg/131.0.0.0'
    }
    params ={
        'is_new_segment':1,
        'fetch_hot':1
    }
    response = requests.get(url,headers=headers,params=params)
    # print(response.json())
    if response.status_code == 200:
        return response.json()
    else:
        return None

def parse_json(response):
    navList = np.append(response['groups'][3]['group'],response['groups'][4]['group'])
    # print(navList)
    for nav in navList:
        navName = nav['title']
        gid = nav['gid']
        containerid = nav['containerid']
        writerRow([
            navName,
            gid,
            containerid
        ])

if __name__ == '__main__':
    init()
    url = 'https://weibo.com/ajax/feed/allGroups?'
    response = get_data(url)
    parse_json(response)