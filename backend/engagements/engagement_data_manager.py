from backend.engagements.pages import PageManager, Page
from backend.engagements.engagement_data import EngagementData
from backend.saver import Saver


class EngagementDataManager(Saver):
    def __init__(self, data_path: str) -> None:
        """
        Instantiate PageManager and load engagements.
        :param data_path: Path to data directory.
        """
        super().__init__(data_path, "engagements")
        self.page_manager = PageManager(data_path)

    def get_slugs(self) -> list[str]:
        """
        Get slugs for all engagements.
        :return: List of slugs.
        """
        return list(self.data.keys())

    def get_engagement_data(self, slug: str) -> EngagementData:
        """
        Get the data from the engagement identified by the slug.
        :param slug: Slug identifying the engagement.
        :return: EngagementData for the engagement.
        """
        return self.data[slug]

    def get_page_manager(self) -> PageManager:
        """
        Get the PageManager instance.
        :return: PageManager instance.
        """
        return self.page_manager

    def get_all_source_urls(self) -> set[str]:
        """
        Get a set of all sources URLs.
        :return: Set of source URLs.
        """
        return self.page_manager.get_all_page_urls()

    def add_engagement_data(self, engagement_data: EngagementData) -> None:
        """
        Add engagement data to the manager and save it to the file.
        :param engagement_data: EngagementData.
        """
        self.data[engagement_data.get_slug()] = engagement_data
        self.save_data()
