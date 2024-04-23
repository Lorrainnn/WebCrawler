import json
from urllib.parse import urlparse


class Calculation:
    def __init__(self):
        self.data={}
        self.unique_pages={}

    def extract_data(self):
        with open("temp_data.json", "r") as f:
            for line in f:
                # Parse the JSON object from the line
                data = json.loads(line)
                url = data["url"]
                content = data["content"]
                self.data[url] = content

    #question 1?
    def count_unique_page(self, urls):
        try:
            unique_pages = {}
            for ele in self.data.keys():
                subdomain = urlparse(ele)
                subdomain = subdomain.netloc
                if subdomain not in unique_pages:
                    unique_pages[subdomain] = 1
                elif subdomain in unique_pages:
                    unique_pages[subdomain] += 1
        except:
            pass

    def longest_page_and_common_word(self):
        pass