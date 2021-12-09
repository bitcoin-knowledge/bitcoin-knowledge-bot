import json

def remove_duplicates():
    lines = []

    with open ('./datasets/openai_datasets/bitcoin_chatbot_training_data.jsonl', 'r') as f:
        for obj in f:
            line = json.loads(obj)
            if line not in lines:
                lines.append(line)

    with open ('./datasets/openai_datasets/bitcoin_chatbot_training_data.jsonl', 'w') as f:
        for line in lines:
            f.write(json.dumps(line) + '\n')

remove_duplicates()
