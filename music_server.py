import json
import os
import numpy as np
from model.music_downloadv2 import (
    Spider,
    WangYiYun,
)
from flask import (
    Flask,
    render_template,
    request,
    redirect,
    url_for,
)
from model.MelLearning import(
    transFormat,
    getMelPic
)
from model.tuneAnalyse.call_predictor import(
    predictor
)
from model.lyricAnalyse.get_result import(
    result
)
# 先要初始化一个 Flask 实例
# @app.route('/', methods=['GET'])
# def index():
#     return render_template("index.html")

app = Flask(__name__, static_folder='views/statics')
app = Flask(__name__, static_url_path='')


@app.route('/list.search', methods=['GET'])
def search():
    # print(request.args)
    spider = Spider()
    songs = spider.run(request.args['search'])
    return songs


@app.route('/list.isFree', methods=['GET'])
def isFree():
    spider = Spider()
    songs = spider.run(request.args['songName'])
    songs = json.loads(songs)
    for i in songs['data']:
        # print(i)
        if int(request.args['songNum']) == i[0]:
            if spider.download_music(int(i[8])) == "notFree":
                return "notFree"
            else:
                return "isFree"


@app.route('/analyse.lyric', methods=['GET'])
def lyricAnalyse():
    spider = Spider()
    songs = spider.run(request.args['songName'])
    songs = json.loads(songs)
    # print("songsType:",type(songs))
    # print("songs['data']:",songs['data'])
    for i in songs['data']:
        # print(i)
        if int(request.args['songNum']) == i[0]:
            spider.download_music(int(i[8])) == "notfree"
            # return i[6]
            mylist = (i[1], i[6], i[7])
            myjson = json.dumps(mylist)
            return myjson


@app.route('/analyse.tune', methods=['GET'])
def tuneAnalyse():
    root = 'C:/Users/echo1999/Documents/Github/MusicAnalyse/static/myData/'
    if os.path.exists(root + 'wav/0.wav'):
        os.remove(root + 'wav/0.wav')
    if os.path.exists(root + 'wav/1_show.wav'):
        os.remove(root + 'wav/1_show.wav')
    if os.path.exists('C:/Users/echo1999/Documents/Github/MusicAnalyse/download.mp3'):
        os.remove('C:/Users/echo1999/Documents/Github/MusicAnalyse/download.mp3')
    if os.listdir(root + 'picture') != []:
        os.remove(root + 'picture/1_show_None.png')
        os.remove(root + 'picture/0_None.png')
    unprocessed_file = root + 'musicDownload'  # 待处理音频文件所在目录
    transedToWav = root + 'wav/'  # 格式转换完毕后存放地址
    mfccPic_path = root + 'picture'
    if transFormat(unprocessed_file, transedToWav) == "tooShort":
        return "tooShort"
    getMelPic(transedToWav, mfccPic_path)
    if os.listdir(root + 'musicDownload') != []:
        os.remove(root + 'musicDownload/download.mp3')
    return "ok"


@app.route('/analyse.tuneResult', methods=['GET'])
def tuneResult():
    path = r"C:\Users\echo1999\Documents\Github\MusicAnalyse\static\myData\picture\0_None.png"
    result = predictor(path)
    return result


@app.route('/analyse.lyricResult', methods=['GET'])
def lyricResult():
    # print("request.args['songLyric']:", request.args['songLyric'])
    lyric = request.args['songLyric']
    lyricResult = result(lyric)
    print("lyricResult:", lyricResult)
    return lyricResult


# 运行服务器
if __name__ == '__main__':
        # debug 模式可以自动加载你对代码的变动, 所以不用重启程序
        # host 参数指定为 '0.0.0.0' 可以让别的机器访问你的代码
    config = dict(
        debug=False,
        host='0.0.0.0',
        port=2000,
    )
    app.run(**config)
    # app.run() 开始运行服务器
    # 所以你访问下面的网址就可以打开网站了
    # http://127.0.0.1:2000/
    # lyricResult()
