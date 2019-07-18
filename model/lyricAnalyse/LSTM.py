# -*- coding: utf-8 -*-
import tensorflow as tf
from tensorflow.contrib import learn
import numpy as np
import os
import time
from tensorflow.python.framework import graph_util
import sys
sys.path.append(
    r"C:\Users\echo1999\Documents\Github\MusicAnalyse\model\lyricAnalyse")
import LSTM_model

CHECKPOINT_EVERY = 10
NUM_CHECKPOINTS = 5

# 数据
positive_texts = []
filepath = os.listdir(r"C:\Users\echo1999\Documents\Github\MusicAnalyse\model\lyricAnalyse\songlist_happy_quchong")
for file in filepath:
    with open(r"C:\\Users\\echo1999\\Documents\\Github\\MusicAnalyse\\model\\lyricAnalyse\\songlist_happy_quchong\\" + file, 'r',
            encoding='utf-8') as readfile:
        positive_texts.append(readfile.read())
# print("positive_texts:",positive_texts)

negative_texts = []
filepath1 = os.listdir(r"C:\Users\echo1999\Documents\Github\MusicAnalyse\model\lyricAnalyse\songlist_sad_quchong")
for file1 in filepath1:
    with open(r"C:\\Users\\echo1999\\Documents\\Github\\MusicAnalyse\\model\\lyricAnalyse\\songlist_sad_quchong\\" + file1, 'r',
            encoding='utf-8') as readfile1:
        negative_texts.append(readfile1.read())
# print("negative_texts:",negative_texts)

# 标签
label_name_dict = {
    0: "正面情感",
    1: "负面情感"
}

# pre_texts = []
# filepath2 = os.listdir("./model/lyricAnalyse/songlist_sad_quchong/")
# for file2 in filepath2:
#     with open("./model/lyricAnalyse/songlist_sad_quchong/" + file2, 'r',
#             encoding='utf-8') as readfile2:
#         pre_texts.append(readfile2.read())
# a = len(pre_texts)

# filepath3 = os.listdir("./model/lyricAnalyse/songlist_happy_quchong/")
# for file3 in filepath3:
#     with open("./model/lyricAnalyse/songlist_happy_quchong/" + file3, 'r',
#             encoding='utf-8') as readfile3:
#         pre_texts.append(readfile3.read())
# b = len(pre_texts) - a
# # 测试标签
# label_test = [1] * a + [0] * b

# 将文本和标签矢量化
all_texts = positive_texts + negative_texts
labels = [0] * len(positive_texts) + [1] * len(negative_texts)




# 配置信息
embedding_size = 50
num_classes = 2


max_document_length = 100
vocab_processor = learn.preprocessing.VocabularyProcessor(max_document_length)
# print(labels)
# 按训练集建立字典
datas = np.array(list(vocab_processor.fit_transform(all_texts)))

# # 按测试集建立字典
# pre = np.array(list(vocab_processor.transform(pre_texts)))

# 字典长度
vocab_size = len(vocab_processor.vocabulary_)

datas_placeholder = tf.placeholder(tf.int32, [None, max_document_length])
tf.identity(datas_placeholder, name='Placeholder_Data')

y, variables =LSTM_model.model(datas_placeholder, vocab_size)
tf.identity(y, name='y')

labels_placeholder = tf.placeholder(tf.int32, [None])
tf.identity(labels_placeholder, name='Placeholder_Label')

losses = tf.nn.softmax_cross_entropy_with_logits_v2(labels=tf.one_hot(labels_placeholder, 2),
                                                    logits=variables[-1])
mean_loss = tf.reduce_mean(losses)
# optimizer = tf.train.AdamOptimizer(learning_rate=1e-2).minimize(mean_loss)
optimizer = tf.train.AdamOptimizer(learning_rate=1e-2).minimize(mean_loss)






# feed_dict = {
#     datas_placeholder: datas,
#     labels_placeholder: labels
# }

# 模型和摘要的保存目录
# out_dir = os.path.abspath(os.path.join(os.path.curdir, 'Model'))
out_dir  = r"C:\Users\echo1999\Documents\Github\MusicAnalyse\model\lyricAnalyse\Model"
# print('\nWriting to {}\n'.format(out_dir))
# 损失值和正确率的摘要
loss_summary = tf.summary.scalar('loss', losses)
# acc_summary = tf.summary.scalar('accuracy', evaluation_step)

# 保存检查点
# checkpoint_dir = os.path.abspath(os.path.join(out_dir, 'checkpoints'))
checkpoint_dir = r"C:\Users\echo1999\Documents\Github\MusicAnalyse\model\lyricAnalyse\Model\checkpoints"
checkpoint_prefix = os.path.join(checkpoint_dir, 'model')
if not os.path.exists(checkpoint_dir):
    os.makedirs(checkpoint_dir)
saver = tf.train.Saver(tf.global_variables(), max_to_keep=NUM_CHECKPOINTS)
# print(tf.global_variables())

def train():
    with tf.Session() as sess:
        sess.run(tf.global_variables_initializer())
        tf.train.write_graph(sess.graph_def, r"C:\Users\echo1999\Documents\Github\MusicAnalyse\model\lyricAnalyse\Model", 'train.pbtxt')
        print("Graph saved")
        # 训练摘要
        # train_summary_op = tf.summary.merge([loss_summary, acc_summary])
        train_summary_dir = os.path.join(out_dir, 'summaries', 'train')
        train_summary_writer = tf.summary.FileWriter(train_summary_dir, sess.graph)
        # 开发摘要
        # dev_summary_op = tf.summary.merge([loss_summary, acc_summary])
        dev_summary_dir = os.path.join(out_dir, 'summaries', 'dev')
        dev_summary_writer = tf.summary.FileWriter(dev_summary_dir, sess.graph)

        for step in range(20):
            sess.run(optimizer, feed_dict={datas_placeholder: datas, labels_placeholder: labels})
            val = sess.run(mean_loss, feed_dict={datas_placeholder: datas, labels_placeholder: labels})
            if step % 10 == 0:
                print("step = {}\t mean loss ={}".format(step, val))

            # 每隔checkpoint_every保存一次模型和测试摘要
            if step % CHECKPOINT_EVERY == 0:
                # dev_summary_writer.add_summary(dev_summaries, i)
                path = saver.save(sess, checkpoint_prefix, global_step=step)
                print('Saved model checkpoint to {}\n'.format(path))

    # print("predict")
    # # 预测
    # predicted_labels_val = sess.run(y, feed_dict={variables[1]: pre})
    # count=0
    # sum = len(pre_texts)
    # for i, text in enumerate(pre_texts):
    #     label = predicted_labels_val[i]
    #     label_name = label_name_dict[label]
    # # print("{0} => {1},原始为：{2}".format(text, label_name,label_test[i]))
    #     pre_label = label_test[i]
    #     if pre_label == label:
    #         count+=1
    #     print("{0} => {1},原始为:{2}".format(text, label, pre_label))
    # print("accuray:", count/sum)

if __name__ == '__main__':
    train()
