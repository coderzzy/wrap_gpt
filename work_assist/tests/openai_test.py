import work_assist.core.gpt.model_config as model


def test_batch():
    gpt_type = 'openai'
    api_key = ''
    input_text = '光明优倍减脂肪50%鲜牛奶 950ml'
    temperature_config=1
    model_config = 'gpt-3.5-turbo-1106'
    system_prompt = '输出不超过10个字'
    user_prompt = '提取商品中的4个关键词'
    ex_user_prompt = ''
    ex_assistant_prompt = ''
    text = model.modelConfig_batch(gpt_type, api_key,
                            input_text, temperature_config, model_config,
                            system_prompt, user_prompt, ex_user_prompt, ex_assistant_prompt)
    print(text)


if __name__ == "__main__":
    test_batch()