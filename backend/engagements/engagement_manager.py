from engagements.llm import LLM
from engagements.engagement_data import EngagementData
from engagements.engagement import Engagement
from engagements.engagement_data_manager import EngagementDataManager
from engagements.pages import Page, PageManager
from engagements.search import URL


class CannotCrawlException(Exception):
    def __init__(self, *args):
        super().__init__("Crawling this URL is disallowed", *args)


class EngagementManager:
    def __init__(self, llm: LLM, data_path, ignore_robots_file=False) -> None:
        """
        Set reference to LLM instance and instantiate EngagementDataManager.
        :param llm: LLM instance.
        :param data_path: Path to data directory.
        """
        self.llm = llm
        self.data_manager = EngagementDataManager(data_path)
        self.ignore_robots_file = ignore_robots_file

    def get_slugs(self) -> list[str]:
        """
        Get slugs for all engagements.
        :return: List of slugs.
        """
        return self.data_manager.get_slugs()

    def wrap_engagement_data(self, data: EngagementData) -> Engagement:
        """
        Wrap engagement data in a new Engagement object.
        Pass references to EngagementDataManager and LLM instances.
        :param data: Engagement data.
        :return: Engagement.
        """
        return Engagement(self.data_manager, self.llm, data)

    def get_engagement(self, slug: str) -> Engagement:
        """
        Get engagement identified by the slug.
        :param slug: Slug identifying the engagement.
        :return: Engagement.
        """
        engagement_data = self.data_manager.get_engagement_data(slug)
        return self.wrap_engagement_data(engagement_data)

    def get_engagements(self) -> dict[str, Engagement]:
        """
        Get dictionary of all slugs and their respective engagements.
        :return: Dictionary of engagements.
        """
        engagements = {}
        for slug in self.data_manager.get_slugs():
            engagements[slug] = self.get_engagement(slug)
        return engagements

    def get_page_manager(self) -> PageManager:
        """
        Get PageManager instance.
        :return: PageManager instance.
        """
        return self.data_manager.get_page_manager()

    def get_page(self, url: str) -> Page:
        """
        Get the page identified by the url.
        :param url: URL identifying the page.
        :return: Page.
        """
        return self.get_page_manager().get_page(url)

    def get_all_source_urls(self) -> set[str]:
        """
        Get a set of all sources URLs.
        :return: Set of source URLs.
        """
        return self.data_manager.get_all_source_urls()

    def add_engagement(self, engagement: Engagement) -> None:
        """
        Save an engagement to the data file.
        :param engagement: Engagement.
        """
        self.data_manager.add_engagement_data(engagement.get_data())

    def create_engagement_from_url(self, url: URL) -> Engagement | None:
        """
        Create and save an engagement from the URL if it does not already exist.
        :param url: URL to a source.
        :return: Engagement if created, None otherwise.
        """
        if not self.ignore_robots_file and not url.can_crawl():
            raise CannotCrawlException()
        url = str(url)
        if url in self.get_all_source_urls():
            return None
        page = self.get_page(url)
        engagement = Engagement(self.data_manager, self.llm, page)
        self.add_engagement(engagement)
        return engagement
