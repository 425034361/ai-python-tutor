import requests

url = "http://127.0.0.1:8000/ask"
payload = {"error_msg": "IndexError: list index out of range"}

# 发送 POST 请求
response = requests.post(url, json=payload)

# 打印服务器返回的结果
print(response.json()["reply"])