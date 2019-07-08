import json
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
    # spider = Spider()
    # songs = spider.run(request.args['search'])
    with open('./song.json', encoding='utf-8') as f:
        temp = json.loads(f.read())
        # print(type(temp))
        # print(temp)
    songs = json.dumps(temp)
    return songs
    # return songs


@app.route('/analyse.lyric', methods=['GET'])
def lyric():
    spider = Spider()
    with open('./song.json', encoding='utf-8') as f:
        temp = json.loads(f.read())
        # print(type(temp))
        # print(temp)
    songs = json.dumps(temp)
    # url = 
    url = spider.__get_mp3(songs[int(request.args['songnum'])][7])
    if not url:
        print('歌曲需要收费，下载失败')
    else:
        filename = songs[int(request.args['songnum'])][1]
        spider.__download_mp3(url, filename)

    with open('./song.json', encoding='utf-8') as f:
        temp = json.loads(f.read())
    
    for i in temp['data']:
        for j in i:
            if int(request.args['songnum']) == i[j]:
                # return i[6]
                mylist = (i[1],i[6],i[7])
                myjson = json.dumps(mylist)
                # myjson = fp.json.dump(mylist)
                return myjson
                




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
