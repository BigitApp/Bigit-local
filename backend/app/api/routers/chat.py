import json
from typing import Optional, Sequence
from app.utils.index import get_index
from fastapi import APIRouter, HTTPException, Request, status
from fastapi.responses import StreamingResponse
from bigdl.llm.transformers import AutoModel
from transformers import AutoTokenizer

from bigdl.llm.llamaindex.llms.bigdlllm import BigdlLLM
from llama_index import ServiceContext
from llama_index.llms.base import ChatMessage
from llama_index.llms.types import MessageRole
from llama_index.llms.openai import OpenAI
from pydantic import BaseModel
from llama_index.chat_engine import SimpleChatEngine

chat_router = r = APIRouter()


class _Message(BaseModel):
    role: MessageRole
    content: str


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
    messages: Optional[Sequence[_Message]] = None
    datasource: Optional[str] = None
    config: Optional[_LLMConfig] = None
    embeddings: Optional[Sequence[_Embedding]] = None


def convert_sse(obj: any):
    return "data: {}\n\n".format(json.dumps(obj))


def llm_from_config(config: Optional[_LLMConfig]):
    # if config:
        # return OpenAI(
        #     model=config.model,
        #     temperature=config.temperature,
        #     max_tokens=config.maxTokens,
        # )
    model_path = "/home/aowang/chat-llamaindex/backend/llms/chatglm-6b"
    model = AutoModel.from_pretrained(model_path, load_in_4bit=True, trust_remote_code=True)
    tokenizer = AutoTokenizer.from_pretrained(model_path, trust_remote_code=True)
    return BigdlLLM(
        model=model,  # 已加载的模型对象
        tokenizer=tokenizer,  # 已加载的分词器对象
    )
    # else:
    #     return OpenAI(model="gpt-3.5-turbo")


@r.post("")
async def chat(request: Request, data: _ChatData):
    service_context = ServiceContext.from_defaults(llm=llm_from_config(data.config))


    # if not data.datasource:
    #     # TODO: add support for simple chat without datasource
    #     raise HTTPException(
    #         status_code=status.HTTP_400_BAD_REQUEST,
    #         detail="No datasource provided",
    #     )

    index = get_index(service_context, 'watchos')

    # convert messages coming from the request to type ChatMessage
    messages = (
        [ChatMessage(role=m.role, content=m.content) for m in data.messages]
        if data.messages
        else []
    )

    # query chat engine
    # chat_engine = SimpleChatEngine.from_defaults()
    chat_engine = index.as_chat_engine()
    response = chat_engine.s(data.message, messages)

    # stream response
    async def event_generator():
        for token in response.response_gen:
            # If client closes connection, stop sending events
            if await request.is_disconnected():
                break
            yield convert_sse(token)
        yield convert_sse({"done": True})

    return StreamingResponse(
        event_generator(),
        media_type="text/event-stream",

    )
