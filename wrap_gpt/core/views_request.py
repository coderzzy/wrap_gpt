# 请求处理能力
import os
import traceback
import threading
from django.http import HttpResponse, JsonResponse, StreamingHttpResponse
from django.core.files.storage import FileSystemStorage
from django.views.decorators.csrf import csrf_exempt
from wrap_gpt.core.constants import CONTENT_ROOT, EXCEL_ROOT
from wrap_gpt.core.run_gpt import content_stream_response, content_stream_result, excel_process


def is_ajax(request):
    return request.META.get('HTTP_X_REQUESTED_WITH') == 'XMLHttpRequest'


# 上传单文本处理的文件，并保存本地
def upload_content(request):
    if is_ajax(request):
        # 处理 Ajax 请求
        if request.method == 'POST' and request.FILES['file']:
            # parameters
            timesleep_config = int(request.POST.get('timesleep_config'))
            maxtokens_config = int(request.POST.get('maxtokens_config'))
            temperature_config = float(request.POST.get('temperature_config'))
            model_config = request.POST.get('model_config')
            system_prompt = request.POST.get('system_prompt')
            if system_prompt == '':
                return JsonResponse({'status': 'error', 'message': 'prompt不能为空'}, safe=False)
            try:
                # file
                uploaded_file = request.FILES['file']
                fs = FileSystemStorage()
                file_name = uploaded_file.name
                filepath = fs.save(os.path.join(CONTENT_ROOT, file_name), uploaded_file)
                return JsonResponse({'status': 'success', 'data': {'file_name': file_name}},
                                    safe=False)
            except Exception as e:
                traceback.print_exc()
                return JsonResponse({'status': 'error', 'message': str(e)}, safe=False)
    return JsonResponse({'status': 'error', 'message': '内部异常'}, safe=False)


# 流式处理单文本的内容
@csrf_exempt
def stream_content(request):
    data = json.loads(request.body)
    timesleep_config = int(data.get('timesleep_config'))
    maxtokens_config = int(data.get('maxtokens_config'))
    temperature_config = float(data.get('temperature_config'))
    model_config = data.get('model_config')
    system_prompt = data.get('system_prompt')
    file_name = data.get('file_name')
    # process
    os.path.join(CONTENT_ROOT, file_name)
    input_path = os.path.join(CONTENT_ROOT, file_name)
    gpt_type, response = content_stream_response(input_path,
                             timesleep_config, maxtokens_config, temperature_config, model_config,
                             system_prompt)
    response = StreamingHttpResponse(content_stream_result(gpt_type, response),
                                     content_type='application/octet-stream')
    return response


# 上传excel文件，保存本地，并启动线程进行处理
def upload_excel(request):
    if is_ajax(request):
        # 处理 Ajax 请求
        if request.method == 'POST' and request.FILES['file']:
            # parameters
            input_column_name = request.POST.get('input_column_name')
            output_column_name = request.POST.get('output_column_name')
            timesleep_config = int(request.POST.get('timesleep_config'))
            maxtokens_config = int(request.POST.get('maxtokens_config'))
            temperature_config = float(request.POST.get('temperature_config'))
            model_config = request.POST.get('model_config')
            system_prompt = request.POST.get('system_prompt')
            user_prompt = request.POST.get('user_prompt')
            ex_user_prompt = request.POST.get('ex_user_prompt')
            ex_assistant_prompt = request.POST.get('ex_assistant_prompt')
            if input_column_name == '' or output_column_name == '':
                return JsonResponse({'status': 'error', 'message': '列名不能为空'}, safe=False)
            if system_prompt == '' or user_prompt == '':
                return JsonResponse({'status': 'error', 'message': 'prompt不能为空'}, safe=False)
            try:
                # file
                uploaded_file = request.FILES['file']
                fs = FileSystemStorage()
                origin_filename = uploaded_file.name
                filepath = fs.save(os.path.join(EXCEL_ROOT, 'unfinished_'+origin_filename), uploaded_file)
                # process
                input_path = filepath
                output_path = os.path.join(EXCEL_ROOT, f'finished_{origin_filename}')
                thread = threading.Thread(target=excel_process,
                                          args=(input_path, output_path, input_column_name, output_column_name,
                                                timesleep_config, maxtokens_config, temperature_config, model_config,
                                                system_prompt, user_prompt, ex_user_prompt, ex_assistant_prompt,))
                thread.start()
                return JsonResponse({'status': 'success'}, safe=False)
            except Exception as e:
                traceback.print_exc()
                return JsonResponse({'status': 'error', 'message': str(e)}, safe=False)
    return JsonResponse({'status': 'error', 'message': '内部异常'}, safe=False)


# 下载已经处理好的excel
def download_excel(request, file_name):
    file_path = os.path.join(EXCEL_ROOT, file_name)
    if os.path.exists(file_path):
        with open(file_path, 'rb') as excel_file:
            response = HttpResponse(excel_file.read(), content_type='application/ms-excel')
            response['Content-Disposition'] = f'attachment; filename="{file_name}"'
            return response
    else:
        return HttpResponse("File not found", status=404)


# 删除文件列表中的excel
def delete_excel(request):
    file_name = request.POST.get('file_name')
    file_path = os.path.join(EXCEL_ROOT, file_name)
    if os.path.exists(file_path):
        os.remove(file_path)
        return JsonResponse('success', safe=False)
    return JsonResponse('error', safe=False)


from openai import OpenAI
import json
# do_lab，忽略 CSRF 校验
@csrf_exempt
def do_lab(request):
    data = json.loads(request.body)
    user_input = data.get('input')
    client = OpenAI(
        # defaults to os.environ.get("OPENAI_API_KEY")
        api_key=os.environ.get('OPENAI_KEY'),
    )
    completion = client.chat.completions.create(
        model="gpt-3.5-turbo",
        messages=[
            {"role": "user", "content": user_input}
        ],
        stream=True
    )

    def get_streaming_content(completion):
        for chunk in completion:
            content = chunk.choices[0].delta.content
            if not content:
                content = '~'
            yield content

    response = StreamingHttpResponse(get_streaming_content(completion), content_type='application/octet-stream')
    return response