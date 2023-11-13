from django.shortcuts import render
from django.http import HttpResponse, JsonResponse
from django.core.files.storage import FileSystemStorage
import os
import threading
from wrap_gpt.core.constants import CONTENT_ROOT, EXCEL_ROOT
from wrap_gpt.core.gpt.run_gpt import content_process, excel_process

def is_ajax(request):
    return request.META.get('HTTP_X_REQUESTED_WITH') == 'XMLHttpRequest'

### 页面渲染
def head(request):
    return render(request, "head.html")

def index(request):
    return render(request, "index.html")

def console(request):
    uploaded_excels = [(file_name, file_name.split('_')[1], file_name.split('_')[0]) 
                      for file_name in os.listdir(os.path.join(EXCEL_ROOT))]
    context = {'uploaded_excels': uploaded_excels}
    return render(request, 'console.html', context)

def case(request):
    return render(request, "case.html")

### 请求
def upload_content(request):
    if is_ajax(request):
        # 处理 Ajax 请求
        if request.method == 'POST' and request.FILES['file']:
            # parameters
            timesleep_config = int(request.POST.get('timesleep_config'))
            maxtokens_config = int(request.POST.get('maxtokens_config'))
            temperature_config = float(request.POST.get('temperature_config'))
            model_config = request.POST.get('model_config')
            system_prompt = str(request.POST.get('system_prompt'))
            # file
            uploaded_file = request.FILES['file']
            fs = FileSystemStorage()
            file_name = uploaded_file.name
            filepath = fs.save(os.path.join(CONTENT_ROOT, file_name), uploaded_file)
            # process
            input_path = filepath
            result = content_process(input_path, 
                    timesleep_config, maxtokens_config, temperature_config, model_config, 
                    system_prompt)
            return JsonResponse({'file_name': file_name, 'result': result}, safe=False)
    return JsonResponse('error', safe=False)


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
            return JsonResponse(filepath, safe=False)
    return JsonResponse('error', safe=False)


def download_excel(request, file_name):
    file_path = os.path.join(EXCEL_ROOT, file_name)
    if os.path.exists(file_path):
        with open(file_path, 'rb') as excel_file:
            response = HttpResponse(excel_file.read(), content_type='application/ms-excel')
            response['Content-Disposition'] = f'attachment; filename="{file_name}"'
            return response
    else:
        return HttpResponse("File not found", status=404)


# json 
def delete_excel(request):
    file_name = request.POST.get('file_name')
    file_path = os.path.join(EXCEL_ROOT, file_name)
    if os.path.exists(file_path):
        os.remove(file_path)
        return JsonResponse('success', safe=False)
    return JsonResponse('error', safe=False)

