from requests import get
from copy import deepcopy
from bs4 import BeautifulSoup


def reset_file(filename: str):
    """
    :param filename: File to be reset.
    :returns Nothing: Resets a File by writing the empty string to it.
    """
    file = open(filename, "w")
    file.write("")
    file.close()

def write_to_file(filename: str, text: list, multiple_lines = False):
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

def remove_tags(HTML: str):
    """
    :param HTML: String input with HTML tags.
    :returns: String with all data between '<' and '>' deleted.
    """
    list_HTML = list(HTML)
    output_string = []
    collect = True
    for character in list_HTML:
        if character == "<":
            collect = False
        if collect == True:
            output_string.append(character)
        if character == ">":
            collect = True
    return "".join(output_string)


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

def find_headings(
    soup: BeautifulSoup, include_headings: tuple = ("h1", "h2", "h3", "h4", "h5", "h6")
):
    """
    :param soup: BeautifulSoup webpage
    :param include_headings: List of heading styles to find
    :returns List of BeautifulSoup heading tags
    """
    headings = []
    for heading in soup.find_all(include_headings):
        for attribute in list(heading.attrs.keys()):
            if attribute not in ("class", "id"):
                del heading[attribute]
        headings.append(deepcopy(heading))
    return headings


def find_and_strip_images(soup: BeautifulSoup):
    """
    Finds all images in the soup, clears the children, keeps only alt, src, and srcset attributes, and returns a list of references.
    :param soup: BeautifulSoup HTML Output.
    :returns: List of BeatifulSoup image tags.
    """
    images = []
    for image in soup.find_all("img"):
        image.clear()
        for attribute in list(image.attrs.keys()):
            if attribute not in ("alt", "src", "srcset"):
                del image[attribute]
        images.append(deepcopy(image))
    return images
