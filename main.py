import os
from dotenv import load_dotenv
from fastapi import FastAPI
from pydantic import BaseModel
from openai import OpenAI

# 加载 .env 文件里的密钥
load_dotenv()

#运行成功后执行这段代码：uvicorn main:app --reload

# 从环境变量里读取密钥，这样代码里就没有明文了
client = OpenAI(
    api_key=os.getenv("DEEPSEEK_API_KEY"), 
    base_url="https://api.deepseek.com"
)

app = FastAPI()

# 定义接收数据的格式
class ErrorRequest(BaseModel):
    error_msg: str

# 把之前的 GET 改成 POST，因为我们要传输一段比较长的代码报错文本
@app.post("/ask")
def ask_question(request: ErrorRequest):
    # 构造 Prompt，给大模型设定人设
    prompt = f"你是一个耐心的少儿编程老师，请用通俗易懂的语言，给一个初学者解释这个Python报错并提供修改建议：\n{request.error_msg}"
    
    # 调用 DeepSeek 的大模型
    response = client.chat.completions.create(
        model="deepseek-chat",
        messages=[
            {"role": "user", "content": prompt}
        ]
    )
    
    # 提取大模型返回的文本并返回给前端
    ai_reply = response.choices[0].message.content
    return {"reply": ai_reply}