import re
from bs4 import BeautifulSoup
from urllib.parse import urljoin
from engagements.llm import LLM
from engagements.pages import Page
from engagements.slideshow import EngagementSlide


class EngagementData:
    @staticmethod
    def title_to_slug(title: str) -> str:
        """
        Convert a title string into a lowercase, alphanumeric, underscored slug.
        :param title: Title.
        :return: Slug.
        """
        title = title.strip().lower()
        # replace variable length spaces with single underscores
        title = re.sub(r" +", "_", title)
        # remove any character that is not alphanumeric or an underscore
        return re.sub("[^a-z0-9_]", "", title)

    def __init__(self, llm: LLM, page: Page) -> None:
        """
        Initialise with one source URL and generate a slug from the source.
        :param llm: LLM instance.
        :param page: Page.
        """
        self.source_urls = {page.get_url()}
        self.title = llm.title(page)
        self.slug = self.title_to_slug(self.title)
        self.create_summary(llm, page)
        self.create_employees(llm, page)
        self.create_images(page)
        self.slide = None

    def get_slug(self) -> str:
        """
        Get the slug identifying the engagement.
        :return: Slug.
        """
        return self.slug

    def create_summary(self, llm: LLM, page: Page) -> None:
        self.summary = llm.summarise(page)

    def get_summary(self) -> list[str]:
        return self.summary

    def create_employees(self, llm: LLM, page: Page) -> None:
        """
        Get a list of employees involved in the engagement.
        :return: List of employees.
        """
        self.employees = llm.employees(page)

    def get_employees(self) -> set[str]:
        return self.employees

    def create_images(self, page: Page) -> None:
        """
        Get the images from all pages. Each image has the "alt" attribute and either "src" or "srcset" attribute.
        :return: List of images.
        """
        self.images = []
        new_images = page.get_images()
        for image in new_images:
            image_url = image.get("src")
            if image_url is not None:
                if not image_url.endswith((".png", ".jpg", ".jpeg")):
                    continue
                if image_url.startswith("/"):
                    image_url = urljoin(page.get_url(), image_url)
                image["src"] = image_url
                self.images.append(image)

    def get_images(self) -> list[BeautifulSoup]:
        return self.images

    def get_title(self) -> str:
        """
        Get the title of the engagement.
        :return: Title.
        """
        return self.title

    def get_source_urls(self) -> set[str]:
        """
        Get all URLs for the engagement sources.
        :return: Set of source URLs.
        """
        return self.source_urls

    def add_source_url(self, url: str) -> None:
        """
        Add a new source URL to the engagement.
        :param url: Source URL.
        """
        self.source_urls.add(url)

    def add_slide(self, slide: EngagementSlide) -> None:
        """
        Add a slide to the engagement.
        :param slide: Slide.
        """
        self.slide = slide

    def get_slide(self) -> EngagementSlide:
        """
        Get the slide of the engagement.
        :return: Slide.
        """
        return self.slide
