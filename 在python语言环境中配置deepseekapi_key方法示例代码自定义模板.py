# 把API Key添加到环境变量
# 安装openai模块
import os
from openai import OpenAI

# 从环境变量中读取API Key
api_key = os.getenv("CQKXGdeepseekapikey")

if not api_key:
    raise ValueError("Please set the CQKXGdeepseekapikey environment variable.")

client = OpenAI(api_key=api_key, base_url="https://api.deepseek.com/v1")

response = client.chat.completions.create(
    model="deepseek-chat",
    messages=[
        {"role": "system", "content": "You are a helpful assistant"},
        {"role": "user", "content": "Hello"},
    ],
    stream=False,
)

print(response.choices[0].message.content)
