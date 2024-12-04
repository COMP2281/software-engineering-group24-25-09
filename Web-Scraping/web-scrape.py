from requests import get
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

def remove_escapes(text :str):
    """
    :param text: String with escape characters.
    :returns: String with all escape characters removed.
    
    Credit: https://stackoverflow.com/questions/8115261/how-to-remove-all-the-escape-sequences-from-a-list-of-strings
    """
    escapes = "".join([chr(char) for char in range(1,32)])
    translator = str.maketrans("", "", escapes)
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

def get_headers(filename: str, soup: str, header_array: list = ["h1", "h2", "h3", "h4", "h5", "h6"]):
    """
    :param filename: Name of file to write to.
    :param soup: BeautifulSoup HTML Output.
    :param header_array: List of all header styles to be scraped.
    :returns (Written to File): 2D Array of Headers from given HTML, h[index-1].
    """
    headers = []
    for header_type in header_array:
        headers.append(soup.find_all(header_type))
    for header_type in headers:
        for index in range(0, len(header_type)):
            header_type[index] = remove_escapes(remove_tags(str(header_type[index])))
    write_to_file(filename, headers)

def get_images(filename: str, soup: str):
    """
    :param filename: Name of file to write to.
    :param soup: BeautifulSoup HTML Output.
    :returns (Written to File): 2D Array of Images from given HTML; index 0:alt text, index 1:src.
    """
    image_objects = soup.find_all("img")
    images = []
    for image in image_objects:
        try:
            images.append([image['alt'], image['src']])
        except:
            try:
                srcset = image['srcset']
                srcset = srcset.split(" ")
                images.append([image['alt'], srcset[0]])
            except:
                pass
    write_to_file(filename, images)

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
    index = 0
    file = open(input_filename, "r")
    for URL in file:
        try:
            URL = remove_escapes(URL)
            scrape_website(URL, str(str(output_folder) + "\\" + str(index) + ".txt"))
        except:
            pass
        index += 1
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