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

# 先要初始化一个 Flask 实例
# app = Flask(__name__, static_folder='views/statics')
app = Flask(__name__, static_url_path='')
@app.route('/', methods=['GET'])
def index():
    return render_template("index.html")


# @app.route('/', methods=['GET'])
# def index():
#     return render_template("index.html")

@app.route('/list.search', methods=['GET'])
def search():
    # print(request.args)
    spider = Spider()
    songs = spider.run(request.args['search'])
    # with open('./song.json', encoding='utf-8') as f:
    #     temp = json.loads(f.read())
        # print(type(temp))
        # print(temp)
    # songs = json.dumps(temp)
    return songs
    # return songs


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
            spider.download_music(int(i[8]))
            # return i[6]
            mylist = (i[1],i[6],i[7])
            myjson = json.dumps(mylist)
            # myjson = fp.json.dump(mylist)
            return myjson


@app.route('/analyse.tune', methods=['GET'])
def tuneAnalyse():
    if os.listdir(r'C:\Users\echo1999\Documents\Github\MusicAnalyse\static\myData\picture') != []:
        os.remove(r'C:\Users\echo1999\Documents\Github\MusicAnalyse\static\myData\picture\0_None.png')
    unprocessed_file = r"C:\Users\echo1999\Documents\Github\MusicAnalyse\static\myData\musicDownload"  # 待处理音频文件所在目录
    transedToWav = r"C:\Users\echo1999\Documents\Github\MusicAnalyse\static\myData\wav"  # 格式转换完毕后存放地址
    # 存放wav格式文件转换mel频谱图的目录
    mfccPic_path = r"C:\Users\echo1999\Documents\Github\MusicAnalyse\static\myData\picture"
    transFormat(unprocessed_file, transedToWav)
    getMelPic(transedToWav, mfccPic_path)
    if os.listdir(r'C:\Users\echo1999\Documents\Github\MusicAnalyse\static\myData\musicDownload') != []:
        os.remove(
            r'C:\Users\echo1999\Documents\Github\MusicAnalyse\static\myData\musicDownload\download.mp3')
    if os.listdir(r'C:\Users\echo1999\Documents\Github\MusicAnalyse\static\myData\wav') != []:
        os.remove(
            r'C:\Users\echo1999\Documents\Github\MusicAnalyse\static\myData\wav\0.wav')
    return "ok"


# 运行服务器
if __name__ == '__main__':
        # debug 模式可以自动加载你对代码的变动, 所以不用重启程序
        # host 参数指定为 '0.0.0.0' 可以让别的机器访问你的代码
    config = dict(
        debug=True,
        host='0.0.0.0',
        port=2000,
    )
    app.run(**config)
    # app.run() 开始运行服务器
    # 所以你访问下面的网址就可以打开网站了
    # http://127.0.0.1:2000/
