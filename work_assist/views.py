# 路由能力
from django.shortcuts import render
import os
from work_assist.core.constants import EXCEL_ROOT


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


def lab(request):
    return render(request, "lab.html")

