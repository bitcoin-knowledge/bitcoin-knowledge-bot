import re
import os
import openai
import json
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

    # Clean and continually write to training file as text lists are fed in and filtered
    def clean_text(self, text_list):
        openai_data = []
        for count in range(len(text_list)):
            try:
                # Only create the object every other iteration
                if count % 2 == 0:
                    if text_list[count].text != "" and text_list[count+1].text != "":
                        prompt_text = text_list[count].text
                        completion_text = text_list[count+1].text
                        # Get rid of any text that is shorter than 50 chars
                        # Get rid of any text that has no whitespace in it
                        if len(prompt_text) > 50 and prompt_text.find(" ") != -1 and len(completion_text) > 50 and completion_text.find(" ") != -1:
                            # Remove all non ascii chars
                            # prompts
                            strencode_prompt = prompt_text.encode("ascii", "ignore")
                            strdecode_prompt = strencode_prompt.decode()
                            # completions
                            strencode_completion = completion_text.encode("ascii", "ignore")
                            strdecode_completion = strencode_completion.decode()
                            # Filter out any string with more than one white space in between characters
                            re.sub(" +", ' ', strdecode_prompt)
                            re.sub(" +", ' ', strdecode_completion)
                            final_prompt = self.filter_text(strdecode_prompt)
                            final_completion = self.filter_text(strdecode_completion)
                            if final_prompt != False and final_completion != False:
                                j = {
                                    "prompt": f"{final_prompt}\n\n###\n\n",
                                    "completion": " " + final_completion
                                }
                                openai_data.append(j)                   

            except:
                print("Error")
        # Continually write to training file
        with open('./datasets/openai_datasets/bitcoin_chatbot_training_data.jsonl', 'a') as outfile:    
            for obj in openai_data:
                json.dump(obj, outfile)
                outfile.write('\n')


    def filter_text(text):
        num_of_letters = len(text) - text.count(" ")
        if text.count(" ") < num_of_letters:
            return text
        else:
            return False