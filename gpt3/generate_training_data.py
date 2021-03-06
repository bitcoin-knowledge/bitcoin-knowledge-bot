import json
import string
import re
from .clean_text import clean

def generate(prompts):
    openai_data = []
    for count in range(len(prompts)):
        try:
            # Only create the object every other iteration
            if count % 2 == 0:
                # Make sure we're not grabbing empty text (This will skip over prompt/completions that are empty, have a podcast link, or are an outro to the podcast)
                if prompts[count].text != "" and prompts[count+1].text != "":
                    prompt_text = prompts[count].text
                    # cleaned_prompt_text = prompt_text.translate(str.maketrans('', '', string.punctuation))
                    completion_text = prompts[count+1].text
                    # cleaned_completion_text = completion_text.translate(str.maketrans('', '', string.punctuation))
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
                        final_prompt = clean(strdecode_prompt)
                        final_completion = clean(strdecode_completion)
                        if final_prompt != False and final_completion != False:
                            j = {
                                "prompt": f"{final_prompt}\n\n###\n\n",
                                "completion": " " + final_completion
                            }
                            openai_data.append(j)
                                

        except:
            print("Error")

    with open('./datasets/openai_datasets/bitcoin_chatbot_training_data.jsonl', 'a') as outfile:    
        for obj in openai_data:
            json.dump(obj, outfile)
            outfile.write('\n')