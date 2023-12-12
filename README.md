# GPT封装

## Django等环境安装
```
# pip install -r requirements.txt

pip install pandas
pip install django
pip install django-browser-reload
pip install openai
pip install erniebot
pip install tiktoken
pip install python-docx
pip install PyPDF2

django-admin --version

```

## 程序启动
```python
python manage.py OPENAI_KEY:xxxx,WENXIN_TOKEN:xxxx[,...] runserver 0.0.0.0:8000
```


## 程序管理后台
```python
python manage.py createsuperuser
```


## 层次结构
html/templates/static -> views -> services -> core/models/...

## TODO
1. 层次结构改造，整合出service层，隔离views和models