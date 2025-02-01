import requests
import csv
import numpy as np
import os
from datetime import datetime
import time


def init():
    if not os.path.exists('./articleComments.csv'):
        with open('./articleComments.csv','w',encoding='utf-8',newline='') as csvFile:
            writer = csv.writer((csvFile))
            writer.writerow([
                'articleId',
                'created_at',
                'likes_counts',
                'region',
                'content',
                'authorName',
                'authorGender',
                'authorAddress',
                'authorAvatar'
            ])

def writerRow(row):
    if not os.path.exists('./articleComments.csv'):
        with open('./articleComments.csv','a',encoding='utf-8',newline='') as csvFile:
            writer = csv.writer((csvFile))
            writer.writerow(row)

def get_data(url,params):
    headers = {
        'Cookie':'XSRF-TOKEN=MybEb-aOOWn1QpHX0GPHOlEt; SCF=Aqje2BC3PQ1yQqISevKZUYvGBPN1qs-ONBt0a7tyWHyFdMbavIZoT9qg6GNb1W6NlLtMJ4bNebla6fLwnNRV5kQ.; SUB=_2A25Kf-YyDeRhGeNI7FYU8SzFzziIHXVp9Wf6rDV8PUNbmtAbLRH1kW9NSCLIZQoT81_v3HpPPiALOwoCrfsCj7Ny; SUBP=0033WrSXqPxfM725Ws9jqgMF55529P9D9WWw0.curRv72MEQPi3LPLQf5JpX5KzhUgL.Fo-cS0BfeKz4ShB2dJLoIEBLxKqL1KqL1hMLxKqLBo5L1KnLxKBLB.qL1K5LxKBLB.qL1K5t; ALF=02_1738744676; WBPSESS=S2MSu44btTPR38ch3vySt6A9Edp4Fl4QBzcmQlZgldPNcn0G_8MBTP6T8svc9NTpvEaaVoniW30cYyxAxqGMiOdtgcpnhF6RWBxaAvmKJS_CqmJI5OR3kyLlbRXPOMj0SJvWGojT-JG8Ak2osQ_Vvg==',
        'User-Agent':'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/131.0.0.0 Safari/537.36 Edg/131.0.0.0'
    }

    response = requests.get(url,headers=headers,params=params)
    # print(response.json())
    if response.status_code == 200:
        return response.json()['data']
    else:
        return None

def getAllArticleList():
    articleList = []
    with open('./articleData.csv','r',encoding='utf-8') as reader:
        readerCsv = csv.reader(reader)
        next(reader)
        for nav in readerCsv:
            articleList.append(nav)
    return articleList

def parse_json(response,articleId):
    for comment in response:
        created_at = datetime.strptime(comment['created_at'],'%a %b %d %H:%M:%S %z %Y').strftime('%Y-%m-%d')
        likes_counts = comment['like_counts']
        try:
            region = comment['source'].replace('来自', '')
        except:
            region = '无'
        content = comment['text_raw']
        authorName = comment['user']['screen_name']
        authorGender = comment['user']['gender']
        authorAddress = comment['user']['location']
        authorAvatar = comment['user']['avatar_large']
        writerRow([
            articleId,
            created_at,
            likes_counts,
            region,
            content,
            authorName,
            authorGender,
            authorAddress,
            authorAvatar
        ])

def start():
    commentUrl = 'https://weibo.com/ajax/statuses/buildComments'
    init()
    articleList = getAllArticleList()
    for article in articleList:
        articleId = article[0]
        print('正在爬取id值为 %s 的文章评论' % articleId)
        time.sleep(2)
        params = {
            'id':int(articleId),
            'is_show_bulletin':2
        }
        response = get_data(commentUrl,params)
        parse_json(response,articleId)

if __name__ == '__main__':
    start()