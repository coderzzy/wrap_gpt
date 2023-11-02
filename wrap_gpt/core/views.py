from django.shortcuts import render
from django.http import HttpResponse, JsonResponse
from django.core.files.storage import FileSystemStorage
import os
import threading
from wrap_gpt.core.constants import EXCEL_ROOT
from wrap_gpt.core.gpt.excel_process import excel_process

def is_ajax(request):
    return request.META.get('HTTP_X_REQUESTED_WITH') == 'XMLHttpRequest'

def head(request):
    return render(request, "head.html")

def index(request):
    return render(request, "index.html")

def upload_excel(request):
    if is_ajax(request):
        # 处理 Ajax 请求
        if request.method == 'POST' and request.FILES['file']:
            uploaded_file = request.FILES['file']
            fs = FileSystemStorage()
            origin_filename = uploaded_file.name
            filepath = fs.save(os.path.join(EXCEL_ROOT, 'unfinished_'+origin_filename), uploaded_file)
            thread = threading.Thread(target=excel_process, args=(filepath, origin_filename, ))
            thread.start()
            return JsonResponse(filepath, safe=False)
    # 其他请求，渲染页面
    uploaded_files = [(file_name.split('_')[1], file_name.split('_')[0]) 
                      for file_name in os.listdir(os.path.join(EXCEL_ROOT))]
    context = {'uploaded_files': uploaded_files}
    return render(request, 'upload.html', context)

def download_excel(request, file_name):
    file_path = os.path.join(EXCEL_ROOT, 'finished_'+file_name)
    if os.path.exists(file_path):
        with open(file_path, 'rb') as excel_file:
            response = HttpResponse(excel_file.read(), content_type='application/ms-excel')
            response['Content-Disposition'] = f'attachment; filename="{file_name}"'
            return response
    else:
        return HttpResponse("File not found", status=404)

