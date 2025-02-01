import requests
import csv
import numpy as np
import os
from datetime import datetime
import time


def init():
    if not os.path.exists('./articleData.csv'):
        with open('./articleData.csv','w',encoding='utf-8',newline='') as csvFile:
            writer = csv.writer((csvFile))
            writer.writerow([
                'id', # 发文章者的id
                'likeNum', # 点赞数量attitudes_count
                'commentsLen', # 评论数量comments_count
                'reposts_count', #转发量reposts_count
                'region', # 地区region_name
                'content', # 内容text/text_raw
                'contentLen', # 字数的长度textLength
                'created_at', # 文章发布的时间created_at: "Sun Dec 29 20:12:24 +0800 2024"
                'type', # 类型
                'detailUrl', # 文章详情页 followBtnCode: {uid: 7002084904, followcardid: "1028030000_5112963503489414_3a951b6b"}followcardid: "1028030000_5112963503489414_3a951b6b"uid: 7002084904
                'authorAvatar', # 作者头像avatar_hd/avatar_large
                'authorName', # 作者昵称screen_name
                'authorDetail', # 作者详情页面profile_url: "/u/6983976608"
                'isVip', # v_plus
            ])

def writerRow(row):
    if not os.path.exists('./articleData.csv'):
        with open('./articleData.csv','a',encoding='utf-8',newline='') as csvFile:
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
        return response.json()['statuses']
    else:
        return None

def getAllTypeList():
    typeList = []
    with open('./navData.csv','r',encoding='utf-8') as reader:
        readerCsv = csv.reader(reader)
        next(reader)
        for nav in readerCsv:
            typeList.append(nav)
    return typeList

def parse_json(response,type):
    for article in response:
        id = article['id']
        likeNum = article['attitudes_count']
        commentsLen = article['comments_count']
        reposts_count = article['reposts_count']
        try:
            region = article['region_name'].replace('发布于','')
        except:
            region = '无'
        content = article['text_raw']
        try:
            contentLen = article['textLength']
        except:
            contentLen = '无'
        created_at = datetime.strptime(article['created_at'],'%a %b %d %H:%M:%S %z %Y').strftime('%Y-%m-%d')
        type = type
        try:
            detailUrl = 'https://weibo.com/' + str(article['id']) + '/' + str(article['mblogid'])
            # print(detailUrl)
        except:
            detailUrl='无'
        authorAvatar = article['user']['avatar_large']
        authorName = article['user']['screen_name']
        authorDetail = 'https://weibo.com/u/' + str(article['user']['id'])
        isVip = article['user']['v_plus']
        writerRow([
            id,
            likeNum,
            commentsLen,
            reposts_count,
            region,
            content,
            contentLen,
            created_at,
            type,
            detailUrl,
            authorAvatar,
            authorName,
            authorDetail,
            isVip,
        ])

def start(typeNum=3,pageNum=2):
    articleUrl = 'https://weibo.com/ajax/feed/hottimeline'
    init()
    typeList = getAllTypeList()
    typeNumCount = 0
    for type in typeList:
        if typeNumCount > typeNum:return
        time.sleep(2)
        for page in range(0,pageNum):
            print('正在爬取的类型：%s 中的第 %s 页文章的数据'%(type[0],page+1))
            time.sleep(1)
            params = {
                'group_id':type[1],
                'containerid':type[2],
                'maxid':page,
                'count':10,
                'extparam':'discover|new_feed',
            }
            response = get_data(articleUrl,params)
            parse_json(response,type[0])
        typeNum += 1


if __name__ == '__main__':
    start()