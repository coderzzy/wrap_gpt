import time
import os
import traceback
import pandas as pd
import work_assist.core.gpt.model_config as model
from work_assist.core.gpt.input_process import txt_read, excel_read, word_read, pdf_read
import work_assist.models as models


def chat_stream_response(input_text, model_config):
    print('start')
    gpt_type, api_key = __get_gpt_type(model_config)
    print(gpt_type, api_key)
    response = model.modelConfig_content_stream_response(gpt_type, api_key,
                                                         input_text, model_config, input_text)
    print('end')
    return gpt_type, response


def chat_stream_result(gpt_type, response):
    print('chat_stream_result')
    return model.modelConfig_content_stream_result(gpt_type, response)


# 单文本处理，选择流式方案
def content_stream_response(input_path,
                    timesleep_config, temperature_config, model_config,
                    system_prompt):
    print('start')
    # 内容读取
    file_type = input_path.split('.')[-1]
    input_text = ''
    if file_type == "txt" or file_type == "py":
        input_text = txt_read(input_path)
    elif file_type == "xlsx":
        input_text = excel_read(input_path)
    elif file_type == "docx":
        input_text = word_read(input_path)
    elif file_type == "pdf":
        input_text = pdf_read(input_path)
    # gpt
    gpt_type, api_key = __get_gpt_type(model_config)
    response = model.modelConfig_content_stream_response(gpt_type, api_key,
                                                         input_text, model_config, system_prompt,
                                                         temperature_config)
    os.remove(input_path)
    print('end')
    return gpt_type, response


def content_stream_result(gpt_type, response):
    print('content_stream_result')
    return model.modelConfig_content_stream_result(gpt_type, response)


# excel批处理，非流式方案
def excel_process(file_name, file_path,
                  column_name, output_column_name,
                     timesleep_config, temperature_config, model_config,
                     system_prompt, user_prompt, ex_user_prompt, ex_assistant_prompt):
    print('start')
    # gpt
    gpt_type, api_key = __get_gpt_type(model_config)
    try:
        df = pd.read_excel(file_path)
        # 记录初始数据
        models.Excel.objects.create(name=file_name, file_path=file_path,
                                    processed_line=0, total_line=df.shape[0],
                                    status='processing', status_content='')
        # 循环遍历每一行并调用GPT-3.5 API处理
        generated_texts = []
        for index, row in df.iterrows():
            input_text = row[column_name]  # 从指定列获取文本
            generated_text = model.modelConfig_batch(gpt_type, api_key,
                                                 input_text, temperature_config, model_config,
                                                 system_prompt, user_prompt, ex_user_prompt, ex_assistant_prompt)
            generated_texts.append(generated_text)
            print(generated_text)
            print("Process "+str(index+1)+": "+generated_text)
            # 更新数据
            models.Excel.objects.filter(name=file_name).update(processed_line=index+1)
            time.sleep(timesleep_config)
        df[output_column_name] = generated_texts  # 将生成的文本添加到新列
        df.to_excel(file_path, index=False)
        # 更新数据
        models.Excel.objects.filter(name=file_name).update(status='success')
    except Exception as e:
        traceback.print_exc()
        # 记录异常
        models.Excel.objects.filter(name=file_name).update(status='error', status_content=str(e))
    print('end')


# 图片处理，流式方案
def figure_stream_response(input_path, model_config, system_prompt):
    print('start')
    image_data = None
    with open(input_path, "rb") as image_file:
        image_data = image_file.read()
    gpt_type, api_key = __get_gpt_type(model_config)
    os.remove(input_path)
    response = model.modelConfig_figure_stream_response(gpt_type, api_key,
                                                        image_data, model_config, system_prompt)
    print('end')
    return gpt_type, response


def figure_stream_result(gpt_type, response):
    print('figure_stream_result')
    return model.modelConfig_figure_stream_result(gpt_type, response)


# return: gpt_type, api_key
def __get_gpt_type(model_config):
    if "ernie" in model_config:
        return "wenxin", os.environ.get('WENXIN_TOKEN')
    if "kdxf" in model_config:
        return "kdxf", {"app_id": os.environ.get('KDXF_APPID'),
                        "secret": os.environ.get('KDXF_SECRET'),
                        "key": os.environ.get('KDXF_KEY')}
    # 默认是openai
    if "gpt-4" in model_config:
        return "openai", os.environ.get('OPENAI_4_KEY')
    return "openai", os.environ.get('OPENAI_3.5_KEY')
