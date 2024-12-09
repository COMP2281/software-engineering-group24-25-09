import json
import os
import time

from googleapiclient.discovery import build


# updating the query counter
def update_query_counter(prev_time: time, calls_remaining: int):
    prev_calls_file = open(
        "Web-Scraping\APICallManagment\GoogleSearchQueryCounter.txt", "w"
    )
    prev_calls_file.writelines([str(prev_time), "\n", str(calls_remaining)])
    prev_calls_file.close()
    return


# getting the API key, held on Rosie's computer, directed to by the enviornment variable
api_key_file_path = os.getenv("GOOGLE_API_KEY")
api_key_file = open(api_key_file_path, "r")
api_key = api_key_file.read()
my_cse_id = "12a15c6009e82483b"

# ensuring daily 100 query limit is not exceeded
prev_calls_file = open(
    "Web-Scraping\APICallManagment\GoogleSearchQueryCounter.txt", "r"
)
prev_calls_file_contents = prev_calls_file.readlines()
prev_time = prev_calls_file_contents[0]
calls_remaining = int(prev_calls_file_contents[2])
prev_calls_file.close()
current_time = time.time()
time_elapsed = current_time - float(prev_time)

# if over a day has passed since the last time update, start the total call counter again
if time_elapsed >= 86400:
    update_query_counter(current_time, 100)


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
            '"IBM" "University" article UK Ireland', api_key, my_cse_id, num=10
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
