from spiderContent import start as spiderConterntStart
from spiderComments import start as spiderCommentsStart
import os
from sqlalchemy import create_engine
import pandas as pd

engine = create_engine('mysql+pymysql://root:123456@127.0.0.1/weibo_articles?charset=utf8mb4')

def save_to_sql():
    try:
        articleOldPd = pd.read_sql('select * from article',engine)
        articleNewPd = pd.read_csv('./articleData.csv')
        commentOldPd = pd.read_sql('select * from comments', engine)
        commentNewPd = pd.read_csv('./articleComments.csv')

        concatArticlePd = pd.concat([articleNewPd,articleOldPd],join='inner')
        concatCommentPd = pd.concat([commentNewPd,commentOldPd],join='inner')

        concatArticlePd.drop_duplicates(subset='id',keep='last',inplace=True)
        concatCommentPd.drop_duplicates(subset='content',keep='last',inplace=True)

        concatArticlePd.to_sql('article',con=engine,if_exists='replace',index=False)
        concatCommentPd.to_sql('comments', con=engine, if_exists='replace', index=False)
    except:
        articleNewPd = pd.read_csv('./articleData.csv')
        commentNewPd = pd.read_csv('./articleComments.csv')
        articleNewPd.to_sql('article',con=engine,if_exists='replace',index=False)
        commentNewPd.to_sql('comments', con=engine, if_exists='replace', index=False)

    # os.remove('./articleData.csv')
    # os.remove('./articleComments.csv')
    # os.remove(('./navData.csv'))

def main():
    print('正在爬取文章数据')
    spiderConterntStart()
    print('正在爬取文章的评论数据')
    spiderCommentsStart()
    print('正在存储数据')
    save_to_sql()

if __name__ == '__main__':
    main()