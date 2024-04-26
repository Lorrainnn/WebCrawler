import json
from PartA import *
from urllib.parse import urlparse

# word that does not count
stop_word = {
    "a", "about", "above", "after", "again", "against", "all", "am", "an", "and",
    "any", "are", "aren't", "as", "at", "be", "because", "been", "before", "being",
    "below", "between", "both", "but", "by", "can't", "cannot", "could", "couldn't",
    "did", "didn't", "do", "does", "doesn't", "doing", "don't", "down", "during",
    "each", "few", "for", "from", "further", "had", "hadn't", "has", "hasn't", "have",
    "haven't", "having", "he", "he'd", "he'll", "he's", "her", "here", "here's", "hers",
    "herself", "him", "himself", "his", "how", "how's", "i", "i'd", "i'll", "i'm", "i've",
    "if", "in", "into", "is", "isn't", "it", "it's", "its", "itself", "let's", "me", "more",
    "most", "mustn't", "my", "myself", "no", "nor", "not", "of", "off", "on", "once", "only",
    "or", "other", "ought", "our", "ours", "ourselves", "out", "over", "own", "same", "shan't",
    "she", "she'd", "she'll", "she's", "should", "shouldn't", "so", "some", "such", "than", "that",
    "that's", "the", "their", "theirs", "them", "themselves", "then", "there", "there's", "these",
    "they", "they'd", "they'll", "they're", "they've", "this", "those", "through", "to", "too",
    "under", "until", "up", "very", "was", "wasn't", "we", "we'd", "we'll", "we're", "we've",
    "were", "weren't", "what", "what's", "when", "when's", "where", "where's", "which", "while",
    "were", "weren't", "wha", "what's", "when", "when's", "where", "where's", "which", "while",
    "who", "who's", "whom", "why", "why's", "with", "won't", "would", "wouldn't", "you", "you'd",
    "you'll", "you're", "you've", "your", "yours", "yourself", "yourselves"
}

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
                url = list(data.keys())[0]  # Convert dict_keys object to list and get the first (and only) key
                content = data[url]

                self.data[url] = content

    #question 1
    def count_unique_pages(self):
        self.unique_page = len(self.data)


    #Question 2,3
    def longest_page_and_50_common_word(self):
        for key, value in self.data.items():
            tokens = tokenize(value)
            length = len(tokens)

            if length>self.longest_page_len:
                self.longest_page_url = key
                self.longest_page_len = length

            words = computeWordFrequencies(tokens)

            for key_w in words:
                # If the key is present in dict1, add the corresponding values
                if key_w in self.frequency:
                    self.frequency[key_w] += words[key_w]
                # If the key is not present in dict1, add it with its value
                else:
                    self.frequency[key_w] = words[key_w]

            self.frequency.update(words)



    #question 4
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
        self.longest_page_and_50_common_word()

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
            top_50 = sorted(self.frequency.items(), key=lambda x: x[1], reverse=True)[:50]
            for token, count in top_50:
                w.write(f"{token} - {count}\n")

        with open('reportQ4.txt', 'w', encoding = "utf-8") as w:
            for domain, num in self.domains.items():
                w.write(f"{domain} - {num}\n")






if __name__=="__main__":
    generator = Calculation()
    generator.generate_output()