import requests
from pathlib import Path
from app.bot import ask

def get_project_root() -> Path:
    return Path(__file__).parent.parent


def ping_fine_tune_model():
    ask("ping")