class Prompt:
    def __init__(self, instruction: str, prompt: str):
        self.instruction = instruction
        self.prompt = prompt

    @staticmethod
    def summarise(source: str):
        return Prompt(
            """You are finding how IBM have been involved in educational outreach.
            You will receive the content from a web page. It may contain irrelevant information outside of the main article.
            Please list a few very short sentences summarising the article.
            Write each on a new line.
            Do not confirm this message or say anything else.
            Avoid any formatting or indentation.""",
            source,
        )

    @staticmethod
    def employees(source: str):
        return Prompt(
            """You are finding IBM employees involved in educational outreach.
            You will receive the content from a web page. It may contain irrelevant information outside of the main article.
            Please list each IBM employee involved.
            Write each on a new line.
            Do not confirm this message or say anything else.
            Avoid any formatting or indentation.""",
            source,
        )
