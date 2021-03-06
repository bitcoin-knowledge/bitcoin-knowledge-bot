import requests
from urllib import response
import openai
import os
from dotenv import load_dotenv

load_dotenv()

openai.api_key = os.getenv("OPENAI_API_KEY")
completion = openai.Completion()

model = os.getenv("FINE_TUNE_MODEL_PREMIUM")

test_chat_log = '''The following is a conversation with an AI assistant trained on an open source dataset of trusted Bitcoin (only) knowledge.
The AI assistant wants to steer its users towards fundemental knowledge of Bitcoin, warn against the many flaws and speculation with altcoins, and shine a light on the ong term possiblities of Bitcoin to positively impact the world.
The assistant is helpful, creative, clever, friendly and it tries it's best to simplify concepts (especially when asked).'''
start_chat_log = '''
The following is a conversation with an AI assistant trained on an open source dataset of trusted Bitcoin (only) knowledge.
The AI assistant wants to steer its users towards fundemental knowledge of Bitcoin, warn against the many flaws and speculation with altcoins, and shine a light on the ong term possiblities of Bitcoin to positively impact the world.
The assistant is helpful, creative, clever, friendly and it tries it's best to simplify concepts (especially when asked).


User: How does proof-of-work work in Bitcoin?\n\n###\n\n
Bot: A proof of work is a piece of data which is difficult (costly, time-consuming) to produce but easy for others to verify and which satisfies certain requirements. Producing a proof of work can be a random process with low probability so that a lot of trial and error is required on average before a valid proof of work is generated. Bitcoin uses the Hashcash proof of work system.\n
User: What is a hash?\n\n###\n\n
Bot: A hash is a function which takes a piece of data and converts it into a number.\n
User: What is SHA-256?\n\n###\n\n
Bot: SHA-256 is a specific hash function which takes a piece of data and converts it into a number.\n
User: What is a block?\n\n###\n\n
Bot: A block is a piece of data which contains a hash of the previous block and a set of transactions. These blocks make up the blockchain which is Bitcoin's distributed ledger with the full history and cryptographic proof of all of the previous transactions.\n
User: do you have any trading advice for me?\n\n###\n\n
Bot: Trading is risky and I dont give financial advice, I only suggest stacking Bitcoin and holding your own keys (Not your keys not your Bitcoin)\n
User: Thank you for the help!\n\n###\n\n
Bot: You're welcome, come back anytime!\n'''

def ask(chat_log: str):
    prompt = f'{test_chat_log}\n\n###\n\n{chat_log}Bot:'
    awake = False
    while not awake:
        response = completion.create(
            prompt=prompt, model=model, stop=['\n\n###\n\n', '\n'], temperature=0.4,
            frequency_penalty=1, presence_penalty=1, max_tokens=250)
        if not response.choices[0].text.strip():
            pass
        else:
            awake = True
    answer = response.choices[0].text.strip()
    
    return answer

def suggest_article(question: str):
    req = {"question": question}
    articles = requests.post('http://bitcoin-knowledge-suggestions.herokuapp.com/suggest_article', data=req)
    articles = articles.json()
    print(articles)
    return articles

def ping(p: str):
    prompt = f'{p}\n\n###\n\n'
    completion.create(
        prompt=prompt, model=model, stop=['\n\n###\n\n', '\n'], temperature=0.4,
        frequency_penalty=1, presence_penalty=1, max_tokens=1)