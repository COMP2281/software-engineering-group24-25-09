import json
import os
import pickle
from prompts import prompts
from googleapiclient.discovery import build
class SearchManager:
    def NoAPITest(self):
        # For testing without using credits
        file_path = "Web-Scraping\APICallManagment\APIcallReturns.json"
        with open(file_path, "r") as json_file:
            results = json.load(json_file)
        return results

    def CreateSearch(self):
        search = Search(api_key, cse_id, "../data")
        search.google_search()


class Search:
    def __init__(self, api_key: str, cse_id: str, data_path: str):
        self.api_key = api_key
        self.cse_id = cse_id
        self.file_path = os.path.join(data_path, "counter.pickle")
        self.counter = None
        self.load_counter()
        self.save_counter()

    def file_exists(self):
        """
        Check if counter file exists.
        :return: True if file exists, otherwise False.
        :rtype: bool
        """
        return os.path.isfile(self.file_path)

    def load_counter(self):
        """
        Loads pickle counter file
        """
        if self.file_exists():
            file = open(self.file_path, "rb+")
            self.counter = pickle.load(file)["counter"]
        else:
            self.counter = CreditCounter()
        return

    def save_counter(self):
        """
        Saves pickled file counter
        """
        file = open(self.file_path, "wb+")
        pickle.dump({"counter": self.counter}, file)
        return
    
    def google_search(self):
        """
        Iterates through provided prompts, querying Google API for each prompt, returning 10 URLs per request in JSON.
        :return: JSON results file, exception if out of credits.
        :rtype: JSON
        """
        # ensure every prompt can be queried or else report out of credits
        if self.counter.num_credits_remaining() < len(prompts):
            raise Exception("OUT OF CREDITS FOR EVERY PROMPT (WITHIN SEARCH)")

        results_JSON = []
        for prompt in prompts:
            # double check if there are enough credits remaining or not
            if not self.counter.credits_remaining():
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
        self.counter.decrement_credit_counter()
        self.save_counter()
        #call google custom search api
        service = build("customsearch", "v1", developerKey=self.api_key)
        res = service.cse().list(q=prompt, cx=self.cse_id, num=10).execute()
        #return the item section of the json response (removes irrelevent headers)
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

    # writing URLs to file for processing. one URL per line
    # write_to_file(r"Web-Scraping\APICallManagment\URLs.txt", URLs, True)

    def write_to_file(filename: str, text: list, multiple_lines=False):
        """
        :param filename: File to be written to.
        :param text: Text to be written to file.
        :param multiple_lines: Flag for outputting to multiple lines of the file.
        :returns (Written to File): text
        """
        file = open(filename, "a")
        for data in text:
            if str(data) != "":
                file.write(str(data))
                if multiple_lines:
                    file.write("\n")
        file.write("\n")
        file.close()

    # saving raw json returns to a file
    def save_raw_JSON_return(file_path: str, data: dict):
        # file_path = "Web-Scraping\APICallManagment\APIcallReturns.json"
        with open(file_path, "w") as json_file:
            json.dump(data, json_file, indent=4)
