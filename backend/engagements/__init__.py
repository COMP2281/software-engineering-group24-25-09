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
