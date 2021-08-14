from flask import Flask
from flask import request
from threading import Thread
import bot

app = Flask('')

@app.route('/')
def main():
    return "Your bot is alive!"

def run():
    app.run(host="0.0.0.0", port=8080)

def keep_alive():
    server = Thread(target=run)
    server.start()

@app.route('/ask', methods=['POST'])
def ask_bot():
    question = request.json["question"]
    answer = bot.ask(question)
    # run keep_alive everytime there is a request

    return answer
    
keep_alive()