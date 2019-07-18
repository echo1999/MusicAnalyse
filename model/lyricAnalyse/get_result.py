import re
import jieba
import tensorflow as tf
from tensorflow.python.ops.rnn import static_rnn
from tensorflow.python.ops.rnn_cell_impl import BasicLSTMCell
import os
import numpy as np
import sys
sys.path.append(
    r"C:\Users\echo1999\Documents\Github\MusicAnalyse\model\lyricAnalyse")

import LSTM
# tf.reset_default_graph()

def result(lyric):
    saver = tf.train.import_meta_graph(
        r'C:\Users\echo1999\Documents\Github\MusicAnalyse\model\lyricAnalyse\Model\checkpoints\model-10.meta')
    # y = graph.get_tensor_by_name("y:0")
    # datas_placeholder = graph.get_tensor_by_name("Placeholder_Data:0")
    print("lyric:",lyric)
    content = re.sub(r'(.*:.*\n|.*：.*\n|\n\n+)*', '', lyric)
    # print("去冗余信息后:",content)
    # 定义一个空字符串
    final = ""
    word = jieba.lcut(content)
    # print("jieba分词后:",word)
    for i in word:
        if i == "\n":
            final += " "
        else:
            final += i + " "
    # print("分词后处理效果：",final)

    # stopwords = [line.strip() for line in open('./model/lyricAnalyse/stopword.txt', 'r', encoding='utf-8').readlines()]
    stopwords = [line.strip() for line in open(
        r'C:\Users\echo1999\Documents\Github\MusicAnalyse\model\lyricAnalyse\stopword.txt', 'r', encoding='utf-8').readlines()]
    content = "".join(final)
    outstr = ''  # 待返回字符串
    for word in content:
        if word not in stopwords:
            outstr += word
    # print("去除停用词后：",outstr)
    l = []
    outstr=outstr.split()
    for line_one in outstr:
        # 去重操作
        if line_one not in l:
            l.append(line_one)
    str4 = " ".join(l)
    print("str4:",str4)
    # print("去重以后：",str4)
    #模型节点
    # 按测试集建立字典
    pre_text=[]
    pre_text.append(str4)
    pre = np.array(list(LSTM.vocab_processor.transform(pre_text)))

    # labels_placeholder = tf.placeholder(tf.int32, [None])
    # losses = tf.nn.softmax_cross_entropy_with_logits_v2(labels=tf.one_hot(labels_placeholder, 2),
    #                                                     logits=variables[-1])
    # mean_loss = tf.reduce_mean(losses)
    # optimizer = tf.train.AdamOptimizer(learning_rate=1e-2).minimize(mean_loss)
    
    # global graph
    # graph = tf.get_default_graph()



    # with graph.as_default():
    with tf.Session() as sess:
        print("@@@@@@@@@@@@@@@@@@@@@@@@@")
        # print("tf.train.Saver():::::::", tf.train.Saver())
        # saver = tf.train.Saver()
        # print("saver::::", saver)
        saver.restore(sess, tf.train.latest_checkpoint(
            r"C:\Users\echo1999\Documents\Github\MusicAnalyse\model\lyricAnalyse\Model\checkpoints"))  # 注意此处路径前添加"./"


        print("***********", pre)
        predicted_labels_val = sess.run("y:0", feed_dict={"Placeholder:0": pre})
  
        label = predicted_labels_val[0]
        # label_name = label_name_dict[label]
        print("{0} => {1}".format(str4, label))
    
        if label == 0:
            return "happy"
        else:
            return "sad"

if __name__ == "__main__":
    lyric = "作曲: 逃跑计划 作词: 逃跑计划Oh honey我脑海里全都是你oh 无法抗拒的心悸难以呼吸tonight是否又要错过\n\
    一个夜晚是否还要掩饰最后的期待oh tonight一万次悲伤依然会有dream我一直在最温暖的地方等你似乎只能这样 停留一\n\
    个方向已不能改变每一颗眼泪 是一万道光最昏暗的地方也变得明亮我奔涌的暖流 寻找你的海洋我注定这样oh honey你目\n\
    光里充满忧郁就像经历一片废墟 难以逃避tonight是否还要错过这个夜晚是否还要熄灭所有的期待oh tonight一万次悲伤\n\
    依然会有dream我一直在最后的地方等你似乎只能这样 停留一个方向已不能改变每一颗眼泪 是一万道光最昏暗的地方也\n\
    变得明亮我奔涌的暖流 寻找你的海洋我注定这样一万次悲伤依然会有dream我一直在最后的地方等你似乎只能这样 停留\n\
    一个方向已不能改变每一颗眼泪 是一万道光最昏暗的地方也变得明亮我奔涌的暖流 寻找你的海洋我注定这样oh honey我\n\
    脑海里全都是你oh 无法抗拒的心悸难以呼吸"

    lyricresult=result(lyric)
    print(lyricresult)

