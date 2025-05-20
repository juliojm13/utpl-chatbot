from fastapi import FastAPI
from app.interface import telegram

app = FastAPI()

app.include_router(telegram.router)

@app.get("/health")
def health_check():
    return {"status": "ok"} 