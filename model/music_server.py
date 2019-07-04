import json
from music_download import (
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
app = Flask(__name__)
# host www.qq.com
# router /list.music
# query ?a=123
@app.route('/list.search', methods=['GET'])
def hello_world():
    spider = Spider()
    songs = spider.run('一万次悲伤')
    return songs


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
