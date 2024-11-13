from requests import get
from bs4 import BeautifulSoup

def get_all_images(URL: str):
    try:
        page = get(URL)
        html = page.text
        soup = BeautifulSoup(html, "html.parser")
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
        file = open("Web-Scraping\images.txt", "w")
        for image in images:
            file.write(str(image))
        file.close
    except:
        pass #No Internet

get_all_images("https://www.imperial.ac.uk/news/255517/phase-collaboration-sustainable-futures-between-imperial/")


# Code for downloading the Images in the Future
# ---------------------------------------------
#import urllib.request
#def download_jpg(url, file_path, file_name):
#    full_path = file_path + file_name + ".jpg"
#    urllib.request.urlretrieve(url, full_path)
#url = "https://www.thenorthernecho.co.uk/resources/images/2440381.jpg"
#file_name = "image"
#download_jpg(url, r"C:\Users\Oscar\Documents\Github\software-engineering-group24-25-09\image", file_name )