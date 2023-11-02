import openai
import pandas as pd
import time
import os
from wrap_gpt.core.constants import EXCEL_ROOT

def gptForInstruct(input_text, model_tpye):
    # 调用GPT-3.5 API来生成文本
    response = openai.Completion.create(
        engine=model_tpye,
        # engine="text-davinci-003",
        # engine="gpt-3.5-turbo-instruct",
        prompt=f"提取商品名称中的4个关键词，并根据关键词扩展商品5个其他描述词：{input_text}，只输出这10个词，并用；连接成一行",
        max_tokens=300  # 适当设置生成文本的长度
    )
    generated_text = response.choices[0].text
    # 打印
    #print("处理后的文本:", generated_text)
    return generated_text


def gptForContent(input_text):
    response = openai.ChatCompletion.create(
        model="gpt-3.5-turbo",
        messages=[
            {"role": "system",
             "content": "结果输出不超过10个词，且不出现'搜索词'和'关键词'字样，并将所有词都用；连接成一行"},
            {"role": "user",
             "content": "请帮我提取商品中4个关键词，并扩展5个极有可能能够搜索到该商品的搜索词：东鹏0糖能量饮料(6罐装) 335ml*6"},
            {"role": "assistant", "content": "会议；商用；健身；运动；补充能量；东鹏；能量；饮料；罐装"},
            {"role": "user",
             "content": f"请帮我提取商品中4个关键词，并扩展5个极有可能能够搜索到该商品的搜索词：{input_text}"}
        ]
    )
    result = response['choices'][0]['message']['content']
    #print(result)
    return result


def excel_process(file_path, origin_filename):
    # 设置你的OpenAI API密钥
    openai.api_key = ''

    # 读取Excel文件
    df = pd.read_excel(file_path)

    # 指定要处理的列
    column_name = '商品销售名称'
    output_column_name = 'GPT处理'

    # 循环遍历每一行并调用GPT-3.5 API处理
    generated_texts = []
    processed_count = 0
    new_excel_filename = f'finished_{origin_filename}'
    new_excel_filepath = os.path.join(EXCEL_ROOT, new_excel_filename)

    print('start')
    for index, row in df.iterrows():
        input_text = row[column_name]  # 从指定列获取文本
        generated_text = gptForContent(input_text)
        generated_texts.append(generated_text)
        processed_count += 1  # 增加已处理的行数

        print(f"Processed {processed_count}, Product name is {input_text} :")
        print(generated_text)
        time.sleep(3)  # 等待3秒
    df[output_column_name] = generated_texts  # 将生成的文本添加到新列
    df.to_excel(new_excel_filepath, index=False)
    os.remove(file_path)
    print('finished')


