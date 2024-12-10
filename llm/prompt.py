class Prompt:
    def __init__(self, instruction, prompt):
        self.instruction = instruction
        self.prompt = prompt

    @staticmethod
    def summarise(source):
        return Prompt(
            """You are summarising an article for a slide in a slideshow.
            You will receive the content from a web page in the following format:
            Line 1: The URL of the web page
            Line 2: A sequence of lists representing images by their alt text and URL
            Line 3: A sequence of lists containing headings, where the lists are in order of importance
            Remaining lines: All text extracted from paragraph tags
            Please summarise the article with a list of short sentences.
            Write each sentence on a new line.
            Do not write anything else.
            Avoid any formatting or indentation.""",
            source,
        )
