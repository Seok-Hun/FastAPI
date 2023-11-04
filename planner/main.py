from fastapi import FastAPI
from fastapi.responses import RedirectResponse
from typing import List
from routes.users import user_router
from routes.events import event_router
from database.connection import conn

import uvicorn

app = FastAPI()

# 라우트 등록
app.include_router(user_router, prefix="/user")
app.include_router(event_router, prefix="/event")

# 애플리케이션 실행 시 데이터베이스 생성
# conn()함수를 호출해 데이터베이스 생성
@app.on_event("startup")
def on_startup():
    conn()

# RedirectResponse는 상태 코드 307(리다이렉트) 반환
# /으로 접속하면 /event로 리다이렉트
@app.get("/")
async def home():
    return RedirectResponse(url="/event/")

if __name__ == "__main__":
    uvicorn.run("main:app", host="localhost", port=8000, reload=True)