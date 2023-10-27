from django.shortcuts import render
from django.http import HttpResponse
from django.core.files.storage import FileSystemStorage
import os

EXCEL_ROOT = 'temp_files/excel'

def upload_excel(request):
    filename = ""
    if request.method == 'POST' and request.FILES['file']:
        uploaded_file = request.FILES['file']
        fs = FileSystemStorage()
        filename = fs.save(EXCEL_ROOT+'/'+uploaded_file.name, uploaded_file)

    uploaded_files = os.listdir(os.path.join(EXCEL_ROOT))
    context = {'filename':filename, 'uploaded_files': uploaded_files}
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

