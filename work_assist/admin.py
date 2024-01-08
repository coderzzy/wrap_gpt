from django.contrib import admin
import work_assist.models as models


# Register your models here.
class ExcelManager(admin.ModelAdmin):
    list_display = ['id', 'name', 'file_path']


admin.site.register(models.User)
admin.site.register(models.Excel, ExcelManager)
