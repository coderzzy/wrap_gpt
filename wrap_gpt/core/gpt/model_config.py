import time
import pandas as pd
import wrap_gpt.core.gpt.wenxin.wenxin as wenxin
import wrap_gpt.core.gpt.openai.openai as openai


# 对外: 批量处理
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
        time.sleep(timesleep_config)
    df[output_column_name] = generated_texts  # 将生成的文本添加到新列
    df.to_excel(output_path, index=False)


# 对外: 单次内容输入
def modelConfig_content(gpt_type, api_key, 
                        input_text, temperature_config, model_config, system_prompt):
    print("system_prompt："+system_prompt)
    if gpt_type == 'wenxin':
        # 文心一言
        print('wenxin')
        response = wenxin.get_response(api_key, input_text, model_config, system_prompt)
        result = wenxin.get_result(response)
        print("result："+result)
        return result
    # if gpt_type == '':

    # openai，默认是openai
    print('openai')
    response = openai.get_response(api_key,
                                   input_text, model_config, temperature_config,
                                   system_prompt=system_prompt)
    result = openai.get_result(response)
    print("result："+result)
    return result


# 对外: 单次内容处理，流式，返回response
def modelConfig_content_stream_response(gpt_type, api_key,
                        input_text, maxtokens_config, temperature_config, model_config, system_prompt):
    print("system_prompt："+system_prompt)
    if gpt_type == 'wenxin':
        # 文心一言
        print('wenxin')
        response = wenxin.get_response(api_key, input_text, model_config, system_prompt, stream=True)
        return response
    # if gpt_type == '':

    # openai，默认是openai
    print('openai')
    response = openai.get_response(api_key,
                                   input_text, model_config, temperature_config, maxtokens_config,
                                   system_prompt, stream=True)
    return response


# 对外: 单次内容处理，流式，返回result(function)
def modelConfig_content_stream_result(gpt_type, response):
    if gpt_type == 'wenxin':
        # 文心一言
        return wenxin.get_result(response, stream=True)
    # if gpt_type == '':

    # openai，默认是openai
    print('openai')
    return openai.get_result(response, stream=True)


# 批处理excel2excel，内部调用
def modelConfig_batch(gpt_type, api_key,
                   input_text, maxtokens_config, temperature_config,model_config,
                   system_prompt, user_prompt, ex_user_prompt, ex_assistant_prompt):
    if gpt_type == 'wenxin':
        # 文心一言
        print('wenxin')
        response = wenxin.get_response(api_key,
                                       input_text, model_config,
                                       system_prompt, user_prompt, ex_user_prompt, ex_assistant_prompt)
        return wenxin.get_result(response)

    # if gpt_type == '':

    # openai，默认是openai
    print('openai')
    response = openai.get_response(api_key,
                                   input_text, model_config, temperature_config, maxtokens_config,
                                   system_prompt, user_prompt, ex_user_prompt, ex_assistant_prompt)
    result = openai.get_result(response)
    return result
