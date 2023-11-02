from fastapi import FastAPI
from todo import router

app = FastAPI()

@app.get("/")
async def welcome() -> dict:
    return {
        "message" : "hello wordl!"
    }

app.include_router(router)