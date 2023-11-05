import openai
import pandas as pd
import time
from To_zzy.model_config import modelConfig_ex
from To_zzy.model_config import modelConfig_nex

# batch process
def batchProcess(openai, input_path, output_path, column_name, output_column_name,
                 timesleep_config, maxtokens_config, temperature_config, model_config,
                 system_prompt, user_prompt, ex_user_prompt, ex_assistant_prompt):
    df = pd.read_excel(input_path)
    # 循环遍历每一行并调用GPT-3.5 API处理
    generated_texts = []

    for index, row in df.iterrows():
        input_text = row[column_name]  # 从指定列获取文本
        # 批处理excel2excel（包括示例）
        if ex_user_prompt != "":
            generated_text = modelConfig_ex(openai, input_text, maxtokens_config, temperature_config, model_config,
                 system_prompt, user_prompt, ex_user_prompt, ex_assistant_prompt)
        # 批处理excel2excel（无示例）
        else:
            generated_text = modelConfig_nex(openai, input_text, maxtokens_config, temperature_config,model_config,
                     system_prompt, user_prompt)
        generated_texts.append(generated_text)
        print("Process "+str(index+1)+": "+generated_text)
        time.sleep(timesleep_config)  # 普通api等待20秒，充值api等待3秒

    df[output_column_name] = generated_texts  # 将生成的文本添加到新列
    df.to_excel(output_path, index=False)
