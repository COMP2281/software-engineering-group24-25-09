import ollama


class LLM:
    def start_ollama(self):
        pass

    def __init__(self, url: str, model_name):
        self.url = url
        self.model_name = model_name
        self.start_ollama()
