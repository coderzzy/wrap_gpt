# db <-> model
# https://www.jb51.net/article/254422.htm
# python3 manage.py makemigrations
# python3 manage.py migrate
from django.db import models


class User(models.Model):
    name = models.CharField(max_length=255)


