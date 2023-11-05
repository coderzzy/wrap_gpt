import openai
from .batch_process import batchProcess


def excel_process(input_path, output_path, column_name, output_column_name,
                     timesleep_config, maxtokens_config, temperature_config, model_config,
                     system_prompt, user_prompt, ex_user_prompt, ex_assistant_prompt):
    openai.api_key = ''
    batchProcess(openai, input_path, output_path, column_name, output_column_name,
                     timesleep_config, maxtokens_config, temperature_config, model_config,
                     system_prompt, user_prompt, ex_user_prompt, ex_assistant_prompt)

