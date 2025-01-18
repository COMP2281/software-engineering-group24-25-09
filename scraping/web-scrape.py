from requests import get
from requests.exceptions import RequestException
from copy import deepcopy
from bs4 import BeautifulSoup


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
