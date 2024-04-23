import json
from PartA import *
from urllib.parse import urlparse


class Calculation:
    def __init__(self):
        self.data={}
        self.unique_pages={}

        self.longest_page_url = ""
        self.longest_page_len = 0
        self.frequency = {}

    def extract_data(self):
        with open("temp_data.json", "r") as f:
            for line in f:
                # Parse the JSON object from the line
                data = json.loads(line)
                url = data["url"]
                content = data["content"]
                self.data[url] = content

    #question 1
    def count_unique_pages(self):
        return len(self.data)


    #Question 2,3?
    def longest_page_and_50_common_word(self):
        for pair in self.data.items():
            tokens = tokenize(pair[1])
            length = len(tokens)
            if length>self.longest_page_len:
                self.longest_page_url = pair[0]
                self.longest_page_len = length

            words = computeWordFrequencies(tokens)
            self.frequency.update(words)


    #question 4?
    def count_subdomain(self):
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



if __name__=="__main__":
    pass