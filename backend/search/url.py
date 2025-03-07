import re
from requests.exceptions import RequestException
from backend.web import get, build_url, USER_AGENT
from backend.search.types import SearchResult
from urllib.parse import urlparse


class NoRobotsFileException(Exception):
    def __init__(self, *args):
        super().__init__("Could not get robots.txt", *args)


class URL:
    def __init__(self, data: SearchResult) -> None:
        self.url = data["link"]
        self.title = data["title"]
        self.domain = data["displayLink"]
        if data["snippet"]:
            self.snippet = data["snippet"]

    def __str__(self) -> str:
        return self.url

    def __hash__(self) -> int:
        return hash(self.url)

    def __eq__(self, other: any) -> bool:
        if isinstance(other, URL):
            return str(self) == str(other)
        else:
            return False

    @property
    def path(self) -> str:
        return urlparse(self.url).path

    def get_raw_robots_rules(self) -> str:
        try:
            url = build_url(scheme="https", netloc=self.domain, path="robots.txt")
            response = get(url)
            if not response.ok or not response.headers.get("Content-Type").startswith(
                "text/plain"
            ):
                raise NoRobotsFileException()
        except RequestException:
            raise NoRobotsFileException()
        return response.text

    def get_robots_rules(self) -> list[list[str]]:
        raw_robots_rules = self.get_raw_robots_rules().strip().lower()
        # https://regex101.com/r/AuB3vK/2
        robots_rules = re.findall(
            r"user-agent:[\s\S]*?(?=\s*user-agent:|$)", raw_robots_rules
        )
        # https://regex101.com/r/6NpoBA/1
        return [re.split(r"\s*\r?\n\s*", rule) for rule in robots_rules]

    def can_crawl(self) -> bool:
        try:
            robots_rules = self.get_robots_rules()
        except NoRobotsFileException:
            return False
        print(self.url)
        print(robots_rules)
        allow = True
        for block in robots_rules:
            if not block.pop(0).endswith(("*", USER_AGENT.lower())):
                continue
            for rule in block:
                parsed_rule = rule.split(":", 1)
                if len(parsed_rule) != 2:
                    continue
                directive, path = parsed_rule
                path = urlparse(path).path
                if not path.endswith("/") and self.path != path:
                    continue
                if not self.path.startswith(path):
                    continue
                if directive == "allow":
                    allow = True
                elif directive == "disallow":
                    allow = False
        return allow
