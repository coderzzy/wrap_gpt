# 批处理excel2excel（包括示例）
def modelConfig_ex(openai, input_text, maxtokens_config, temperature_config,model_config,system_prompt, user_prompt, ex_user_prompt, ex_assistant_prompt):
    response = openai.ChatCompletion.create(
        model=model_config,
        messages=[
            {"role": "system", "content": system_prompt},
            {"role": "user", "content": ex_user_prompt},
            {"role": "assistant", "content": ex_assistant_prompt},
            {"role": "user", "content": f"{user_prompt}：{input_text}"}
        ],
        max_tokens=maxtokens_config,
        temperature=temperature_config #between 0 and 2， default=1.0 【数值越高，创新+多样性越强，但可能不太保守】
    )
    result = response['choices'][0]['message']['content']
    print(result)

    return result

# 批处理excel2excel（不包括示例）
def modelConfig_nex(openai, input_text, maxtokens_config, temperature_config,model_config,system_prompt, user_prompt):
    response = openai.ChatCompletion.create(
        model=model_config,
        messages=[
            {"role": "system", "content": system_prompt},
            {"role": "user", "content": f"{user_prompt}：{input_text}"}
        ],
        max_tokens=maxtokens_config,
        temperature=temperature_config #between 0 and 2， default=1.0 【数值越高，创新+多样性越强，但可能不太保守】
    )
    result = response['choices'][0]['message']['content']
    print(result)

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
    print("input_text："+input_text)
    print("system_prompt："+system_prompt)
    print("result："+result)

    return result