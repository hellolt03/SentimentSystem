from utils.getPublicData import getAllArticleData
from snownlp import SnowNLP
def getTableDataList(flag):
    if flag:
        tableList = []
        articleList = getAllArticleData()
        for article in articleList:
            item = list(article)
            value = ''
            if SnowNLP(item[5]).sentiments > 0.5:
                value = '正面'
            elif SnowNLP(item[5]).sentiments < 0.5:
                value = '负面'
            else:
                value = '中性'
            item.append(value)
            tableList.append(item)
        return tableList
    else:
        return getAllArticleData()