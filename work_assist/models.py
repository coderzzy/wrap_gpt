# db <-> model
# https://www.jb51.net/article/254422.htm
# python3 manage.py makemigrations
# python3 manage.py migrate
from django.db import models


class User(models.Model):
    def __str__(self):
        return self.name

    name = models.CharField(max_length=255, unique=True)
    password = models.CharField(max_length=255, default='')
    openai_3_5_key = models.CharField(max_length=255, blank=True, default='')
    openai_4_key = models.CharField(max_length=255, blank=True, default='')
    wenxin_token = models.CharField(max_length=255, blank=True, default='')
    kdxf_appid = models.CharField(max_length=255, blank=True, default='')
    kdxf_secret = models.CharField(max_length=255, blank=True, default='')
    kdxf_key = models.CharField(max_length=255, blank=True, default='')


class Excel(models.Model):
    def __str__(self):
        return self.name

    name = models.CharField(max_length=255)
    file_path = models.CharField(max_length=255)
    processed_line = models.IntegerField()
    total_line = models.IntegerField()
    status = models.CharField(max_length=255)
    status_content = models.CharField(max_length=255)


