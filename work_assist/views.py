# 路由能力
from django.shortcuts import render
import work_assist.services as services


def head(request):
    return render(request, "head.html")


def index(request):
    return render(request, "index.html")


def console(request):
    uploaded_excels = services.list_all_excels()
    context = {'uploaded_excels': uploaded_excels}
    return render(request, 'console.html', context)


def case(request):
    return render(request, "case.html")


def lab(request):
    return render(request, "lab.html")

