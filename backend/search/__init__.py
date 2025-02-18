import os
import pickle
from prompts import prompts
from googleapiclient.discovery import build
from .credit_counter import CreditCounter


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

    def google_search(self):
        """
        Iterates through provided prompts, querying Google API for each prompt, returning 10 URLs per request in JSON.
        :return: JSON results file, exception if out of credits.
        :rtype: JSON
        """
        # ensure every prompt can be queried or else report out of credits
        if self.counter.get_credits() < len(prompts):
            raise Exception("OUT OF CREDITS FOR EVERY PROMPT (WITHIN SEARCH)")

        results_JSON = []
        for prompt in prompts:
            # double check if there are enough credits remaining or not
            if not self.counter.credits_available():
                raise Exception("OUT OF CREDIT COUNTER (WITHIN SEARCH)")
            # add the returned json information for result given by the prompt to the array
            results_JSON.append(self.use_google_api(prompt))

        print(results_JSON)

    def use_google_api(self, prompt: str):
        """
        Calls the Google Search API with a given prompt.
        :param prompt: Google search prompt to be requested
        :return: item section of JSON response
        :rtype: JSON
        """
        # edit the counter for the outgoing api request
        self.counter.decrement_credits()
        self.save_counter()
        # call google custom search api
        service = build("customsearch", "v1", developerKey=self.api_key)
        res = service.cse().list(q=prompt, cx=self.cse_id, num=10).execute()
        # return the item section of the json response (removes irrelevent headers)
        return res["items"]

    def extract_URLs_from_JSON(self, json_data):
        """
        Extracts URLs from the returned JSON of found sites
        :param json_data: JSON data to be converted
        :return: list of URLs
        """
        URLs = []
        for result in json_data:
            URLs.append(result["link"])
        return URLs
