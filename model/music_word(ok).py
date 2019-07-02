import requests
import json
import urllib
import re
from bs4 import BeautifulSoup


def download_by_musicId(music_id):
	url = "http://music.163.com/api/song/lyric?" +"id=" + str(music_id) + "&lv=1&kv=1&tv=-1"
	result = requests.get(url)
	json_obj = result.text

	json_obj = json.loads(json_obj)
	final_lyric = ""
	if( "lrc" in json_obj):
		inital_lyric = json_obj['lrc']['lyric']
		regex = re.compile(r'\[.*\]')
		final_lyric = re.sub(regex,'',inital_lyric).strip()

	return final_lyric

def getSongId_by_playList(playlist_id):
	# 网易云上的民谣歌单
	url = "http://music.163.com/api/playlist/detail?id=" + str(playlist_id) + "&updateTime=-1"
	header = {
        'Host': 'music.163.com',
        'Refer': 'https://music.163.com',
        'User-Agent': 'Mozilla/5.0 (Windows NT 6.3; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/61.0.3163.100 Safari/537.36',
        'Content-Type': 'application/x-www-form-urlencoded',
        'Accept': '*/*',
        'Accept-Encoding': 'gzip, deflate',
        'Accept-Language': 'zh-CN,zh;q=0.8',
        'Cookie': 'os=pc; deviceId=B55AC773505E5606F9D355A1A15553CE78B89FC7D8CB8A157B84; osver=Microsoft-Windows-8-Professional-build-9200-64bit; appver=1.5.0.75771; usertrack=ezq0alR0yqJMJC0dr9tEAg==; MUSIC_A=088a57b553bd8cef58487f9d01ae'
    }
	res = requests.get(url,headers = header)
	res = res.text
	# 将网页转化为xml
	soup = BeautifulSoup(res,'lxml')
	song = soup.p.string
	songlist = json.loads(song)
	songlist = songlist["result"]["tracks"]

	return songlist

def ConvertStrToFile(filename,str):
	with open('songlist/'+filename+".txt",'w',encoding='utf-8') as f:
		f.write(str)

def getAllSongByplaylist(playlist_id):
	songlist = getSongId_by_playList(playlist_id)
	for item in songlist:
		ConvertStrToFile(item["name"],download_by_musicId(item["id"]))
		#print(item["name"])
	print("写入文件成功")

getAllSongByplaylist(2253642724)