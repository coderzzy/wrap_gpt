# 路由能力
from django.shortcuts import render
import os
from work_assist.core.constants import EXCEL_ROOT
import work_assist.models as models


def head(request):
    return render(request, "head.html")


def index(request):
    return render(request, "index.html")


def console(request):
    uploaded_excels = models.Excel.objects.all()
    context = {'uploaded_excels': uploaded_excels}
    return render(request, 'console.html', context)


def case(request):
    return render(request, "case.html")


def lab(request):
    return render(request, "lab.html")

