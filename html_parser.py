from html.parser import HTMLParser
from urllib import parse

class Parser(HTMLParser):
    def __init__(self, base_url):
        super().__init__()
        self.base_url = base_url
        self.links = set()

    def handle_starttag(self, tag, attrs):
        if tag == 'a':
            for (attribute, value) in attrs:
                if attribute == 'href':
                    url = parse.urljoin(self.base_url, value)
                    # print(url)
                    self.links.add(url)

    def page_links(self):
        return self.links