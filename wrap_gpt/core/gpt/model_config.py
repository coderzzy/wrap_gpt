# 批处理excel2excel
def modelConfig_batch(openai,
                   input_text, maxtokens_config, temperature_config,model_config,
                   system_prompt, user_prompt, ex_user_prompt, ex_assistant_prompt):
    messages = [{"role": "system", "content": system_prompt}]
    if ex_user_prompt != "" and ex_assistant_prompt != "":
        messages.append({"role": "user", "content": ex_user_prompt})
        messages.append({"role": "assistant", "content": ex_assistant_prompt})
    messages.append({"role": "user", "content": f"{user_prompt}：{input_text}"})
    response = openai.ChatCompletion.create(
        model=model_config,
        messages = messages,
        max_tokens=maxtokens_config,
        temperature=temperature_config #between 0 and 2， default=1.0 【数值越高，创新+多样性越强，但可能不太保守】
    )
    result = response['choices'][0]['message']['content']
    return result

# 单次内容输入
def modelConfig_content(openai, input_text, temperature_config, model_config, system_prompt):
    response = openai.ChatCompletion.create(
        model=model_config,
        messages=[
            {"role": "system", "content": f"{system_prompt}"},
            {"role": "user", "content": f"{input_text}"}
        ],
        temperature=temperature_config #between 0 and 2， default=1.0 【数值越高，创新+多样性越强，但可能不太保守】
    )
    result = response['choices'][0]['message']['content']
    print("system_prompt："+system_prompt)
    print("result："+result)

    return result