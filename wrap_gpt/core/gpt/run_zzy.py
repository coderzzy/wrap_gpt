import openai

import input_process
from model_config import modelConfig_content, batchProcess


def run():
    # 特有传入参数
    mode_type = "batch"  # content, fine_tuning

    # 特有传入参数：批处理-excel列名
    column_name = '商品销售名称'
    output_column_name = 'GPT处理'

    # 全局默认配置参数（可传入）：
    api_key = ''
    openai.api_key = api_key
    input_path = 'test-GPT1.xlsx'
    output_path = 'outfile.xlsx'

    timesleep_config = 3
    maxtokens_config = 300
    temperature_config = 1.0
    model_config = 'gpt-3.5-turbo'

    #批处理测试【测试成功】
    if mode_type == "batch":
        # 模型prompt参数
        system_prompt = "结果输出不超过10个词，且不出现'搜索词'和'关键词'字样，并将所有词都用；连接成一行"
        user_prompt = ""
        ex_user_prompt = ""
        #user_prompt = "请帮我提取商品中4个关键词，并扩展5个极有可能能够搜索到该商品的搜索词"
        #ex_user_prompt = "请帮我提取商品中4个关键词，并扩展5个极有可能能够搜索到该商品的搜索词：东鹏0糖能量饮料(6罐装) 335ml*6"
        ex_assistant_prompt = "会议；商用；健身；运动；补充能量；东鹏；能量；饮料；罐装"
        # 执行(有示例)
        batchProcess(openai, input_path, output_path, column_name, output_column_name,
                     timesleep_config, maxtokens_config, temperature_config, model_config,
                     system_prompt, user_prompt, ex_user_prompt, ex_assistant_prompt)

    #单文本【测试成功】
    if mode_type == "content_word":
        input_text = input_process.file_read('word_test.txt')
        system_prompt = '总结文档,总共输出50字'
        modelConfig_content(openai, input_text, temperature_config, model_config, system_prompt)

    if mode_type == "content_excel":
        input_text = input_process.excel_read("Marketing_data_test.xlsx")
        system_prompt = "输出分析报告，要求：1.分析结果输出约600个字。2.变化趋势和呈现数据结合在一起,3.8月对比7月所有部类的占比趋势,4.输出可能有利于不同部类渗透率提高的建议"
        modelConfig_content(openai, input_text, temperature_config, model_config,system_prompt)

    #微调（待定）