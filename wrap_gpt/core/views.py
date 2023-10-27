from django.shortcuts import render
from django.http import HttpResponse
from django.core.files.storage import FileSystemStorage
import os
import threading
from wrap_gpt.core.constants import EXCEL_ROOT
from wrap_gpt.core.gpt.excel_process import excel_process

def upload_excel(request):
    filepath = ""
    if request.method == 'POST' and request.FILES['file']:
        uploaded_file = request.FILES['file']
        fs = FileSystemStorage()
        origin_filename = uploaded_file.name
        filepath = fs.save(os.path.join(EXCEL_ROOT, 'unfinished_'+origin_filename), uploaded_file)
        thread = threading.Thread(target=excel_process)
        thread.start()
        print('1111')

    uploaded_files = os.listdir(os.path.join(EXCEL_ROOT))
    context = {'filepath':filepath, 'uploaded_files': uploaded_files}
    return render(request, 'upload.html', context)

def download_excel(request, file_name):
    file_path = os.path.join(EXCEL_ROOT, file_name)
    if os.path.exists(file_path):
        with open(file_path, 'rb') as excel_file:
            response = HttpResponse(excel_file.read(), content_type='application/ms-excel')
            response['Content-Disposition'] = f'attachment; filename="{file_name}"'
            return response
    else:
        return HttpResponse("File not found", status=404)

