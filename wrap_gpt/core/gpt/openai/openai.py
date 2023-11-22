# https://pypi.org/project/openai/1.2.4/
from openai import OpenAI
import requests

def get_response(api_key,
                 input_text, model_config, temperature_config, maxtokens_config=3000,
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
        max_tokens=maxtokens_config,
        temperature=temperature_config,  #between 0 and 2， default=1.0 【数值越高，创新+多样性越强，但可能不太保守】
        stream=stream,
    )
    print(response)
    return response


def get_result(response, stream=False):
    if stream:
        for chunk in response:
            print(chunk)
            content = chunk.choices[0].delta.content
            if not content:
                content = '~'
            yield content
    else:
        return response['choices'][0]['message']['content']


def get_figure_response_and_result(api_key, base64_image,
                                   model_config, maxtokens_config,
                                   system_prompt):
    headers = {
        "Content-Type": "application/json",
        "Authorization": f"Bearer {api_key}"
    }
    payload = {
        "model": model_config,
        "messages": [
            {
                "role": "user",
                "content": [
                    {
                        "type": "text",
                        "text": system_prompt
                    },
                    {
                        "type": "image_url",
                        "image_url": {
                            "url": f"data:image/jpeg;base64,{base64_image}"
                        }
                    }
                ]
            }
        ],
        "max_tokens": maxtokens_config
    }
    response = requests.post("https://api.openai.com/v1/chat/completions", headers=headers, json=payload)
    result = response.json()
    if 'error' in result:
        return result['error']['message']
    return result['choices'][0]['message']['content']
