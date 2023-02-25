from django.shortcuts import render
import os
from haystack.views import SearchView
from SearchSystem.models import *
from django.http import HttpResponse
from .forms import UploadFileForm
import numpy as np
import librosa
import keras
import pandas as pd
from sklearn.preprocessing import StandardScaler
from .models import *


# Create your views here.

def inbase(request):  # 用来数据入库的一次性函数
    path = 'D:\PythonProjects\pythonProject\Image\\'
    image_list = os.listdir(path)
    for image in image_list:
        image_record = Images(location=path + image, name=image, tags=image.replace('.jpg', ''))
        image_record.save()
    return HttpResponse('数据入库已完成！')


def detail(request):
    picture = Images.objects.all()
    content = {'picture': picture}
    if request.method == 'GET':
        return render(request, 'search/true_result.html', content)
    return render(request, 'search/true_result.html', content)


# 一定要继承SearchView
class MySearchView(SearchView):

    # 重写人家的方法
    def create_response(self):
        # 人家的，就这样写，获取到的就是全部的东西
        context = self.get_context()
        data_list = []
        #   context['page'].object_list   这样获取到的就是  数据的list集合
        for sku in context['page'].object_list:
            # 获取表里面的数据，就是前缀就是sku.object
            print(sku.object.name)
            data_list.append({
                'tags': sku.object.tags,
                # 'id': sku.object.id,
                # 'name': sku.object.name,
                # 'location': sku.object.location
            })
        content = {}

        if data_list:
            content = {
                'active_menu': 'homepage',
                'xw_list': data_list,
            }
        else:
            xw_list = Images.objects.all()[0:1]
            content = {
                'active_menu': 'homepage',
                'xw_list': xw_list,
            }

        xw_list = Images.objects.all()[0:1]
        content = {'xw_list': xw_list}
        # 渲染到我们自己写的页面
        return render(self.request, 'search/search.html', {"context": context, "content": content})


def search_image(request):
    if request.method == "GET":
        return render(request, 'search/search.html')
    if request.method == "POST":
        # 获取用户搜索的图片
        search_image = request.POST.get('image')
        '''
        加载图片预处理模块
        得到search_tags
        
        '''
        images_list = Images.objects.all()
        content = {'images_result': images_list}
        return render(request, 'image_search.html', content)


def search_text(request):
    if request.method == "GET":
        return render(request, 'base_text.html')


def search_music(request):
    if request.method == "GET":
        return render(request, 'base_music.html')
    if request.method == "POST":
        # 获取用户搜索的音频并处理
        file = request.FILES.get('music', None)
        if file is None:
            return render(request, 'base_music.html')
        else:
            with open("D:\PythonProjects\MultiMedia\SearchSystem\\tmp\music.wav", 'wb+') as f:
                for chunk in file.chunks():
                    f.write(chunk)
            class_mapping = {
                0: 'blues',
                1: 'classical',
                2: 'country',
                3: 'disco',
                4: 'hiphop',
                5: 'jazz',
                6: 'metal',
                7: 'pop',
                8: 'reggae',
                9: 'rock'
            }
            audio_file = 'D:\PythonProjects\MultiMedia\SearchSystem\\tmp\music.wav'
            # 截取音频文件的中间30s
            duration = librosa.get_duration(filename=audio_file)  # 获取音频时长
            start = (duration - 30) / 2  # 计算中间30秒的起始点
            new_audio, sr = librosa.load(audio_file, sr=22050, duration=30, offset=start)  # 读取音频文件的中间30s

            # 长度
            length = np.shape(new_audio)

            # 提取色度频率特征chroma_stft
            chroma_stft = librosa.feature.chroma_stft(y=new_audio, sr=sr)
            chroma_stft_mean = np.mean(chroma_stft)
            chroma_stft_var = np.var(chroma_stft)

            # 提取均方根特征rms
            rms = librosa.feature.rms(y=new_audio)
            rms_mean = np.mean(rms)
            rms_var = np.var(rms)

            # 提取谱质心特征spectral_centroid
            spectral_centroids = librosa.feature.spectral_centroid(y=new_audio, sr=sr)
            spectral_centroid_mean = np.mean(spectral_centroids)
            spectral_centroid_var = np.var(spectral_centroids)

            # 提取谱带宽特征spectral_bandwidth
            spectral_bandwidths = librosa.feature.spectral_bandwidth(y=new_audio, sr=sr)
            spectral_bandwidth_mean = np.mean(spectral_bandwidths)
            spectral_bandwidth_var = np.var(spectral_bandwidths)

            # 提取衰减特征rolloff
            rolloff = librosa.feature.spectral_rolloff(y=new_audio, sr=sr)
            rolloff_mean = np.mean(rolloff)
            rolloff_var = np.var(rolloff)

            # 提取过零率特征zero_crossing_rate
            zcr = librosa.feature.zero_crossing_rate(new_audio)
            zcr_mean = np.mean(zcr)
            zcr_var = np.var(zcr)

            # 提取谐波特征harmony和感知特征perceptr
            harmony, perceptr = librosa.effects.hpss(new_audio)
            harmony_mean = np.mean(harmony)
            harmony_var = np.var(harmony)
            perceptr_mean = np.mean(perceptr)
            perceptr_var = np.var(perceptr)

            # 提取节奏特征tempo
            tempo = librosa.beat.tempo(y=new_audio)

            # 提取梅尔倒谱系数MFCC特征
            mfccs = librosa.feature.mfcc(y=new_audio, sr=sr, n_mfcc=20)
            mfccs_mean = np.mean(mfccs, axis=1)
            mfccs_var = np.var(mfccs, axis=1)

            # 将平均值和方差分配到偶数和奇数位置上,与csv文件对齐
            mfccs_processed = np.zeros((40,))
            mfccs_processed[::2] = mfccs_mean
            mfccs_processed[1::2] = mfccs_var

            # 组织为一个特征向量
            features = np.concatenate(
                (length, chroma_stft_mean, chroma_stft_var, rms_mean, rms_var, spectral_centroid_mean,
                 spectral_centroid_var, spectral_bandwidth_mean, spectral_bandwidth_var, rolloff_mean,
                 rolloff_var, zcr_mean, zcr_var, harmony_mean, harmony_var, perceptr_mean, perceptr_var,
                 tempo, mfccs_processed), axis=None)

            # 加入原数据集以归一化
            data = pd.read_csv("D:\PythonProjects\MultiMedia\SearchSystem\modelfile\\features_30_sec.csv")  # 读取CSV文件
            data = data.drop(labels="filename", axis=1)  # 删除标签为filename的数据，axis=1表示从列中删除
            data = data.drop(labels="label", axis=1)  # 删除标签为filename的数据，axis=1表示从列中删除
            data.loc[len(data.index)] = features

            fit = StandardScaler()
            X = fit.fit_transform(np.array(data.iloc[:, :], dtype=float))  # 均值方差归一化

            # 提取归一化后的待预测数据
            music = X[-1]

            # 加载已经训练好的模型
            model = keras.models.load_model('D:\PythonProjects\MultiMedia\SearchSystem\modelfile\\audio_model.h5')

            # 使用模型进行预测
            y_pred = model.predict(music.reshape(1, -1))
            predicted_class = np.argmax(y_pred, axis=1)
            predicted_genre = class_mapping[predicted_class[0]]
            print('Predicted class:', predicted_genre)

        music_list = Music.objects.filter(tag=predicted_class[0])
        content = {'music_result': music_list}
        return render(request, 'music_result.html', content)


# 保存上传的音频和图片
def save_music(file):
    with open('tmp/music.wav', 'wb+') as destination:
        for chunk in file.chunks():
            destination.write(chunk)


def save_image(file):
    with open('tmp/...', 'wb+') as destination:
        for chunk in file.chunks():
            destination.write(chunk)
