import subprocess

class OpenAIConnector:
    def __init__(self, token: str, filepath: str, model_name: str, prepare: bool = True):
        self.filepath = filepath
        self.model_name = model_name
        self.token = token
        self.prepare = prepare

    def prepare_fine_tune_dataset(self):
        # Runs the open ai fine tune dataset preparation CLI script on the dataset usine the instantiated filepath
        prepare = subprocess.run(["openai", "tools", "fine_tunes.prepare_data", "-f", self.filepath], capture_output=True)
        print(prepare.stdout.decode("utf-8"))

