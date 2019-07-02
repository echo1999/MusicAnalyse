import jieba
import matplotlib as mpl
import matplotlib.pyplot as plt
from wordcloud import WordCloud
import re
import os


filepath = 'songlist_delete'
file_names =os.listdir(filepath)
for file_name in file_names:

    # 打开文件夹，读取内容，并进行分词
    with open(filepath+'/'+file_name, 'r', encoding='utf-8') as f:
        # 定义一个空字符串
        final = ""
        for line in f.readlines():
            word = jieba.lcut(line)

            for i in word:
                if i =="\n":
                    final += i
                else:
                    final += i+" "
            with open('songlist_jieba/'+file_name, 'w+', encoding='utf-8') as fp:
                fp.write(final)
