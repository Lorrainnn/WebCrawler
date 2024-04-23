import json
from PartA import *
from urllib.parse import urlparse


class Calculation:
    def __init__(self):
        self.data={}

        #Q1
        self.unique_page = 0

        #Q2
        self.longest_page_url = ""
        self.longest_page_len = 0

        #Q3
        self.frequency = {}

        # Q4
        self.domains = {}

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
        self.unique_page = len(self.data)


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
        self.frequency = sorted(self.frequency.items(), key = lambda x: (-x[1], x[0]))


    #question 4?
    def count_subdomain(self):
        try:
            for ele in self.data.keys():
                subdomain = urlparse(ele)
                subdomain = subdomain.netloc
                if subdomain not in self.domains:
                    self.domains[subdomain] = 1
                elif subdomain in self.domains:
                    self.domains[subdomain] += 1
        except:
            pass

    def generate_output(self):
        self.extract_data()
        self.count_unique_pages()
        self.count_subdomain()

        with open('reportQ1.txt', 'w', encoding = "utf-8") as w:
            w.write(f'Number of unique pages: {self.unique_page}\n')
            for key in self.data.keys():
                w.write(key)
                w.write('\n')

        with open('reportQ2.txt', 'w', encoding = "utf-8") as w:
            w.write(f"Longest page: {self.longest_page_url}\n")
            w.write(f"Number of words: {self.longest_page_len}\n")
            w.write(self.data[self.longest_page_url])

        with open('reportQ3.txt', 'w', encoding = "utf-8") as w:
            for token, count in self.frequency[0:50]:
                w.write(f"{token} - {count}\n")

        with open('reportQ4.txt', 'w', encoding = "utf-8") as w:
            for domain, num in self.domains:
                w.write(f"{domain} - {num}\n")






if __name__=="__main__":
    generator = Calculation()
    generator.generate_output()