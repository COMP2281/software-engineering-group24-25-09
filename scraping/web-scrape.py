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

def get_website(URL: str):
    """
    :param URL: The URL of the website to be scraped.
    :returns: BeautifulSoup html parsed text.
    """
    try:
        return BeautifulSoup((get(URL)).text, "html.parser")
    except:
        pass #No Internet


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


def get_text(filename: str, soup: str):
    """
    :param filename: Name of file to write to.
    :param soup: BeautifulSoup HTML Output.
    :returns (Written to File): Array of Paragraph Text from given HTML.
    """
    paragraphs = soup.find_all("p")
    for index in range(0, len(paragraphs)):
        paragraphs[index] = remove_escapes(remove_tags(str(paragraphs[index])))
    write_to_file(filename, paragraphs, True)

def scrape_website(URL: str, filename: str):
    """
    :param URL: URL of Website to Scrape from.
    :param filename: Name of file to write to.
    :returns (Written to File): All Scraped data from given Website URL.
    """
    reset_file(filename)
    write_to_file(filename, [URL])
    soup = get_website(URL)
    get_images(filename, soup)
    get_headers(filename, soup)
    get_text(filename, soup)

def scrape_input(input_filename: str, output_folder: str):
    """
    :param input_filename: Filename of Input.
    :param output_folder: Folder to output .txt output files to.
    :returns (Written to Folder): Iterates through a .txt list of URLs and Scrapes data from each.
    """
    file = open(input_filename, "r")
    for index, URL in enumerate(file):
        try:
            scrape_website(URL, str(str(output_folder) + "\\" + str(index) + ".txt"))
        except:
            pass
    file.close()

scrape_input("Web-Scraping\input.txt", "Web-Scraping\Output")

# Code for downloading the Images in the Future
# ---------------------------------------------
#import urllib.request
#def download_jpg(url, file_path, file_name):
#    full_path = file_path + file_name + ".jpg"
#    urllib.request.urlretrieve(url, full_path)
#url = "https://www.thenorthernecho.co.uk/resources/images/2440381.jpg"
#file_name = "image"
#download_jpg(url, r"C:\Users\Oscar\Documents\Github\software-engineering-group24-25-09\image", file_name )