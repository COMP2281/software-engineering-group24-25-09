from googleapiclient.discovery import build
import pprint
import os
import time

api_key_file_path = os.getenv("GOOGLE_API_KEY")
api_key_file = open(api_key_file_path, "r")
api_key = api_key_file.read()
my_cse_id = "12a15c6009e82483b"

#ensuring daily 100 query limit is not exceeded
prev_calls_file = open("Web-Scraping\APICallManagment\GoogleSearchQueryCounter.txt", "r")
prev_calls_file_contents = prev_calls_file.readlines()
prev_time = prev_calls_file_contents[0]
calls_remaining = prev_calls_file_contents[1]
prev_calls_file.close()
current_time = time.time()
time_elapsed = current_time-float(prev_time)

#if over a day has passed since the last time update, start the total call counter again
if time_elapsed >= 86400:
    calls_remaining = 100
    prev_time = current_time


#code sourced from 1st answer on StackOverflow by user mbdevpl on the page https://stackoverflow.com/questions/37083058/programmatically-searching-google-in-python-using-custom-search
def google_search(search_term, api_key, cse_id, **kwargs):
    if calls_remaining>0:
        calls_remaining-=1
        service = build("customsearch", "v1", developerKey=api_key)
        res = service.cse().list(q=search_term, cx=cse_id, **kwargs).execute()
        return res['items']
    else:
        print("ran out of API calls")
        return False

#results = google_search('"IBM" "University" article UK Ireland', api_key, my_cse_id, num=40)
#for result in results:
#    pprint.pprint(result)


#updating the query counter
prev_calls_file = open("Web-Scraping\APICallManagment\GoogleSearchQueryCounter.txt", "w")
#update to new date if appropriate
#update counter from number of calls
prev_calls_file.writelines([str(prev_time),"\n",str(calls_remaining)])
prev_calls_file.close()
