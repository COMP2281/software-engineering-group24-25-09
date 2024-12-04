from googleapiclient.discovery import build
import pprint
import os

api_key_file_path = os.getenv("GOOGLE_API_KEY")
api_key_file = open(api_key_file_path, "r")
api_key = api_key_file.read()
print(api_key)
my_cse_id = "12a15c6009e82483b"

def google_search(search_term, api_key, cse_id, **kwargs):
    service = build("customsearch", "v1", developerKey=api_key)
    res = service.cse().list(q=search_term, cx=cse_id, **kwargs).execute()
    return res['items']

results = google_search('"IBM" "University" article UK Ireland', api_key, my_cse_id, num=10)
for result in results:
    pprint.pprint(result)