import subprocess
import os
import openai
from dotenv import load_dotenv

class OpenAIConnector:
    def __init__(self, token: str, filepath: str, model_name: str):
        self.filepath = filepath
        self.model_name = model_name
        self.token = token

    def upload_dataset(self):
        load_dotenv()
        openai.api_key = os.getenv("OPENAI_API_KEY")
        openai.File.create(
        file=open(self.prepared_filepath),
        purpose='fine-tune'
        )
        openai_file_list = openai.File.list()
        # Sort file list by date (reversed)
        sorted_files = sorted(openai_file_list['data'], key=lambda d: d['created_at'], reverse=True)
        new_file = sorted_files[0]['id']
        print(new_file)

        return new_file

    def create_fine_tune_model(self):
        load_dotenv()
        openai_training_file = os.getenv("TRAINING_FILE")
        openai.FineTune.create(training_file=openai_training_file, model="curie", n_epochs=5)

        # print(openai.FineTune.list())
        openai_fine_tune_list = openai.FineTune.list()
        sorted_fine_tunes = sorted(openai_fine_tune_list['data'], key=lambda d: d['created_at'], reverse=True)
        # Need to update this, not sure if newest fine tune model is always last in the list
        new_model = sorted_fine_tunes[0]["fine_tuned_model"]
        print(new_model)

        return new_model