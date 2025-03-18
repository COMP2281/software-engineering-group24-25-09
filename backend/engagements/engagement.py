from urllib.parse import urljoin
from engagements.llm import LLM
from engagements.engagement_data import EngagementData
from engagements.engagement_data_manager import EngagementDataManager
from engagements.pages import Page, PageManager
from bs4 import BeautifulSoup
from engagements.slideshow import EngagementSlide


class Engagement:
    def __init__(
        self,
        engagement_data_manager: EngagementDataManager,
        llm: LLM,
        data: EngagementData | Page,
    ) -> None:
        """
        Set references to engagement_manager and llm.
        If given a Page then create new EngagementData.
        :param engagement_data_manager: EngagementDataManager instance.
        :param llm: LLM instance.
        :param data: EngagementData or Page to start new EngagementData.
        """
        self.engagement_data_manager = engagement_data_manager
        self.llm = llm
        if isinstance(data, EngagementData):
            self.data = data
        elif isinstance(data, Page):
            self.data = EngagementData(self.llm, data)

    def get_slug(self) -> str:
        """
        Get the slug identifying the engagement.
        :return: Slug.
        """
        return self.data.get_slug()

    def get_source_urls(self) -> set[str]:
        """
        Get all URLs for the engagement sources.
        :return: Set of source URLs.
        """
        return self.data.get_source_urls()

    def get_data(self) -> EngagementData:
        """
        Get the EngagementData object.
        :return: EngagementData.
        """
        return self.data

    def add_source_url(self, url: str) -> None:
        """
        Add a new source URL to the engagement.
        :param url: Source URL.
        """
        self.data.add_source_url(url)
        self.engagement_data_manager.save_data()

    def get_page_manager(self) -> PageManager:
        """
        Get the PageManager instance.
        :return: PageManager instance.
        """
        return self.engagement_data_manager.get_page_manager()

    def get_source(self, url: str) -> Page:
        """
        Get a source that belongs to the engagement.
        :param url: Page URL.
        :return: Page.
        """
        if url not in self.data.get_source_urls():
            raise Exception(
                f"Source URL {url} not found in Engagement {self.get_slug()}"
            )
        return self.get_page_manager().get_page(url)

    def get_sources(self) -> list[Page]:
        """
        Get all sources that belong to the engagement.
        :return: List of Pages.
        """
        pages = []
        for url in self.data.get_source_urls():
            page = self.get_source(url)
            pages.append(page)
        return pages

    def get_images(self) -> list[BeautifulSoup]:
        """
        Get the images from all pages. Each image has the "alt" attribute and either "src" or "srcset" attribute.
        :return: List of images.
        """
        images = []
        for url in self.get_source_urls():
            new_images = self.get_page_manager().get_page(url).get_images()
            for image in new_images:
                image_url = image.get("src")
                if image_url is not None:
                    if not image_url.endswith((".png", ".jpg", ".jpeg")):
                        continue
                    if image_url.startswith("/"):
                        image_url = urljoin(url, image_url)
                    image["src"] = image_url
                    images.append(image)
        return images

    def get_title(self) -> str:
        """
        Get the engagement title.
        :return: Title.
        """
        return self.data.get_title()

    def get_summary(self) -> list[str]:
        """
        Get a summary of the engagement in short sentences.
        :return: List of sentences.
        """
        sentences = []
        for page in self.get_sources():
            sentences += self.llm.summarise(page)
        return sentences

    def get_employees(self) -> set[str]:
        """
        Get a list of employees involved in the engagement.
        :return: List of employees.
        """
        employees = set()
        for page in self.get_sources():
            employees = employees.union(self.llm.employees(page))
        return employees

    def generate_slide(self) -> None:
        slide = (
            EngagementSlide()
            .set_title(self.get_title())
            .set_summary(self.get_summary())
            .set_employees(list(self.get_employees()))
        )
        images = self.get_images()
        print(images)
        if len(images) > 0:
            slide.set_image(images[0])

        self.data.add_slide(slide)
        self.engagement_data_manager.save_data()

    def get_slide(self) -> EngagementSlide:
        return self.data.get_slide()
