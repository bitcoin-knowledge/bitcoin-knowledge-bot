from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from app.bot import ask
from app.article_suggestion import suggest_article
from app.app_utils import ping_fine_tune_model

class ChatLog(BaseModel):
    chat_log: str

origins = [
    "http://localhost:3000",
    "https://bitcoin-knowledge-bot.vercel.app"
]

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_methods=["GET", "POST"],
    allow_headers=["*"],
)

@app.get('/')
def main():
    # ping_fine_tune_model()
    return "Bot online"

def run():
    app.run(host="0.0.0.0", port=8080)

@app.post("/ask")
def ask_bot(log: ChatLog):
    answer = ask(log.chat_log)
    articles = suggest_article(log.chat_log)
    predictions = {
        "answer": answer,
        "articles": [articles]
    }

    return predictions