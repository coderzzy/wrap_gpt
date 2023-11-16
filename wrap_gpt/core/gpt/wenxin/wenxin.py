# https://yiyan.baidu.com/developer/doc#Glm002aat
import erniebot


def get_response(api_key,
                 input_text, model_config,
                 system_prompt='', user_prompt='', ex_user_prompt='', ex_assistant_prompt='',
                 stream=False):
    messages=[
        {"role": "user", "content": f"{system_prompt}"},
        {"role": "assistant", "content": "好的"}
    ]
    if ex_user_prompt != "" and ex_assistant_prompt != "":
        messages.append({"role": "user", "content": ex_user_prompt})
        messages.append({"role": "assistant", "content": ex_assistant_prompt})
    if user_prompt != "":
        messages.append({"role": "user", "content": f"{user_prompt}：{input_text}"})
    else:
        messages.append({"role": "user", "content": repr(input_text)})
    response = erniebot.ChatCompletion.create(
        _config_=dict(
            api_type="aistudio",
            access_token=api_key,
        ),
        model=model_config,
        messages=messages,
        stream=stream,
    )
    return response


def get_result(response, stream=False):
    if stream:
        for chunk in response:
            content = chunk.result
            yield content
    else:
        return response['result']