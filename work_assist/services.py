import work_assist.models as models


def list_users_with_name_and_pwd(username, password):
    return list(models.User.objects.filter(name=username, password=password).values())


def list_all_excels():
    return models.Excel.objects.all()


def delete_excel_by_file_name(file_name):
    models.Excel.objects.filter(name=file_name).delete()


def create_excel(file_name, file_path, processed_line, total_line, status, status_content):
    models.Excel.objects.create(name=file_name, file_path=file_path,
                                processed_line=processed_line, total_line=total_line,
                                status=status, status_content=status_content)


def update_excel_processed_line_by_file_name(file_name, processed_line):
    models.Excel.objects.filter(name=file_name).update(processed_line=processed_line)


def update_excel_status_and_content_by_file_name(file_name, status, status_content):
    models.Excel.objects.filter(name=file_name).update(status=status, status_content=status_content)
