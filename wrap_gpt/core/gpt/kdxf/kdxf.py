# https://www.xfyun.cn/doc/spark/Web.html#_1-%E6%8E%A5%E5%8F%A3%E8%AF%B4%E6%98%8E
import base64
import ssl
import websocket
from wrap_gpt.core.gpt.kdxf import kdxf_figure_process, kdxf_content_process


# TODO: 流式处理，以及socket报错，'socket' object has no attribute 'pending'
def get_response_and_result(api_key, input_text, system_prompt):
    appid = api_key['app_id']
    api_secret = api_key['secret']
    api_key = api_key['key']
    # 准备参数
    kdxf_content_process.answer = ""
    domain = "generalv3"
    spark_url = "ws://spark-api.xf-yun.com/v3.1/chat"
    question = kdxf_content_process\
        .checklen(kdxf_content_process.generateText("user", f'{system_prompt}:{input_text}'))
    # websocket建立
    websocket.enableTrace(False)
    ws_url = kdxf_content_process.create_url(api_key, api_secret, spark_url)
    ws = websocket.WebSocketApp(ws_url,
                                on_message=kdxf_content_process.on_message,
                                on_error=kdxf_content_process.on_error,
                                on_close=kdxf_content_process.on_close,
                                on_open=kdxf_content_process.on_open)
    ws.appid = appid
    ws.question = question
    ws.domain = domain
    ws.run_forever(sslopt={"cert_reqs": ssl.CERT_NONE})
    return kdxf_content_process.answer


# api_key 为 {app_id:'', api_secret:'', api_key:''}
def get_figure_response_and_result(api_key, image_data, system_prompt):
    appid = api_key['app_id']
    api_secret = api_key['secret']
    api_key = api_key['key']
    # 准备参数
    kdxf_figure_process.answer = ""
    imageunderstanding_url = "wss://spark-api.cn-huabei-1.xf-yun.com/v2.1/image"  # 云端环境的服务地址
    text = [{"role": "user", "content": str(base64.b64encode(image_data), 'utf-8'), "content_type": "image"}]
    question = kdxf_figure_process.checklen(kdxf_figure_process.generateText("user", system_prompt, text))
    # websocket建立
    websocket.enableTrace(False)
    ws_url = kdxf_figure_process.create_url(api_key, api_secret, imageunderstanding_url)
    ws = websocket.WebSocketApp(ws_url,
                                on_message=kdxf_figure_process.on_message,
                                on_error=kdxf_figure_process.on_error,
                                on_close=kdxf_figure_process.on_close,
                                on_open=kdxf_figure_process.on_open)
    ws.appid = appid
    ws.imagedata = image_data
    ws.question = question
    ws.run_forever(sslopt={"cert_reqs": ssl.CERT_NONE})
    # 返回结果
    return kdxf_figure_process.answer
