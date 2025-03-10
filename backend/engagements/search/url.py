from urllib.parse import urlparse
from requests import RequestException
from engagements.web import build_url, USER_AGENT, get
from urllib.robotparser import RobotFileParser


class NoRobotsFileException(Exception):
    def __init__(self, *args):
        super().__init__("Could not get robots.txt", *args)


class URL:
    def __init__(self, url: str) -> None:
        self.url = url
        self.domain = urlparse(self.url).netloc

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
    def robots_file_url(self) -> str:
        return build_url(scheme="https", netloc=self.domain, path="robots.txt")

    def get_robots_lines(self) -> list[str]:
        try:
            response = get(self.robots_file_url)
        except RequestException:
            raise NoRobotsFileException()
        if not response.ok:
            raise NoRobotsFileException()
        return response.text.splitlines()

    def can_crawl(self) -> bool:
        robot_parser = RobotFileParser()
        try:
            lines = self.get_robots_lines()
        except NoRobotsFileException:
            return True
        robot_parser.parse(lines)
        return robot_parser.can_fetch(USER_AGENT, self.url)
