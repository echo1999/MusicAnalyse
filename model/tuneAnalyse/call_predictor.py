import tensorflow as tf
import numpy as np
import sys


def predictor(path):
    # 模型目录
    # 训练后生成的检查点文件夹，在当前工程下。
    CHECKPOINT_DIR = r'C:\Users\echo1999\Documents\Github\MusicAnalyse\model\tuneAnalyse\runs\1562719894\checkpoints'
    INCEPTION_MODEL_FILE = r'C:\Users\echo1999\Documents\Github\MusicAnalyse\model\tuneAnalyse\tensorflow_inception_graph.pb'

    # inception-v3模型参数
    BOTTLENECK_TENSOR_NAME = 'pool_3/_reshape:0'  # inception-v3模型中代表瓶颈层结果的张量名称
    JPEG_DATA_TENSOR_NAME = 'DecodeJpeg/contents:0'  # 图像输入张量对应的名称

    # 测试数据

    # path = sys.argv[1] 图片路径
    # path = r"C:\Users\echo1999\Documents\Github\MusicAnalyse\static\myData\picture\38_None.png"

    # 类别字典
    # disease_dict = {0: 'baifen', 1: 'tiaoxiu', 2: 'yexiu'}
    disease_dict = {0: 'happy', 1: 'sad'}


    # 读取数据
    image_data = tf.gfile.FastGFile(path, 'rb').read()

    # 评估
    checkpoint_file = tf.train.latest_checkpoint(CHECKPOINT_DIR)
    with tf.Graph().as_default() as graph:
        with tf.Session().as_default() as sess:
            # 读取训练好的inception-v3模型
            with tf.gfile.FastGFile(INCEPTION_MODEL_FILE, 'rb') as f:
                graph_def = tf.GraphDef()
                graph_def.ParseFromString(f.read())

            # 加载inception-v3模型，并返回数据输入张量和瓶颈层输出张量
            bottleneck_tensor, jpeg_data_tensor = tf.import_graph_def(
                graph_def,
                return_elements=[BOTTLENECK_TENSOR_NAME, JPEG_DATA_TENSOR_NAME])

            # 使用inception-v3处理图片获取特征向量
            bottleneck_values = sess.run(bottleneck_tensor, {jpeg_data_tensor: image_data})
            # 将四维数组压缩成一维数组，由于全连接层输入时有batch的维度，所以用列表作为输入
            bottleneck_values = [np.squeeze(bottleneck_values)]

            # 加载图和变量（这里我选择的是step=900的图，使用的是绝对路径。）
            saver = tf.train.import_meta_graph(
                r'C:\Users\echo1999\Documents\Github\MusicAnalyse\model\tuneAnalyse\runs\1562719894\checkpoints\model-9000.meta')
            saver.restore(sess, r'C:\Users\echo1999\Documents\Github\MusicAnalyse\model\tuneAnalyse\runs\1562719894\checkpoints\model-9000')

            # 通过名字从图中获取输入占位符
            input_x = graph.get_operation_by_name('BottleneckInputPlaceholder').outputs[0]

            # 我们想要评估的tensors
            predictions = graph.get_operation_by_name('evaluation/ArgMax').outputs[0]

            # 收集预测值
            all_predictions = []
            all_predictions = sess.run(predictions, {input_x: bottleneck_values})

            # 打印出预测结果
            index1 = str(all_predictions)[1]
            index = int(index1)
            print(disease_dict[index])
            return disease_dict[index]


