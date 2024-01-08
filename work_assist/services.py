import work_assist.models as models


def list_users_with_name_and_pwd(username, password):
    return list(models.User.objects.filter(name=username, password=password).values())


def list_all_excels():
    return models.Excel.objects.all()


def delete_excel_by_file_name(file_name):
    models.Excel.objects.filter(name=file_name).delete()
