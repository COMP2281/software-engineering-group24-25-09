from requests import get
from bs4 import BeautifulSoup

def reset_file():
    file = open("Web-Scraping\scrape.txt", "w")
    file.write("")
    file.close()

def write_to_file(text: list):
    file = open("Web-Scraping\scrape.txt", "a")
    for data in text:
        file.write(str(data))
    file.write("\n")
    file.close()

def remove_tags(HTML: str):
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
    Removes all escape characters

    https://stackoverflow.com/questions/8115261/how-to-remove-all-the-escape-sequences-from-a-list-of-strings
    """
    escapes = "".join([chr(char) for char in range(1,32)])
    translator = str.maketrans("", "", escapes)
    return text.translate(translator)

def get_website(URL: str):
    """
    @params
    URL: the URL of the website to be scraped

    Outputs BeautifulSoup html parsed text
    """
    try:
        return BeautifulSoup((get(URL)).text, "html.parser")
    except:
        pass #No Internet

def get_headers(soup, header_array):
    #  ["h1", "h2", "h3", "h4", "h5", "h6"]
    headers = []
    for header_type in header_array:
        headers.append(soup.find_all(header_type))
    for header_type in headers:
        for index in range(0, len(header_type)):
            header_type[index] = remove_escapes(remove_tags(str(header_type[index])))
    write_to_file(headers)

def get_images(soup):
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
    write_to_file(images)

def get_text(soup):
    paragraphs = soup.find_all("p")
    for index in range(0, len(paragraphs)):
        paragraphs[index] = remove_escapes(remove_tags(str(paragraphs[index])))
    write_to_file(paragraphs)

def scrape_website(URL: str):
    reset_file()
    soup = get_website(URL)
    get_images(soup)
    get_headers(soup, ["h1", "h2", "h3", "h4", "h5", "h6"])
    get_text(soup)

scrape_website("https://www.imperial.ac.uk/news/255517/phase-collaboration-sustainable-futures-between-imperial/")

# https://www.imperial.ac.uk/news/255517/phase-collaboration-sustainable-futures-between-imperial/

# Code for downloading the Images in the Future
# ---------------------------------------------
#import urllib.request
#def download_jpg(url, file_path, file_name):
#    full_path = file_path + file_name + ".jpg"
#    urllib.request.urlretrieve(url, full_path)
#url = "https://www.thenorthernecho.co.uk/resources/images/2440381.jpg"
#file_name = "image"
#download_jpg(url, r"C:\Users\Oscar\Documents\Github\software-engineering-group24-25-09\image", file_name )