import re
from backend.engagements.llm import LLM
from backend.engagements.pages import Page


class EngagementData:
    @staticmethod
    def title_to_slug(title: str) -> str:
        """
        Convert a title string into a lowercase, alphanumeric, underscored slug.
        :param title: Title.
        :return: Slug.
        """
        title = title.strip().lower()
        # replace variable length spaces with single underscores
        title = re.sub(r" +", "_", title)
        # remove any character that is not alphanumeric or an underscore
        return re.sub("[^a-z0-9_]", "", title)

    def __init__(self, llm: LLM, page: Page) -> None:
        """
        Initialise with one source URL and generate a slug from the source.
        :param llm: LLM instance.
        :param page: Page.
        """
        self.source_urls = {page.get_url()}
        self.slug = self.title_to_slug(llm.title(page))

    def get_slug(self) -> str:
        """
        Get the slug identifying the engagement.
        :return: Slug.
        """
        return self.slug

    def get_source_urls(self) -> set[str]:
        """
        Get all URLs for the engagement sources.
        :return: Set of source URLs.
        """
        return self.source_urls

    def add_source_url(self, url : str) -> None:
        """
        Add a new source URL to the engagement.
        :param url: Source URL.
        """
        self.source_urls.add(url)
