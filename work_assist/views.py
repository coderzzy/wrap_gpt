# 路由能力
from django.shortcuts import render
from django.shortcuts import redirect
from django.contrib import messages
import work_assist.services as services


def head(request):
    return render(request, "head.html")


def index(request):
    return render(request, "index.html")


def console(request):
    token = request.COOKIES.get('user-token')
    if not token:
        # 尚未登录
        messages.info(request, '使用工作台功能，需要先登录！')
        return redirect('index')
    uploaded_excels = services.list_all_excels()
    context = {'uploaded_excels': uploaded_excels}
    return render(request, 'console.html', context)


def case(request):
    return render(request, "case.html")


def lab(request):
    return render(request, "lab.html")

