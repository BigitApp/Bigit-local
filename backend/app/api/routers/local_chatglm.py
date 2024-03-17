import json
from typing import Optional, Sequence
from app.utils.index import get_index
from fastapi import APIRouter, HTTPException, Request, status
from fastapi.responses import StreamingResponse
from bigdl.llm.transformers import AutoModel
from transformers import AutoTokenizer

from bigdl.llm.llamaindex.llms.bigdlllm import BigdlLLM
from llama_index.core.base.llms.types import (
    ChatMessage,
    MessageRole,
)
from llama_index.llms.openai import OpenAI
from pydantic import BaseModel
from llama_index.core.settings import Settings

from llama_index.core.prompts.base import PromptTemplate
from llama_index.core.chat_engine import CondenseQuestionChatEngine


local_chatglm_router = r = APIRouter()


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
    chatHistory: Optional[Sequence[_Message]] = None
    datasource: Optional[str] = None
    config: Optional[_LLMConfig] = None
    embeddings: Optional[Sequence[_Embedding]] = None


def convert_sse(obj: any):
    return "data: {}\n\n".format(json.dumps(obj))


def llm_from_config(config: Optional[_LLMConfig]):
    model_path = "/home/aowang/chat-llamaindex/backend/llms/chatglm-6b"
    model = AutoModel.from_pretrained(model_path, load_in_4bit=True, trust_remote_code=True)
    tokenizer = AutoTokenizer.from_pretrained(model_path, trust_remote_code=True)
    return BigdlLLM(
        model=model, 
        tokenizer=tokenizer, 
    )


@r.post("")
async def local_chatglm(request: Request, data: _ChatData):
    local_llm=llm_from_config(data.config)
    Settings.llm = local_llm

    custom_prompt = PromptTemplate(
        """\
    Given a conversation (between Human and Assistant) and a follow up message from Human, \
    rewrite the message to be a standalone question that captures all relevant context \
    from the conversation.

    <Chat History>
    {chat_history}

    <Follow Up Message>
    {question}

    <Standalone question>
    """
    )
    index = get_index('watchos')

    # list of `ChatMessage` objects
    custom_chat_history = (
        [ChatMessage(role=m.role, content=m.content) for m in data.chatHistory]
        if data.chatHistory
        else []
    )

    query_engine = index.as_query_engine()
    chat_engine = CondenseQuestionChatEngine.from_defaults(
        query_engine=query_engine,
        condense_question_prompt=custom_prompt,
        chat_history=custom_chat_history,
        verbose=True,
    )

    response = chat_engine.chat(data.message)
    
    return response
