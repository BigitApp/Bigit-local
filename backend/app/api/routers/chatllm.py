from bigdl.llm.transformers import AutoModel
from transformers import AutoTokenizer
import torch

# 加载模型和分词器
model_path = "/home/aowang/chat-llamaindex/backend/llms/chatglm-6b"
model = AutoModel.from_pretrained(model_path, load_in_4bit=True, trust_remote_code=True)
tokenizer = AutoTokenizer.from_pretrained(model_path, trust_remote_code=True)

# 多轮对话的上下文管理
context = ""
while True:
    # 获取用户输入
    prompt = input("你想问AI什么？\n> ")

    # 如果用户输入退出，结束循环
    if prompt.lower() == '退出':
        print("感谢与AI对话，再见！")
        break

    # 更新上下文
    context += prompt + "\n"

    # 格式化提示模板
    CHATGLM_V2_PROMPT_TEMPLATE = "问：{}\n\n答：".format(context)

    # 使用分词器编码输入
    input_ids = tokenizer.encode(CHATGLM_V2_PROMPT_TEMPLATE.format(prompt=prompt), return_tensors="pt")

    # 使用模型生成答案
    with torch.inference_mode():
        output = model.generate(input_ids, max_new_tokens=512)

    # 解码输出并打印
    output_str = tokenizer.decode(output[0], skip_special_tokens=True)
    print('-' * 20, 'AI的回答', '-' * 20)
    print(output_str)

    # 清空上下文以开始新的对话
    context = ""