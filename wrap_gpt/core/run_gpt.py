import os
import wrap_gpt.core.gpt.model_config as model
from wrap_gpt.core.gpt.input_process import txt_read, excel_read, word_read, pdf_read


# 单文本处理，选择流式方案
def content_stream_response(input_path,
                    timesleep_config, maxtokens_config, temperature_config, model_config, 
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
                                 input_text, maxtokens_config, temperature_config, model_config, system_prompt)
    os.remove(input_path)
    print('end')
    return gpt_type, response


def content_stream_result(gpt_type, response):
    print('stream_result')
    return model.modelConfig_content_stream_result(gpt_type, response)


# excel批处理，非流式方案
def excel_process(input_path, output_path, column_name, output_column_name,
                     timesleep_config, maxtokens_config, temperature_config, model_config,
                     system_prompt, user_prompt, ex_user_prompt, ex_assistant_prompt):
    print('start')
    # gpt
    gpt_type, api_key = __get_gpt_type(model_config)
    model.batchProcess(gpt_type, api_key,
                    input_path, output_path, column_name, output_column_name,
                    timesleep_config, maxtokens_config, temperature_config, model_config,
                    system_prompt, user_prompt, ex_user_prompt, ex_assistant_prompt)
    os.remove(input_path)
    print('end')


# 图片处理，非流式方案
def figure_process(input_path, maxtokens_config, model_config, system_prompt):
    image_data = None
    with open(input_path, "rb") as image_file:
        image_data = image_file.read()
    gpt_type, api_key = __get_gpt_type(model_config)
    os.remove(input_path)
    return model.modelConfig_figure(gpt_type, api_key,
                       image_data, model_config, maxtokens_config, system_prompt)


# return: gpt_type, api_key
def __get_gpt_type(model_config):
    if "ernie" in model_config:
        return "wenxin", os.environ.get('WENXIN_TOKEN')
    if "kdxf" in model_config:
        return "kdxf", {"app_id": os.environ.get('KDXF_APPID'),
                        "secret": os.environ.get('KDXF_SECRET'),
                        "key": os.environ.get('KDXF_KEY')}
    # 默认是openai
    return "openai", os.environ.get('OPENAI_KEY')
