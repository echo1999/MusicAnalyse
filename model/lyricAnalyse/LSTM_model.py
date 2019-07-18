import tensorflow as tf
from tensorflow.contrib import learn
from tensorflow.python.ops.rnn import static_rnn
from tensorflow.python.ops.rnn_cell_impl import BasicLSTMCell

# 配置信息
embedding_size = 50
num_classes = 2
max_document_length = 100

def model(input,vocab_size):

    # 构建随机的词向量矩阵
    # tf.get_variable(name,  shape, initializer): name变量的名称，shape变量的维度，initializer变量初始化的方式
    embeddings = tf.get_variable("embeddings", [vocab_size, embedding_size], initializer=tf.truncated_normal_initializer)
    embedded = tf.nn.embedding_lookup(embeddings, input)

    # 将数据处理成LSTM的输入格式（时序）
    rnn_input = tf.unstack(embedded, max_document_length, axis=1, name="rnn-input")

    # 定义LSTM
    lstm_cell = BasicLSTMCell(20, forget_bias=1.0)
    rnn_outputs, rnn_states = static_rnn(lstm_cell, rnn_input, dtype=tf.float32)

    # predict
    logits = tf.layers.dense(rnn_outputs[-1], num_classes)
    predicted_labels = tf.argmax(logits, axis=1)

    return predicted_labels, [embeddings, embedded, lstm_cell, logits]
