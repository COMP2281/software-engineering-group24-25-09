from urllib.parse import urlunparse
import requests

USER_AGENT = "Durham_COMP2281_2425_9_EngagementTracker/1.0 (+https://github.com/COMP2281/software-engineering-group24-25-09) Requests/2.32.3"


def build_url(scheme: str, netloc: str, url="", path="", query="", fragment=""):
    # https://stackoverflow.com/a/15799706
    return str(urlunparse((scheme, netloc, url, path, query, fragment)))


def get(*args, **kwargs) -> requests.Response:
    if "headers" not in kwargs:
        kwargs["headers"] = {}
    kwargs["headers"]["User-Agent"] = USER_AGENT
    return requests.get(*args, **kwargs)
