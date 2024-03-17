from fastapi import APIRouter, HTTPException, Request, status
from bigdl.llm.transformers import AutoModel
from transformers import AutoTokenizer
import torch
from pydantic import BaseModel
from typing import Optional, Sequence, Dict

model_path = "/home/aowang/chat-llamaindex/backend/llms/chatglm-6b"
model = AutoModel.from_pretrained(model_path, load_in_4bit=True, trust_remote_code=True)
tokenizer = AutoTokenizer.from_pretrained(model_path, trust_remote_code=True)

chat_router_local = APIRouter()


class _LLMConfig(BaseModel):
    model: str
    temperature: Optional[float] = None
    topP: Optional[float] = None
    sendMemory: bool = False
    maxTokens: int = 2000


class _Embedding(BaseModel):
    text: str
    embedding: Sequence[float]

class _ChatData(BaseModel):
    message: str
    chatHistory: Sequence[Dict[str, str]]  # 使用字典列表来表示聊天历史
    datasource: Optional[str] = None
    config: Optional[_LLMConfig] = None
    embeddings: Optional[Sequence[_Embedding]] = None

async def chat(request: Request, data: _ChatData):
    # 解析请求数据
    try:
        message = data.message
        chat_history_list = [entry["content"] for entry in data.chatHistory]  # 提取每次交互的内容
        chat_history_str = "\n".join(chat_history_list)  # 将聊天历史连接成一个字符串

        if not message:
            raise ValueError("Message is required.")
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=str(e),
        )

    # 准备输入
    prompt = f"历史聊天是这样的：{chat_history_str}\n\n问题是这样的：{message}\n\n答：,请为我写出最终的答案"
    input_ids = tokenizer.encode(prompt, return_tensors="pt")

    # 使用BigDL模型生成回答
    with torch.inference_mode():
        output = model.generate(input_ids, max_new_tokens=512)
        response_text = tokenizer.decode(output[0][len(input_ids[0]):], skip_special_tokens=True)
        print('answer:',response_text)
    # 返回回答
    return {response_text}

@chat_router_local.post("/api/chat")
async def chat_endpoint(request: Request, data: _ChatData):
    response = await chat(request, data)
    return response