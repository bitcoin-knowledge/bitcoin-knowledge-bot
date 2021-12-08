import subprocess
import os
import openai
from dotenv import load_dotenv

class OpenAIConnector:
    def __init__(self, token: str, filepath: str, model_name: str, prepare: bool = True, prepared_filepath: str = None):
        self.filepath = filepath
        self.model_name = model_name
        self.token = token
        self.prepare = prepare
        self.prepared_filepath = prepared_filepath

    def prepare_fine_tune_dataset(self):
        # Runs the open ai fine tune dataset preparation CLI script on the dataset usine the instantiated filepath
        prepare = subprocess.run(["openai", "tools", "fine_tunes.prepare_data", "-f", self.filepath], capture_output=True)
        print(prepare.stdout.decode("utf-8"))

    def upload_dataset(self):
        load_dotenv()
        openai.api_key = os.getenv("OPENAI_API_KEY")
        openai.File.create(
        file=open(self.prepared_filepath),
        purpose='fine-tune'
        )

test = OpenAIConnector(token="", filepath="./datasets/openai_datasets/bitcoin_chatbot_training_data.jsonl", model_name="", prepare=True, prepared_filepath="")
test.prepare_fine_tune_dataset()