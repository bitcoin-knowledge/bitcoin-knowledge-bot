import requests
from pathlib import Path

def get_project_root() -> Path:
    return Path(__file__).parent.parent


def ping_fine_tune_model():
    url = "https://api.openai.com/v1/fine-tunes/ft-Iid0qFfG44dFyu34vaiM0NJF"
    response = requests.get(url)
    if response.status_code == 200:
        return True
    else:
        return False