import ffmpeg
import re
import sklearn
import os
import librosa
import librosa.display
import numpy as np
import matplotlib.pyplot as plt
from pydub import AudioSegment
import shutil


def transFormat(import_path, export_path):

    dirs = os.listdir(import_path)
    
    i = 0
    for file in dirs:
        # print(file)
        if re.match('.*.mp3', file):
            source_file = import_path+ "/" +file
            splited_name = file.split(".")
            # print(splited_name)
            processed_file = export_path+ str(i) +".wav"
            i += 1
            print(file)

            try:
                cutted_wav = AudioSegment.from_mp3(source_file)
                # sound.export(processed_file,format ='wav')
            except:
                print('MP3文件有问题')
                continue
            
            # cutted_wav = AudioSegment.from_wav(processed_file)
            cutted_wav = cutted_wav[25*1000:]
            wav_len = len(cutted_wav)
            cutted_wav = cutted_wav[: wav_len-25*1000]
            # 取中间截取后的前40秒
            wav_len = wav_len/2
            if wav_len <= 39*1000:
                continue
            else:
                cutted_wav = cutted_wav[wav_len - 41*1000:wav_len-1]
            
            wav_len = len(cutted_wav)
            
            if len(cutted_wav) == 40999:
                cutted_wav.export(processed_file, format="wav")
            else:
                continue

def getMelPic(export_path, mfccPic_path):
    # import_path = "G:/huawei/MUsicEmotionFilter/example"
    # import_path = "G:/huawei/MUsicEmotionFilter/happy_wav"
    dirs = os.listdir(export_path)

    for file in dirs:

        print(file)
        # print(file)
        if re.match('.*.wav', file):
            # print(file)

            plt.figure()

            x, fs = librosa.load(export_path + os.sep + file, sr=44100)
            # print(type(x))
            if len(x) == 0:
                continue
            # print(x)
            # 我们可以绘制音频数组librosa.display.waveplot：
            librosa.display.waveplot(x, sr=fs)
            # plt.show()
            # librosa.feature.mfcc 通过音频信号计算MFCC：
            mfccs = librosa.feature.mfcc(x, sr=fs)
            # print(mfccs.shape)
            # plt.show()
            # 使用sklearn.preprocessing.scale()函数，可以直接将给定数据进行标准化。
            mfccs = sklearn.preprocessing.scale(mfccs, axis=1)
            # print(mfccs.mean(axis=1))
            # print(mfccs.var(axis=1))
            # Displaying the MFCCs:
            # 我们可以使用显示频谱图： librosa.display.specshow.
            librosa.display.specshow(mfccs, sr=fs, x_axis='time')

            splited_name = file.split(".")

            plt.savefig(mfccPic_path + os.sep + splited_name[0] + "_None.png")

            plt.close()
            # X = librosa.stft(x)
            # Xdb = librosa.amplitude_to_db(abs(X))
            # plt.figure(figsize=(14, 5))
            # librosa.display.specshow(Xdb, sr=fs, x_axis='time', y_axis='hz')
            # plt.show()
        else:
            print("这不是一个wav文件")

def figurePicData():
    unprocessed_file = "C:/Users/echo1999/Documents/Github/MusicAnalyse/myData/MusicDownload"  # 待处理音频文件所在目录
    transedToWav = "C:/Users/echo1999/Documents/Github/MusicAnalyse/myData/wav/"  # 格式转换完毕后存放地址
    mfccPic_path = "C:/Users/echo1999/Documents/Github/MusicAnalyse/myData/picture"  # 存放wav格式文件转换mel频谱图的目录
    transFormat(unprocessed_file, transedToWav)
    getMelPic(transedToWav, mfccPic_path)
    # shutil.rmtree('../myData/MusicDownload')
    # os.mkdir('../myData/MusicDownload')
    # shutil.rmtree('../myData/picture')
    # os.mkdir('../myData/picture')
    if os.listdir('C:/Users/echo1999/Documents/Github/MusicAnalyse/myData/wav') != []:
        os.remove('C:/Users/echo1999/Documents/Github/MusicAnalyse/myData/wav/0.wav')
    if os.listdir('C:/Users/echo1999/Documents/Github/MusicAnalyse/myData/MusicDownload') != []:
        os.remove('C:/Users/echo1999/Documents/Github/MusicAnalyse/myData/MusicDownload/download.mp3')
    # os.remove(
    #         '../myData/wav/0.wav')

# figurePicData()
