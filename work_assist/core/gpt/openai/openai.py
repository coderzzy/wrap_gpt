# https://pypi.org/project/openai/1.2.4/
from openai import OpenAI


def get_response(api_key,
                 input_text, model_config, temperature_config,
                 system_prompt='', user_prompt='', ex_user_prompt='', ex_assistant_prompt='',
                 stream=False):
    client = OpenAI(
        # defaults to os.environ.get("OPENAI_API_KEY")
        api_key=api_key,
    )
    messages = [{"role": "system", "content": system_prompt}]
    if ex_user_prompt != "" and ex_assistant_prompt != "":
        messages.append({"role": "user", "content": ex_user_prompt})
        messages.append({"role": "assistant", "content": ex_assistant_prompt})
    if user_prompt != "":
        messages.append({"role": "user", "content": f"{user_prompt}：{input_text}"})
    else:
        messages.append({"role": "user", "content": input_text})
    response = client.chat.completions.create(
        model=model_config,
        messages=messages,
        temperature=temperature_config,  #between 0 and 2， default=1.0 【数值越高，创新+多样性越强，但可能不太保守】
        stream=stream,
    )
    return response


def get_result(response):
    return response.choices[0].message.content


def get_stream_result(response):
    for chunk in response:
        content = chunk.choices[0].delta.content
        if not content:
            content = '~'
        yield content


def get_figure_response(api_key, base64_image,
                                   model_config,
                                   system_prompt, stream=False):
    client = OpenAI(
        api_key=api_key,
    )
    messages = [
        {
            "role": "user",
            "content":[
                {"type": "text", "text": system_prompt},
                {"type": "image_url", "image_url": {"url": f"data:image/jpeg;base64,{base64_image}"}}
            ]
        }
    ]
    response = client.chat.completions.create(
        model=model_config,
        messages=messages,
        stream=stream,
        max_tokens=500,  # 未知原因，openai的图片处理，默认token值很小
    )
    return response
