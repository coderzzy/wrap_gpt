import os
from .model_config import modelConfig_content, batchProcess
from .input_process import txt_read, excel_read, word_read, pdf_read

def content_process(input_path, 
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
    gpt_type = os.environ.get('GPT_TYPE')
    api_key = ''
    if gpt_type == 'wenxin':
        # wenxin
        api_key = os.environ.get('WENXIN_TOKEN')
    else:
        # openai
        # 默认是openai
        api_key = os.environ.get('OPENAI_KEY')
        
    result = modelConfig_content(gpt_type, api_key, 
                                 input_text, temperature_config, model_config, system_prompt)
    os.remove(input_path)
    print('end')
    return result


def excel_process(input_path, output_path, column_name, output_column_name,
                     timesleep_config, maxtokens_config, temperature_config, model_config,
                     system_prompt, user_prompt, ex_user_prompt, ex_assistant_prompt):
    print('start')
    # gpt
    gpt_type = os.environ.get('GPT_TYPE')
    api_key = ''
    if gpt_type == 'wenxin':
        # wenxin
        api_key = os.environ.get('WENXIN_TOKEN')
    else:
        # openai
        # 默认是openai
        api_key = os.environ.get('OPENAI_KEY')

    batchProcess(gpt_type, api_key, 
                    input_path, output_path, column_name, output_column_name,
                    timesleep_config, maxtokens_config, temperature_config, model_config,
                    system_prompt, user_prompt, ex_user_prompt, ex_assistant_prompt)
    os.remove(input_path)
    print('end')
