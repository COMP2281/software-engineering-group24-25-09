import subprocess
import httpx
import ollama

from .prompt import Prompt


class LLM:
    def ollama_running(self):
        """
        Check if Ollama is running.
        :return: True if Ollama is running, otherwise False.
        :rtype: bool
        """
        # try to run Ollama list command
        try:
            self.client.list()
            return True
        # if it can't connect, return False
        except httpx.ConnectError:
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

    def _generate(self, prompt: Prompt):
        return self.client.generate(
            model=self.model_name, system=prompt.instruction, prompt=prompt.prompt
        ).response

    def summarise(self, source: str):
        return self._generate(Prompt.summarise(source))

    def employees(self, source: str):
        return self._generate(Prompt.employees(source))
