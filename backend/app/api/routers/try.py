import requests
import json

# FastAPI应用的URL和端口
url = "http://127.0.0.1:8000" 
# 路由端点
endpoint = "/chat"

def ask_ai(question):
    # 准备请求数据
    data = {
        "message": question
    }
    # 发送POST请求
    response = requests.post(f"{url}{endpoint}", json=data)
    # 检查请求是否成功
    if response.status_code == 200:
        # 解析响应数据
        response_data = response.json()
        # 打印AI的回答
        print("AI的回答:", response_data.get("answer"))
    else:
        # 如果请求失败，打印错误信息
        print("请求失败，状态码:", response.status_code)
        print("错误信息:", response.text)

# 多轮对话循环
print("开始与AI对话。输入'退出'结束对话。")
while True:
    # 获取用户输入
    user_input = input("你想问AI什么？> ")
    if user_input.lower() == '退出':
        print("感谢与AI对话，再见！")
        break
    # 向AI提问
    ask_ai(user_input)