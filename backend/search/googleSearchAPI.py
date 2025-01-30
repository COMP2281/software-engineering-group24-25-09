import json
import os
import time
from dotenv import load_dotenv, find_dotenv
import pickle
from searchPrompts import prompts
load_dotenv(find_dotenv())
# loading environment variables for API
api_key = os.getenv("GOOGLE_API_KEY")
cse_id = os.getenv("GOOGLE_CSE_ID")

print(api_key)
print(cse_id)
# ensuring daily 100 query limit is not exceeded
# prev_calls_file = open(
#     "Web-Scraping\APICallManagment\GoogleSearchQueryCounter.txt", "r"
# )
# prev_calls_file_contents = prev_calls_file.readlines()
# prev_time = prev_calls_file_contents[0]
# calls_remaining = int(prev_calls_file_contents[2])
# prev_calls_file.close()
# current_time = time.time()
# time_elapsed = current_time - float(prev_time)

# # if over a day has passed since the last time update, start the total call counter again
# if time_elapsed >= 86400:
#     update_query_counter(current_time, 100)
from googleapiclient.discovery import build

class CreditCounter:
    def __init__(self):
        self.credits = 100
        self.time = time.time()

    def num_credits_remaining(self):
        return self.credits

    def credits_remaining(self):
        self.update_counter()
        if self.credits > 0:
            return True
        else:
            return False
    
    def update_counter(self):
        # if over a day has passed since the last time update, start the total call counter again
        current_time = time.time()
        time_elapsed = current_time - self.time
        if time_elapsed >= 86400:
            self.time = current_time
            self.reset_credits()
        return

    def reset_credits(self):
        self.credits = 100
        return

    def decrement_credit_counter(self):
        if self.credits_remaining():
            self.credits -= 1
        else:
            raise Exception("OUT OF SEARCH CREDITS (WITHIN CREDITCOUNTER)")
        return

class Search:
    def __init__(self, api_key: str, cse_id: str, data_path: str):
        self.api_key = api_key
        self.cse_id = cse_id
        self.file_path = data_path + "counter.pickle"
        self.counter = None
        self.load_counter()
        self.save_counter()
        
    # checks if counter file exists, boolean response
    def file_exists(self):
        return os.path.isfile(self.file_path)
    
    # loads in pickle counter file
    def load_counter(self):
        if self.file_exists():
            file = open(self.file_path, "rb+")
            self.counter = pickle.load(file)["counter"]
        else:
            self.counter = CreditCounter()
        return

    # saves pickeled file counter
    def save_counter(self):
        file = open(self.file_path, "wb+")
        pickle.dump({"counter":self.counter}, file)
        return
    
    # will go through the promps provided, queries the google api for each query, returning 10
    # URLS each time is messy JSON
    # then calls the private get URLs method to extract these URLs and return them as a list
    def google_search(self):
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
        
        URLs = self.extract_URLs_from_JSON(results_JSON)
        print(URLs)
        return URLs


    def use_google_api(self, prompt: str):
        # edit the counter for the outgoing api request
        self.counter.decrement_credit_counter()
        self.save_counter()
        #call google custom search api
        service = build("customsearch", "v1", developerKey=self.api_key)
        res = service.cse().list(q=prompt, cx=self.cse_id, num=10).execute()
        #return the item section of the json response (removes irrelevent headers)
        return res["items"]

    def extract_URLs_from_JSON(self,json_data):
        # extracting URLs from the returned JSON of found sites
        URLs = []
        for result in json_data:
            URLs.append(result["link"])
        return URLs

#FOR TESTING WITHOUT USING CREDITS
# def use_test_api_results():
#     file_path = "Web-Scraping\APICallManagment\APIcallReturns.json"
#     with open(file_path, "r") as json_file:
#         results = json.load(json_file)
#     return results


search = Search(api_key, cse_id, "../data/")
print(search.counter.credits)
#search.google_search()