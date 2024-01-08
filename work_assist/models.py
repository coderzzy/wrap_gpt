# db <-> model
# https://www.jb51.net/article/254422.htm
# python3 manage.py makemigrations
# python3 manage.py migrate
from django.db import models


class User(models.Model):
    def __str__(self):
        return self.name

    name = models.CharField(max_length=255)


class Excel(models.Model):
    def __str__(self):
        return self.name

    name = models.CharField(max_length=255)
    file_path = models.CharField(max_length=255)
    processed_line = models.IntegerField()
    total_line = models.IntegerField()
    status = models.CharField(max_length=255)
    status_content = models.CharField(max_length=255)


