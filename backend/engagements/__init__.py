import os
import pickle

from .engagement import Engagement, EngagementData
from .llm import LLM
from .pages import PageManager, Page


class EngagementManager:
    def file_exists(self):
        return os.path.isfile(self.file_path)

    def load_engagements(self):
        if self.file_exists():
            file = open(self.file_path, "rb")
            self.engagement_data_objects = pickle.load(file)

    def __init__(self, llm: LLM, data_path):
        self.file_path = os.path.join(data_path, "engagements.pickle")
        self.page_manager = PageManager(data_path)
        self.llm = llm
        self.engagement_data_objects = {}
        self.load_engagements()

    def save_engagements(self):
        file = open(self.file_path, "wb")
        pickle.dump(self.engagement_data_objects, file)

    def wrap_engagement_data(self, data: EngagementData) -> Engagement:
        return Engagement(self, data)

    def get_engagement_data(self, slug):
        return self.engagement_data_objects[slug]

    def get_engagement(self, slug: str) -> Engagement:
        engagement_data = self.get_engagement_data(slug)
        return self.wrap_engagement_data(engagement_data)

    def get_engagements(self):
        engagements = {}
        for slug in self.engagement_data_objects:
            engagements[slug] = self.get_engagement(slug)
        return engagements

    def add_engagement_data(self, engagement_data: EngagementData) -> None:
        self.engagement_data_objects[engagement_data.get_slug()] = engagement_data
        self.save_engagements()

    def add_engagement(self, engagement: Engagement) -> None:
        self.add_engagement_data(engagement.get_data())
