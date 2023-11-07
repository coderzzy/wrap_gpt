import openai
import os
from .batch_process import batchProcess
from .model_config import modelConfig_content
from .input_process import file_read, excel_read

def content_process(input_path, 
                    timesleep_config, maxtokens_config, temperature_config, model_config, 
                    system_prompt):
    print('start')
    openai.api_key = os.environ.get('OPENAI_KEY')
    file_type = input_path.split('.')[-1]
    input_text = ''
    if file_type == "txt":
        input_text = file_read(input_path)
    elif file_type == "xlsx":
        input_text = excel_read(input_path)
    result = modelConfig_content(openai, input_text, temperature_config, model_config, system_prompt)
    os.remove(input_path)
    print('end')
    return result


def excel_process(input_path, output_path, column_name, output_column_name,
                     timesleep_config, maxtokens_config, temperature_config, model_config,
                     system_prompt, user_prompt, ex_user_prompt, ex_assistant_prompt):
    print('start')
    openai.api_key = os.environ.get('OPENAI_KEY')
    batchProcess(openai, input_path, output_path, column_name, output_column_name,
                     timesleep_config, maxtokens_config, temperature_config, model_config,
                     system_prompt, user_prompt, ex_user_prompt, ex_assistant_prompt)
    os.remove(input_path)
    print('end')
