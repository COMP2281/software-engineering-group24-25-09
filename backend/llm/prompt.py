class Prompt:
    def __init__(self, instruction: str, prompt: str):
        self.instruction = instruction
        self.prompt = prompt

    @staticmethod
    def summarise(source: str):
        return Prompt(
            """You are extracting IBM employees involved in educational outreach.
            You will receive the content from a web page in the following format:
            Line 1: The URL of the web page
            Line 2: A sequence of lists representing images by their alt text and URL
            Line 3: A sequence of lists containing headings, where the lists are in order of importance
            Remaining lines: All text extracted from paragraph tags
            Please list each IBM employee involved.
            Write each on a new line.
            Do not confirm this message or say anything else.
            Avoid any formatting or indentation.""",
            source,
        )
