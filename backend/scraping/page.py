from requests import get
from requests.exceptions import RequestException
from copy import deepcopy
from bs4 import BeautifulSoup
import re


def remove_control_characters(text: str):
    """
    Remove control characters x01 to x1f, excluding whitespace characters.
    TODO: determine if function is necessary; there are many more control characters to consider.
        https://en.wikipedia.org/wiki/List_of_Unicode_characters
        https://stackoverflow.com/a/19016117
    :param text: String containing control characters.
    :return: String with control characters removed.
    :rtype: str

    Credit: https://stackoverflow.com/questions/8115261/how-to-remove-all-the-escape-sequences-from-a-list-of-strings
    """
    control_characters = set([chr(char) for char in range(1, 32)])
    keep_control_characters = {"\t", "\n", "\r"}
    control_characters -= keep_control_characters
    control_characters_string = "".join(list(control_characters))
    translator = str.maketrans("", "", control_characters_string)
    return text.translate(translator)


def get_page_soup(url: str):
    """
    Get web page as element with control characters and comments removed.
    :param url: URL of page to get.
    :return: Element.
    :rtype: BeautifulSoup
    """
    try:
        html = get(url).text
    except RequestException as e:
        raise Exception(f"Failed to get {url}:\n{e}")

    html = remove_control_characters(html)
    return BeautifulSoup(html, "html.parser")


def remove_elements(
    soup: BeautifulSoup,
    tags: tuple[str, ...],
):
    """
    Remove all elements from soup with given tags.
    :param soup: BeautifulSoup object.
    :param tags: Tuple of element tags.
    :return: BeautifulSoup object with elements removed.
    :rtype: BeautifulSoup
    """
    for element in soup.find_all(tags):
        element.extract()


def strip_element(element: BeautifulSoup, keep_attributes: tuple[str, ...]):
    """
    Remove attributes from an element.
    :param element: Element to strip.
    :param keep_attributes: Tuple of element attributes to keep.
    :return: Element with attributes removed.
    :rtype: BeautifulSoup
    """
    for attribute in list(element.attrs.keys()):
        if attribute not in keep_attributes:
            del element[attribute]
    return element


def strip_image(image: BeautifulSoup):
    """
    Remove unnecessary attributes and all children from an image.
    :param image: Image element.
    :return: Stripped image element.
    :rtype: BeautifulSoup
    """
    image.clear()
    return strip_element(image, ("alt", "src", "srcset"))


class Page:
    def update(self):
        """
        Get the latest version of the page and update self.
        """
        page = get_page_soup(self.url)
        body = page.find("body")
        self.body = body

    def __init__(self, url: str):
        """
        Set URL and update self.
        :param url: Webpage URL.
        """
        self.body = None
        self.url = url
        self.update()

    def get_content(self):
        """
        Get a copy of the main content from the page.
        :return: Body element without unnecessary children.
        :rtype: BeautifulSoup
        """
        content = deepcopy(self.body)
        remove_elements(
            content,
            (
                "script",
                "style",
                "head",
                "meta",
                "header",
                "footer",
                "noscript",
                "footer",
            ),
        )
        return content

    def get_flat_content(self):
        """
        Get a soup containing all headings, paragraphs, and images in the main content without any nesting.
        :return: BeautifulSoup object.
        :rtype: BeautifulSoup
        """
        body = self.get_content()
        content = BeautifulSoup()
        for element in body.find_all(("h1", "h2", "h3", "h4", "h5", "h6", "p", "img")):
            content.append(deepcopy(element))
        return content

    def get_markdown_content(self):
        """
        Get a Markdown representation of the main content.
        :return: Main content formatted in Markdown.
        :rtype: str
        """
        content = self.get_flat_content()

        # replace images with ![alt text]()
        # URLs aren't needed for the LLM
        for image in content.find_all("img"):
            alt_text = image.get("alt", "")
            image.replace_with(f"\n![{alt_text}]()\n")

        # prefix h1 text with #, h2 with ##, h3 with ###, etc.
        for i in range(1, 7):
            for h in content.find_all("h" + str(i)):
                text = h.get_text()
                h.replace_with(f"\n{"#" * i} {text}\n")

        # ensure double newlines before and after paragraph text
        for p in content.find_all("p"):
            text = p.get_text()
            p.replace_with(f"\n{text}\n")

        # any repeated newlines are clipped to a maximum of 2
        # https://regex101.com/r/cIfG7c/1
        return re.sub(r"\n\n\n+", "\n\n", content.get_text()).strip()

    def get_images(self):
        """
        Get a list of all images in the page.
        :return: A list of stripped image elements.
        :rtype: list[BeautifulSoup]
        """
        images = []
        for image in self.body.find_all("img"):
            image = deepcopy(image)
            image = strip_image(image)
            images.append(image)
        return images
