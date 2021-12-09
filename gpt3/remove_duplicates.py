import json
from os import removedirs

def remove():
    lines = []

    with open ('./datasets/openai_datasets/bitcoin_chatbot_training_data.jsonl', 'r') as f:
        for obj in f:
            removed_count = 0
            line = json.loads(obj)
            if line not in lines:
                lines.append(line)
            else:
                removed_count += 1
                print(f'Removed {removed_count}')

    with open ('./datasets/openai_datasets/bitcoin_chatbot_training_data.jsonl', 'w') as f:
        for line in lines:
            f.write(json.dumps(line) + '\n')

remove()