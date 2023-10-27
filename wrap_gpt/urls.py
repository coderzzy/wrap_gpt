from django.contrib import admin
from django.urls import path, include
from wrap_gpt.core.views import upload_excel, download_excel

urlpatterns = [
    path('admin/', admin.site.urls),
    path("__reload__/", include("django_browser_reload.urls")),
    path('', upload_excel, name='upload_excel'),
    path('download/<str:file_name>/', download_excel, name='download_excel'),
]