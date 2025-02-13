from backend.engagements.llm import LLM
from backend.engagements.pages import PageManager, Page
from backend.engagements.engagement_data import EngagementData
from backend.engagements.engagement import Engagement
from backend.engagements.engagement_data_manager import EngagementDataManager


class EngagementManager:
    def __init__(self, llm: LLM, data_path) -> None:
        """
        Set reference to LLM instance and instantiate EngagementDataManager.
        :param llm: LLM instance.
        :param data_path: Path to data directory.
        """
        self.llm = llm
        self.data_manager = EngagementDataManager(data_path)

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

    def add_engagement(self, engagement: Engagement) -> None:
        """
        Save an engagement to the data file.
        :param engagement: Engagement.
        """
        self.data_manager.add_engagement_data(engagement.get_data())

    def create_engagement_from_url(self, url):
        # TODO: check if engagement already exists
        engagement = Engagement(self.data_manager, self.llm, self.get_page(url))
        self.add_engagement(engagement)
        return engagement
