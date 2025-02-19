import re
import subprocess
import httpx
import ollama

from backend.engagements.llm.prompt import Prompt
from backend.engagements.llm.prompt_builder import PromptBuilder
from backend.engagements.pages import Page


class LLM:
    def ollama_running(self) -> bool:
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

    def _start_ollama(self) -> None:
        subprocess.Popen(["ollama", "show", self.model_name]).wait()

    def start_ollama(self) -> None:
        if self.ollama_running():
            print("Ollama is already running")
        else:
            self._start_ollama()

    def __init__(self, url: str, model_name: str) -> None:
        self.url = url
        self.model_name = model_name
        self.client = ollama.Client(host=self.url)
        self.start_ollama()

    def _generate(self, prompt: Prompt) -> str:
        return self.client.generate(
            model=self.model_name, system=prompt.instruction, prompt=prompt.prompt
        ).response

    def summarise(self, page: Page) -> list[str]:
        response = self._generate(PromptBuilder.summarise(page.get_markdown_content()))
        sentences = re.split(r"\n+", response)
        return sentences

    def employees(self, page: Page) -> list[str]:
        response = self._generate(PromptBuilder.employees(page.get_markdown_content()))
        employees = re.split(r"\n+", response)
        return employees

    def title(self, page: Page) -> str:
        return self._generate(PromptBuilder.title(page.get_markdown_content()))
