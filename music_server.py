import json
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


# @app.route('/list.download', methods=['GET'])
# def download():
#     # print(request.args)
#     spider = Spider()
#     # songs = spider.run(request.args['search'])
#     download = spider.__download_music(request.args['songID'])
#     # with open('./song.json', encoding='utf-8') as f:
#     #     temp = json.loads(f.read())
#     #     # print(type(temp))
#     #     # print(temp)
#     # songs = json.dumps(temp)
#     return songs


@app.route('/analyse.lyric', methods=['GET'])
def lyric():
    with open('./song.json', encoding='utf-8') as f:
        temp = json.loads(f.read())
        # print(type(temp))
        # print(temp)
    # songs = json.dumps(temp)
    # download = spider.__download_music(request.args['songID'])
    # print("songs Type",type(temp))
    # print(temp)
    # print("songs.data",songs.data[0])
    # print("temp['data] Type",type(temp['data']))
    print(temp['data'])
    for i in temp['data']:
        # print(type(i))
        # print("i",i)
        # print(i[0])
        for j in i:
            if request.args['songnum'] == i[j]:
                return 
        # e = temp['data'][i]
    #     print(e)
    #     # if request.args['songnum'] == e[0]:
    #     #     return e[6]
    #     pass
    # return songs
    # b=for e in temp['data'] for i in e
    # b[0]
    # b[0+j+5]


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
