from .mandrain_model.use_model import score_voice
import json
import os
import re
import time
import uuid
from pydub import AudioSegment
from django.http import HttpResponse
from django.views.decorators.http import require_http_methods
from django.views.decorators.csrf import csrf_exempt
from django.core.files.storage import default_storage


@require_http_methods(["GET", "POST"])
@csrf_exempt
def audio_score(request):
    response = {}
    try:
        if request.method == 'POST':
            # print(request)
            req = request.FILES.get('file')
            file_path = "./mandrain_web/mandrain_model/dataset/" + req.name
            default_storage.save(file_path, req)
            # wav_file_name = file_path
            # wav_file_name = convert_mp3_to_wav( './mandrain_web/mandrain_model/dataset/' + req.name, os.path.dirname(file_path))
            wav_file_name = convert_to_wav('./mandrain_web/mandrain_model/dataset/' + req.name)
            # default_storage.save(wav_file_name,req)
            input_string = request.POST['pinyinSequences'][1:-1]
            # 使用split函数按照逗号分割字符串
            items = input_string.split(',')

            # 创建一个空列表用于存放结果
            char_list = []

            # 遍历分割后的子串，去除首尾双引号后添加到结果列表
            for item in items:
                char = item.strip(' "')
                char_list.append(char)

            # 现在，char_list中已经包含了所需的字符列表
            pinyin_sequences = char_list
            err, score = score_voice(wav_file_name=wav_file_name, std_res=pinyin_sequences)

            # 返回状态信息
            info = {}
            info["err"] = err
            info["score"] = score
            response['msg'] = "Success"
            response["info"] = info
            response['code'] = 200
            os.remove(file_path)
    except Exception as e:
        print(e)
        response['msg'] = '服务器内部错误'
        response['code'] = 1
    return HttpResponse(json.dumps(response), content_type="application/json")


# def convert_mp3_to_wav(mp3_file: str, out_dir: str) -> str:
#     '''
#     将一个mp3文件转换为一个wav文件
#     '''
#     sound = AudioSegment.from_mp3(mp3_file)
#     wav_file = os.path.splitext(os.path.basename(out_dir))[0] + mp3_file + ".wav"
#     sound.export(wav_file, format="wav")
#     return wav_file

def convert_to_wav(filename):
    """
    如果文件不是WAV格式，将其转换为WAV格式。
    """
    # 检查文件扩展名是否为WAV
    if not filename.lower().endswith('.wav'):
        # 尝试使用pydub加载文件
        try:
            sound = AudioSegment.from_file(filename)
        except Exception as e:
            print(e)
            raise ValueError(f"无法加载文件 {filename}，确保它是一个有效的音频文件。") from e

        # 设置采样率为16000Hz
        sound = sound.set_frame_rate(16000)

        # 构建新的WAV文件名
        wav_filename = filename.rsplit('.', 1)[0] + '.wav'

        # 导出音频为WAV格式
        sound.export(wav_filename, format='wav')

        # 更新filename为转换后的WAV文件路径
        filename = wav_filename

    return filename