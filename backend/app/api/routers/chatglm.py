from fastapi import APIRouter, HTTPException, Request, status
from bigdl.llm.transformers import AutoModel
from transformers import AutoTokenizer
import torch

model_path = "/home/aowang/chat-llamaindex/backend/llms/chatglm-6b"
model = AutoModel.from_pretrained(model_path, load_in_4bit=True, trust_remote_code=True)
tokenizer = AutoTokenizer.from_pretrained(model_path, trust_remote_code=True)

chat_router = APIRouter()

async def chat(request: Request, data: dict):
    # 解析请求数据
    try:
        message = data.get("message")
        if not message:
            raise ValueError("Message is required.")
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=str(e),
        )

    # 准备输入
    prompt = f"问：{message}\n\n答："
    input_ids = tokenizer.encode(prompt, return_tensors="pt")

    # 使用BigDL模型生成回答
    with torch.inference_mode():
        output = model.generate(input_ids, max_new_tokens=512)
        response_text = tokenizer.decode(output[0], skip_special_tokens=True)

    # 返回回答
    return {"answer": response_text}

@chat_router.post("/chat")
async def chat_endpoint(request: Request, data: dict):
    response = await chat(request, data)
    return response