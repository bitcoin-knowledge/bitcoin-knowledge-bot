from pathlib import Path
from app.bot import ping

def get_project_root() -> Path:
    return Path(__file__).parent.parent