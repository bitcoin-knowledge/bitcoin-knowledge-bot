import json
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from app.bot import ask
from app.article_suggestion import suggest_article
from app.bot import ping

class ChatLog(BaseModel):
    chat_log: str

origins = [
    "http://localhost:3000",
    "https://bitcoin-knowledge-bot.vercel.app",
    "https://bitcoin-knowledge-bot-frontend.vercel.app",
    "http://localhost:19006",
    "http://localhost:19002"
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
    return "Bot online"

def run():
    app.run(host="0.0.0.0", port=8080)


@app.get('/ping')
def pass_ping():
    ping("")


@app.post("/ask")
def ask_bot(log: ChatLog):
    question = log.chat_log.split('###')[-1]
    answer = ask(log.chat_log)
    # articles = suggest_article(question)
    predictions = {
        "answer": answer,
        "articles": []
    }

    return predictions

@app.get("/knowledge")
def get_knowledge():
    unique = set()
    articles = []
    podcasts = []
    with open("./datasets/knowledge_datasets/bitcoin_articles.json", "r") as f:
        for obj in f:
            line = json.loads(obj)
            if line["title"] not in unique:
                unique.add(line["title"])
                articles.append(line)
    with open("./datasets/knowledge_datasets/bitcoin_podcasts.json", "r") as f:
        for obj in f:
            line = json.loads(obj)
            if line["title"] not in unique:
                unique.add(line["title"])
                podcasts.append(line)
    data = {
        "articles": articles,
        "podcasts": podcasts
    }

    return data
