from .mandrain_model.use_model import score_voice
import json
import os
import re
import time
import uuid
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
            req = request.FILES.get('file')
            # 打开特定的文件进行二进制的写操作
            # destination = open(
            #     os.path.join("mandrain_model/dataset/", req.name), 'wb')
            # for chunk in req.chunks():  # 分块写入文件
            #     destination.write(chunk)
            # destination.close()
            file_path = "./mandrain_web/mandrain_model/dataset/"+req.name
            default_storage.save(file_path,req)
            wav_file_name = file_path
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
            err, score = score_voice(wav_file_name= wav_file_name, std_res=pinyin_sequences)
            
            # 返回状态信息
            info = {}
            info["err"] = err
            info["score"] = score
            response['msg'] = "Success"
            response["info"] = info
            response['code'] = 200
    except Exception as e:
        response['msg'] = '服务器内部错误'
        response['code'] = 1
    return HttpResponse(json.dumps(response), content_type="application/json")