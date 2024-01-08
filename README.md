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
pip install pyjwt

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
- models注册，后台进行数据库管理

## 层次结构
html/templates/static -> views -> run/services -> core/models/...

## TODO
1. 层次结构改造，整合出service层，隔离views和models

## 相关功能及原理
1 登录注册: 基于JWT-Token理念，
- 服务端不存储token，仅进行签名校验
- 前端cookie存储token，实现过期能力；并通过token解析，获取用户信息

2 流式返回
- StreamingHttpResponse(function, content_type='application/octet-stream')
