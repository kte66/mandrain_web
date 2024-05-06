import os

from .speech_model import ModelSpeech
from .speech_model_zoo import SpeechModel251BN
from .speech_features import Spectrogram
from .language_model3 import ModelLanguage

yunmu = ["a", "o", "e", "i", "u", "v", "ai", "ei", "ui", "ao", "ou", "iu", "ie", "ve", "er", "an", "en", "in", "vn", "ang", "eng", "ing", "ong"]
shengmu = ["b", "p", "m", "f", "d", "t", "n", "l", "g", "k", "h", "j", "q", "x", "zh", "ch", "sh", "r", "z", "c", "s", "y", "w"]

os.environ["CUDA_VISIBLE_DEVICES"] = "0"
# print('输入语音为：当打不出中文时，就切换到日语键盘，打几个日语')
    # print('声学模型语音识别结果：')
    # std_res = ["dang1", "da3", "bu4", "chu1", "zhong1", "wen2", "shi2", "jiu4", "qie1", "huan4", "dao4", "ri4", "yu3", "jian4", "pan2", "da3", "ji3", "ge4", "ri4", "yu3"]
def score_voice(wav_file_name, std_res):
    AUDIO_LENGTH = 1600
    AUDIO_FEATURE_LENGTH = 200
    CHANNELS = 1
    # 默认输出的拼音的表示大小是1428，即1427个拼音+1个空白块
    OUTPUT_SIZE = 1428
    sm251bn = SpeechModel251BN(
        input_shape=(AUDIO_LENGTH, AUDIO_FEATURE_LENGTH, CHANNELS),
        output_size=OUTPUT_SIZE
        )
    feat = Spectrogram()
    ms = ModelSpeech(sm251bn, feat, max_label_length=64)
    ms.load_model('./mandrain_web/mandrain_model/save_models/' + sm251bn.get_model_name() + '.model.h5')
    reco_res = ms.recognize_speech_from_file(wav_file_name)
    # print('输入语音为：当打不出中文时，就切换到日语键盘，打几个日语')
    print('声学模型语音识别结果：')
    # std_res = ["dang1", "da3", "bu4", "chu1", "zhong1", "wen2", "shi2", "jiu4", "qie1", "huan4", "dao4", "ri4", "yu3", "jian4", "pan2", "da3", "ji3", "ge4", "ri4", "yu3"]
    score = 0
    err = []
    for i in range(len(reco_res)):
        if i + 1 > len(std_res):
            break
        if reco_res[i] == std_res[i]:
            score += 1
        else:
            err.append([i, reco_res[i]])
    score = 100 * score / len(std_res)
    print("读错的地方：", err)
    print("评分：%.2f" % score)
    print(reco_res)
    print(std_res)
    return err, score
# res = ms.recognize_speech_from_file('./dataset/filename6.wav')
# print('输入语音为：中国空军损失各种飞机，包括训练损失2468架')
# print('声学模型语音识别结果：', end='')
# for si in res:
#     print(si, end=' ')
#
# res = ms.recognize_speech_from_file('./dataset/filename7.wav')
# print('输入语音为：轨道交通经营单位应当按照轨道交通突发事件应急处置方案')
# print('声学模型语音识别结果：', end='')
# for si in res:
#     print(si, end=' ')
#
# res = ms.recognize_speech_from_file('./dataset/filename2.wav')
# print('输入语音为：思维方式、社会特性以及文化、历史等')
# print('声学模型语音识别结果：', end='')
# for si in res:
#     print(si, end=' ')
#
# res = ms.recognize_speech_from_file('./dataset/filename5.wav')
# print('输入语音为：办公室主要负责211工程')
# print('声学模型语音识别结果：', end='')
# for si in res:
#     print(si, end=' ')

