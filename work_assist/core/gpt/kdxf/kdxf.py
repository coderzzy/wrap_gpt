# https://www.xfyun.cn/doc/spark/Web.html#_1-%E6%8E%A5%E5%8F%A3%E8%AF%B4%E6%98%8E
import base64
import ssl
import websocket
from work_assist.core.gpt.kdxf import kdxf_figure_process, kdxf_content_process


# 暂时不支持流式，以非流式的方式使用
def get_response(api_key, input_text,
                 system_prompt='', user_prompt='', ex_user_prompt='', ex_assistant_prompt='',
                 stream=False):
    appid = api_key['app_id']
    api_secret = api_key['secret']
    api_key = api_key['key']
    # 准备参数
    kdxf_content_process.answer = ""
    domain = "generalv3"
    spark_url = "wss://spark-api.xf-yun.com/v3.1/chat"
    messages=[
        {"role": "user", "content": f"{system_prompt}"},
        {"role": "assistant", "content": "好的"}
    ]
    if ex_user_prompt != "" and ex_assistant_prompt != "":
        messages.append({"role": "user", "content": ex_user_prompt})
        messages.append({"role": "assistant", "content": ex_assistant_prompt})
    if user_prompt != "":
        messages.append({"role": "user", "content": f"{user_prompt}：{input_text}"})
    else:
        messages.append({"role": "user", "content": input_text})
    question = kdxf_content_process.checklen(messages)
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
    # 等待处理完成，并返回结果
    return kdxf_content_process.answer


def get_result(response, stream=False):
    if 'header' in response:
        return response['header']['message']
    return response


# api_key 为 {app_id:'', api_secret:'', api_key:''}
def get_figure_response(api_key, image_data, system_prompt, stream=False):
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
    # 等待处理完成，并返回结果
    return kdxf_figure_process.answer
