from scraping import PageManager
from data.urls import urls

page_manager = PageManager("data/pages.pickle")

# for url in urls:
#     page_manager.add_page(url)

print(page_manager.pages)
