from kdxf import SparkApi

text = []

def getText(role,content):
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
    while getlength(text) > 8000:
        del text[0]
    return text

def content_dress(file_content, input_text):
    appid = ""  # 填写控制台中获取的 APPID 信息
    api_secret = ""  # 填写控制台中获取的 APISecret 信息
    api_key = ""  # 填写控制台中获取的 APIKey 信息

    domain = "generalv3"  # v3.0版本
    # domain = "generalv2"    # v2.0版本
    Spark_url = "ws://spark-api.xf-yun.com/v3.1/chat"  # v3.0环境的地址
    # Spark_url = "ws://spark-api.xf-yun.com/v2.1/chat"  # v2.0环境的地址

    #Input = input("\n" +"我:")
    Input = input_text+ file_content #输入＋输出字数控制在8129内
    question = checklen(getText("user",Input))
    SparkApi.answer = ""
    print("星火:",end = "")
    SparkApi.main(appid, api_key, api_secret, Spark_url, domain, question)
    #getText("assistant",SparkApi.answer)
    # print(str(text))

