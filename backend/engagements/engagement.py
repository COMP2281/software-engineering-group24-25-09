class Engagement:
    def __init__(self, slug):
        self.slug = slug
        self.source_urls = set()
        self.summary = None

    def add_page_url(self, url):
        self.source_urls.add(url)

    def get_page_urls(self):
        return self.source_urls
