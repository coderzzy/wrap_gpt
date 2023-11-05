from django.contrib import admin
from django.urls import path, include
from wrap_gpt.core.views import index, console, upload_excel, download_excel, delete_excel

urlpatterns = [
    path('admin/', admin.site.urls),
    path("__reload__/", include("django_browser_reload.urls")),
    path('', index, name='index'),
    path('console', console, name='console'),
    path('upload_excel', upload_excel, name='upload_excel'),
    path('download/<str:file_name>/', download_excel, name='download_excel'),
    path('delete_excel', delete_excel, name='delete_excel'),
]