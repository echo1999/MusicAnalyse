#coding = utf-8
import re
import os

filepath = 'songlist'
file_names =os.listdir(filepath)
for file_name in file_names:

    with open('songlist/'+file_name, 'r',encoding='utf-8') as fpr:
        content = fpr.read()
    #去掉开头歌曲冗余信息
    #content = content.replace(r'^作曲 :|^ 作词 :', '')
    #content = re.sub(r'(作曲 : .*\n| 作词 :.*\n|制作人:.*\n|编曲:.*\n|监制:.*\n|吉他:.*\n|\
    #古典吉他:.*\n|录音缩混:.*\n|和声:.*\n|打击乐:.*\n|大提琴:.*\n)*', '', content)
    content = re.sub(r'(.*:.*\n|.*：.*\n|\n\n+)*', '', content)
    with open('songlist_delete/'+file_name, 'w',encoding='utf-8') as fpw:
        fpw.write(content)