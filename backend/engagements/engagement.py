from backend.engagements.llm import LLM
from backend.engagements.engagement_data import EngagementData
from backend.engagements.engagement_data_manager import EngagementDataManager
from backend.engagements.pages.page import Page
from backend.engagements.pages.page_manager import PageManager
from bs4 import BeautifulSoup


class Engagement:
    def __init__(
        self,
        engagement_data_manager: EngagementDataManager,
        llm: LLM,
        data: EngagementData | Page,
    ) -> None:
        """
        Set references to engagement_manager and llm.
        If given a Page then create new EngagementData.
        :param engagement_data_manager: EngagementDataManager instance.
        :param llm: LLM instance.
        :param data: EngagementData or Page to start new EngagementData.
        """
        self.engagement_data_manager = engagement_data_manager
        self.llm = llm
        if isinstance(data, EngagementData):
            self.data = data
        elif isinstance(data, Page):
            self.data = EngagementData(self.llm, data)

    def get_slug(self) -> str:
        """
        Get the slug identifying the engagement.
        :return: Slug.
        """
        return self.data.get_slug()

    def get_source_urls(self) -> set[str]:
        """
        Get all URLs for the engagement sources.
        :return: Set of source URLs.
        """
        return self.data.get_source_urls()

    def get_data(self) -> EngagementData:
        """
        Get the EngagementData object.
        :return: EngagementData.
        """
        return self.data

    def add_source_url(self, url: str) -> None:
        """
        Add a new source URL to the engagement.
        :param url: Source URL.
        """
        self.data.add_source_url(url)
        self.engagement_data_manager.save_data()

    def get_page_manager(self) -> PageManager:
        """
        Get the PageManager instance.
        :return: PageManager instance.
        """
        return self.engagement_data_manager.get_page_manager()

    def get_source(self, url: str) -> Page:
        """
        Get a source that belongs to the engagement.
        :param url: Page URL.
        :return: Page.
        """
        if url not in self.data.get_source_urls():
            raise Exception(
                f"Source URL {url} not found in Engagement {self.get_slug()}"
            )
        return self.get_page_manager().get_page(url)

    def get_sources(self) -> list[Page]:
        """
        Get all sources that belong to the engagement.
        :return: List of Pages.
        """
        pages = []
        for url in self.data.get_source_urls():
            page = self.get_source(url)
            pages.append(page)
        return pages

    def get_images(self) -> list[BeautifulSoup]:
        """
        Get the images from all pages. Each image has the "alt" attribute and either "src" or "srcset" attribute.
        :return: List of images.
        """
        images = []
        for url in self.get_source_urls():
            images += self.get_page_manager().get_page(url).get_images()
        return images

    def get_title(self) -> str:
        """
        Get the engagement title.
        :return: Title.
        """
        return self.get_slug().replace("_", " ").capitalize()

    def get_summary(self) -> list[str]:
        """
        Get a summary of the engagement in short sentences.
        :return: List of sentences.
        """
        sentences = []
        for page in self.get_sources():
            sentences += self.llm.summarise(page)
        return sentences

    def get_employees(self) -> set[str]:
        """
        Get a list of employees involved in the engagement.
        :return: List of employees.
        """
        employees = set()
        for page in self.get_sources():
            employees = employees.union(self.llm.employees(page))
        return employees
