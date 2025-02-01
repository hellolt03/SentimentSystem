from flask import Flask,session,render_template,redirect,Blueprint,request
from utils.getHomePageData import *
from utils.getPublicData import getAllHotWords
from utils.getHotWordPageData import *
from utils.getTableData import *
from snownlp import SnowNLP
pb=Blueprint('page',__name__,url_prefix='/page',template_folder='templates')


@pb.route('/home')
def home():
    username = session.get('username')
    articleLenMax,likeCountMaxAuthorName,cityMax = getHomeTagsData()
    CommentLikeTop = getHomeCommentLikeTop()
    xData,yData = getHomeArticleCreatedAtChart()
    typeChart = getHomeTypeChart()
    createdAtChart = getHomeCommentCreatedChart()
    return render_template('index.html',
                           username = username,
                           articleLenMax = articleLenMax,
                           likeCountMaxAuthorName = likeCountMaxAuthorName,
                           cityMax = cityMax,
                           CommentLikeTop = CommentLikeTop,
                           xData = xData,
                           yData = yData,
                           typeChart = typeChart,
                           createdAtChart = createdAtChart
                           )

@pb.route('/hotWord')
def hotWord():
    username = session.get('username')
    hotWordList = getAllHotWords()
    defaultHotWord = hotWordList[0][0]
    if request.args.get('hotWord'):defaultHotWord = request.args.get('hotWord')
    hotWordLen = getHoWordLen(defaultHotWord)
    xData,yData =getHotWordPageCreatedAtCharData(defaultHotWord)
    sentences = ''
    value = SnowNLP(defaultHotWord).sentiments
    if value == 0.5:
        sentences = '中性'
    elif value > 0.5:
        sentences = '正面'
    else:
        sentences = '负面'
    print("sentences:",sentences)
    commentData = getCommentFilterData(defaultHotWord)
    return render_template('hotWord.html',
                           username = username,
                           hotWordList = hotWordList,
                           defaultHotWord = defaultHotWord,
                           hotWordLen = hotWordLen,
                           sentences = sentences,
                           xData = xData,
                           yData = yData,
                           commentData = commentData
                           )

@pb.route('/tableData')
def tableData():
    username = session.get('username')
    defaultFlag = False
    if request.args.get('flag'):defaultFlag = True

    tableData = getTableDataList(defaultFlag)
    return render_template('tableData.html',
                           username=username,
                           tableData = tableData,
                           defaultFlag = defaultFlag
                           )

@pb.route('/test')
def test():
    username = session.get('username')
    return render_template('test.html',
                           username=username,
                           )
