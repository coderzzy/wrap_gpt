# 异步处理excel数据
import os
from wrap_gpt.core.constants import EXCEL_ROOT
import asyncio

async def process_excel(origin_filename, filepath):
    await asyncio.sleep(5)
    print(22222)
    # os.rename(filepath, os.path.join(EXCEL_ROOT, 'finished_'+origin_filename))