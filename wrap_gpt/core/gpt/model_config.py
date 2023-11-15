import time
import pandas as pd
from openai import OpenAI
import erniebot

# 批量处理，对外提供接口
def batchProcess(gpt_type, api_key,  
                 input_path, output_path, column_name, output_column_name,
                 timesleep_config, maxtokens_config, temperature_config, model_config,
                 system_prompt, user_prompt, ex_user_prompt, ex_assistant_prompt):
    df = pd.read_excel(input_path)
    # 循环遍历每一行并调用GPT-3.5 API处理
    generated_texts = []
    for index, row in df.iterrows():
        input_text = row[column_name]  # 从指定列获取文本
        generated_text = modelConfig_batch(gpt_type, api_key, 
                                           input_text, maxtokens_config, temperature_config, model_config,
                                           system_prompt, user_prompt, ex_user_prompt, ex_assistant_prompt)
        generated_texts.append(generated_text)
        print("Process "+str(index+1)+": "+generated_text)
        time.sleep(timesleep_config)  # 普通api等待20秒，充值api等待3秒

    df[output_column_name] = generated_texts  # 将生成的文本添加到新列
    df.to_excel(output_path, index=False)

# 单次内容输入，对外提供接口
def modelConfig_content(gpt_type, api_key, 
                        input_text, temperature_config, model_config, system_prompt):
    print("system_prompt："+system_prompt)
    result = ''
    if gpt_type == 'wenxin':
        # 文心一言
        print('wenxin')
        response = erniebot.ChatCompletion.create(
            _config_=dict(
                api_type="aistudio",
                access_token=api_key,
            ),
            model=model_config,
            messages=[
                {"role": "user", "content": f"{system_prompt}"},
                {"role": "assistant", "content": "好的"},
                {"role": "user", "content": f"{repr(input_text)}"}
            ],
        )
        result = response['result']
    else:
        # openai
        # 默认是openai
        print('openai')
        client = OpenAI(
            # defaults to os.environ.get("OPENAI_API_KEY")
            api_key=api_key,
        )
        response = client.ChatCompletion.create(
            model=model_config,
            messages=[
                {"role": "system", "content": f"{system_prompt}"},
                {"role": "user", "content": f"{input_text}"}
            ],
            temperature=temperature_config #between 0 and 2， default=1.0 【数值越高，创新+多样性越强，但可能不太保守】
        )
        result = response['choices'][0]['message']['content']
    print("result："+result)

    return result

# 批处理excel2excel，内部调用
def modelConfig_batch(gpt_type, api_key,
                   input_text, maxtokens_config, temperature_config,model_config,
                   system_prompt, user_prompt, ex_user_prompt, ex_assistant_prompt):
    result=''
    if gpt_type == 'wenxin':
        # 文心一言
        print('wenxin')
        messages = [{"role": "user", "content": system_prompt}]
        messages.append({"role": "assistant", "content": "好的"})
        if ex_user_prompt != "" and ex_assistant_prompt != "":
            messages.append({"role": "user", "content": ex_user_prompt})
            messages.append({"role": "assistant", "content": ex_assistant_prompt})
        messages.append({"role": "user", "content": f"{user_prompt}：{input_text}"})
        response = erniebot.ChatCompletion.create(
            _config_=dict(
                api_type="aistudio",
                access_token=api_key,
            ),
            model=model_config,
            messages=messages,
        )
        result = response['result']
    else:
        # openai
        # 默认是openai
        print('openai')
        client = OpenAI(
            # defaults to os.environ.get("OPENAI_API_KEY")
            api_key=api_key,
        )
        messages = [{"role": "system", "content": system_prompt}]
        if ex_user_prompt != "" and ex_assistant_prompt != "":
            messages.append({"role": "user", "content": ex_user_prompt})
            messages.append({"role": "assistant", "content": ex_assistant_prompt})
        messages.append({"role": "user", "content": f"{user_prompt}：{input_text}"})
        response = client.ChatCompletion.create(
            model=model_config,
            messages = messages,
            max_tokens=maxtokens_config,
            temperature=temperature_config #between 0 and 2， default=1.0 【数值越高，创新+多样性越强，但可能不太保守】
        )
        result = response['choices'][0]['message']['content']
    return result