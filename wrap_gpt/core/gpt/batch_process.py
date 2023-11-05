import pandas as pd
import time
import os
from .model_config import modelConfig_batch

# batch process
def batchProcess(openai, input_path, output_path, column_name, output_column_name,
                 timesleep_config, maxtokens_config, temperature_config, model_config,
                 system_prompt, user_prompt, ex_user_prompt, ex_assistant_prompt):
    df = pd.read_excel(input_path)
    # 循环遍历每一行并调用GPT-3.5 API处理
    generated_texts = []
    print('start')
    for index, row in df.iterrows():
        input_text = row[column_name]  # 从指定列获取文本
        generated_text = modelConfig_batch(openai, input_text, maxtokens_config, temperature_config, model_config,
                system_prompt, user_prompt, ex_user_prompt, ex_assistant_prompt)
        generated_texts.append(generated_text)
        print("Process "+str(index+1)+": "+generated_text)
        time.sleep(timesleep_config)  # 普通api等待20秒，充值api等待3秒

    df[output_column_name] = generated_texts  # 将生成的文本添加到新列
    df.to_excel(output_path, index=False)
    os.remove(input_path)
    print('end')
