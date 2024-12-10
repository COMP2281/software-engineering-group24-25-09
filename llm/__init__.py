import subprocess

import ollama


class LLM:
    def ollama_running(self):
        try:
            self.client.list()
            return True
        except:
            return False

    def _start_ollama(self):
        subprocess.Popen(["ollama", "show", self.model_name]).wait()

    def start_ollama(self):
        if self.ollama_running():
            print("Ollama is already running")
            return
        else:
            self._start_ollama()

    def __init__(self, url: str, model_name: str):
        self.url = url
        self.model_name = model_name
        self.client = ollama.Client(host=self.url)
        self.start_ollama()
