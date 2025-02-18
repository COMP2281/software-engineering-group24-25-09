import os
import pickle
from .prompts import prompts
from googleapiclient.discovery import build, Resource
from .credit_counter import CreditCounter
from .types import SearchResponse
from .url import URL

PAGE_COUNT = 10


class SearchException(Exception):
    def __init__(self, message, *args):
        super().__init__(message * args)


class Search:
    def counter_file_exists(self) -> bool:
        """
        Check if counter file exists.
        :return: True if file exists, False otherwise.
        """
        return os.path.isfile(self.counter_file_path)

    def load_counter(self) -> None:
        """
        Load credit counter from file.
        """
        if self.counter_file_exists():
            file = open(self.counter_file_path, "rb")
            self.counter = pickle.load(file)["counter"]
        else:
            self.counter = CreditCounter()

    def save_counter(self) -> None:
        """
        Save credit counter to file.
        """
        file = open(self.counter_file_path, "wb")
        pickle.dump({"counter": self.counter}, file)

    def __init__(self, api_key: str, cse_id: str, data_path: str) -> None:
        """
        Set Google Cloud credentials and load counter from file. A new counter is created if none exists.
        :param api_key: Google Cloud API key.
        :param cse_id: Google Cloud CSE ID.
        :param data_path: Path to data directory.
        """
        self.api_key = api_key
        self.cse_id = cse_id
        self.counter_file_path = os.path.join(data_path, "counter.pickle")
        self.counter = None
        self.load_counter()
        self.save_counter()

    @property
    def service(self) -> Resource:
        """
        Get Google custom search service.
        :return: Service.
        """
        return build("customsearch", "v1", developerKey=self.api_key)

    def _query_service(self, prompt: str) -> SearchResponse:
        """
        Query Google custom search service given a prompt.
        :param prompt: Prompt to search for.
        :return: Search response.
        """
        return (
            self.service.cse()
            .list(
                q=prompt,
                cx=self.cse_id,
                num=PAGE_COUNT,
            )
            .execute()
        )

    def _decrement_credits(self) -> None:
        """
        Decrement credit counter. Raise an exception if out of credits.
        """
        if not self.counter.credits_available():
            raise SearchException("Daily search limit reached")
        else:
            self.counter.decrement_credits()
            self.save_counter()

    def search(self, prompt: str) -> set[URL]:
        """
        Search using Google API for URLs given a prompt.
        :param prompt: Prompt to search for.
        :return: List of URLs.
        """
        self._decrement_credits()
        response = self._query_service(prompt)
        urls = set()
        for result in response["items"]:
            urls.add(URL(result))
        return urls

    def search_all(self, prompts: list[str]) -> set[URL]:
        """
        Search using Google API for URLs given a list of prompts.
        Raise an exception if not enough credits for all prompts.
        :param prompts: List of prompts.
        """
        if not self.counter.credits_available_for(len(prompts)):
            raise SearchException("Daily search limit reached")

        urls = set()
        for prompt in prompts:
            urls.union(self.search(prompt))
        return urls
