# https://www.xfyun.cn/doc/spark/Web.html#_1-%E6%8E%A5%E5%8F%A3%E8%AF%B4%E6%98%8E
import _thread as thread
import base64
import datetime
import hashlib
import hmac
import json
from urllib.parse import urlparse
import ssl
from datetime import datetime
from time import mktime
from urllib.parse import urlencode
from wsgiref.handlers import format_date_time
import websocket

answer = ""

# api_key 为 {app_id:'', api_secret:'', api_key:''}
def get_figure_response_and_result(api_key, image_data, system_prompt):
    appid = "c9ff7d11"  # 填写控制台中获取的 APPID 信息
    api_secret = "NGFiM2I5YWI5YWRkMGQ2MDNhOWE2NmU2"  # 填写控制台中获取的 APISecret 信息
    api_key = "c2b5aa50eaec8d12538e0062c5d681e1"  # 填写控制台中获取的 APIKey 信息

    imageunderstanding_url = "wss://spark-api.cn-huabei-1.xf-yun.com/v2.1/image"  # 云端环境的服务地址
    text = [{"role": "user", "content": str(base64.b64encode(image_data), 'utf-8'), "content_type": "image"}]
    question = checklen(generateText("user", system_prompt, text))
    main(appid, api_key, api_secret, imageunderstanding_url, image_data, question)
    return answer


# 生成url
def create_url(api_key, api_secret, imageunderstanding_url):
    host = urlparse(imageunderstanding_url).netloc
    path = urlparse(imageunderstanding_url).path
    # 生成RFC1123格式的时间戳
    now = datetime.now()
    date = format_date_time(mktime(now.timetuple()))
    # 拼接字符串
    signature_origin = "host: " + host + "\n" \
                       + "date: " + date + "\n"\
                       + "GET " + path + " HTTP/1.1"
    # 进行hmac-sha256进行加密
    signature_sha = hmac.new(api_secret.encode('utf-8'), signature_origin.encode('utf-8'),
                             digestmod=hashlib.sha256).digest()
    signature_sha_base64 = base64.b64encode(signature_sha).decode(encoding='utf-8')
    authorization_origin = f'api_key="{api_key}", algorithm="hmac-sha256", ' \
                           f'headers="host date request-line", signature="{signature_sha_base64}"'
    authorization = base64.b64encode(authorization_origin.encode('utf-8')).decode(encoding='utf-8')
    # 将请求的鉴权参数组合为字典
    v = {
        "authorization": authorization,
        "date": date,
        "host": host
    }
    # 拼接鉴权参数，生成url
    url = imageunderstanding_url + '?' + urlencode(v)
    # print(url)
    # 此处打印出建立连接时候的url,参考本demo的时候可取消上方打印的注释，比对相同参数时生成的url与自己代码生成的url是否一致
    return url


# 收到websocket错误的处理
def on_error(ws, error):
    print("### error:", error)


# 收到websocket关闭的处理
def on_close(ws, one, two):
    print(" ")


# 收到websocket连接建立的处理
def on_open(ws):
    thread.start_new_thread(run, (ws,))


def run(ws, *args):
    data = json.dumps(gen_params(appid=ws.appid, question=ws.question))
    ws.send(data)


# 收到websocket消息的处理
def on_message(ws, message):
    data = json.loads(message)
    code = data['header']['code']
    if code != 0:
        print(f'请求错误: {code}, {data}')
        ws.close()
    else:
        choices = data["payload"]["choices"]
        status = choices["status"]
        content = choices["text"][0]["content"]
        # print(content)
        global answer
        answer += content
        if status == 2:
            ws.close()


def gen_params(appid, question):
    """
    通过appid和用户的提问来生成请参数
    """
    data = {
        "header": {
            "app_id": appid
        },
        "parameter": {
            "chat": {
                "domain": "image",
                "temperature": 0.5,
                "top_k": 4,
                "max_tokens": 2028,
                "auditing": "default"
            }
        },
        "payload": {
            "message": {
                "text": question
            }
        }
    }
    return data


def generateText(role, content, text):
    jsoncon = {}
    jsoncon["role"] = role
    jsoncon["content"] = content
    text.append(jsoncon)
    return text


def getlength(text):
    length = 0
    for content in text:
        temp = content["content"]
        leng = len(temp)
        length += leng
    return length


def checklen(text):
    #print("text-content-tokens:", getlength(text[1:]))
    while (getlength(text[1:])> 8000):
        del text[1]
    return text


def main(appid, api_key, api_secret, imageunderstanding_url, imagedata, question):

    websocket.enableTrace(False)
    ws_url = create_url(api_key, api_secret, imageunderstanding_url)
    ws = websocket.WebSocketApp(ws_url,
                                on_message=on_message, on_error=on_error, on_close=on_close, on_open=on_open)
    ws.appid = appid
    ws.imagedata = imagedata
    ws.question = question
    ws.run_forever(sslopt={"cert_reqs": ssl.CERT_NONE})



