from backend.engagements.llm.prompt import Prompt


class PromptBuilder:
    @staticmethod
    def summarise(source: str) -> Prompt:
        return Prompt(
            """You are finding how IBM have been involved in educational outreach.
            You will receive the content from a web page. It may contain irrelevant information outside of the main article.
            Please list a few sentences of maximum 15 words each summarising the article.
            Write each on a new line.
            Do not confirm this message or say anything else.
            Avoid any formatting or indentation.""",
            source,
        )

    @staticmethod
    def employees(source: str) -> Prompt:
        return Prompt(
            """You are finding IBM employees involved in educational outreach.
            You will receive the content from a web page. It may contain irrelevant information outside of the main article.
            Please list the name of each IBM employee involved.
            Write each on a new line.
            Do not confirm this message or say anything else.
            Avoid any formatting or indentation.""",
            source,
        )

    @staticmethod
    def title(source: str) -> Prompt:
        return Prompt(
            """You will receive the content from a web page. It may contain irrelevant information outside of the main article.
            Please write a short title of maximum 15 words that describes the content.
            Do not confirm this message or say anything else.""",
            source,
        )
