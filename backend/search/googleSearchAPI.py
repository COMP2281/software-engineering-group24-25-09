import json
import os
import time
from dotenv import load_dotenv
#load_dotenv()
# # loading environment variables for API
# self.api_key = os.getenv("GOOGLE_API_KEY")
# self.cse_id = os.getenv("GOOGLE_CSE_ID")

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
            raise Exception("OUT OF SEARCH CREDITS")
        return

class Search:
    def __init__(self, api_key: str, cse_id: str):
        self.api_key = api_key
        self.cse_id = cse_id

    # updating the query counter
    def update_query_counter(prev_time: time, calls_remaining: int):
        prev_calls_file = open(
            "Web-Scraping\APICallManagment\GoogleSearchQueryCounter.txt", "w"
        )
        prev_calls_file.writelines([str(prev_time), "\n", str(calls_remaining)])
        prev_calls_file.close()
        return
    


    # code sourced from 1st answer on StackOverflow by user mbdevpl on the page https://stackoverflow.com/questions/37083058/programmatically-searching-google-in-python-using-custom-search
    def google_search(search_term, api_key, cse_id, **kwargs):
        service = build("customsearch", "v1", developerKey=api_key)
        res = service.cse().list(q=search_term, cx=cse_id, **kwargs).execute()
        return res["items"]


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


    def use_test_api_results():
        file_path = "Web-Scraping\APICallManagment\APIcallReturns.json"
        with open(file_path, "r") as json_file:
            results = json.load(json_file)
        return results


    def use_google_api(prev_time: time, calls_remaining: int):
        if calls_remaining <= 0:
            print("no remaining calls- using test data")
            return use_test_api_results()
        else:
            calls_remaining -= 1
            results = google_search(
                '"IBM" interacts with "University" article UK Ireland', api_key, cse_id, num=10
            )
            update_query_counter(prev_time, calls_remaining)
            return results


    def extract_URLs_from_JSON(json_data):
        # extracting URLs from the returned JSON of found sites
        URLs = []
        for result in json_data:
            metatags = result["pagemap"]["metatags"]
            try:
                location = metatags[0]["geo.country"]
            except:
                location = False
            # google returns location eg. GB, US- could be used to narrow down sites?
            if location:
                print(location)
            else:
                print("no location given ")
            URLs.append(result["link"])
        return URLs


    results = use_google_api(prev_time, calls_remaining)
    URLs = extract_URLs_from_JSON(results)
    # writing URLs to file for processing. one URL per line
    write_to_file(r"Web-Scraping\APICallManagment\URLs.txt", URLs, True)


    # saving raw json returns to a file
    def save_raw_JSON_return(file_path: str, data: dict):
        # file_path = "Web-Scraping\APICallManagment\APIcallReturns.json"
        with open(file_path, "w") as json_file:
            json.dump(data, json_file, indent=4)
