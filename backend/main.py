import uvicorn
from app.api.routers.chatglm import chat_router_local
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

app = FastAPI()

app.include_router(chat_router_local, prefix="/api/chat")
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # 或者指定前端应用的域名
    allow_credentials=True,
    allow_methods=["*"],  # 允许所有方法
    allow_headers=["*"],  # 允许所有头部
)

if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", reload=False)
