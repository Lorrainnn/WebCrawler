#Part A: Word Frequencies
import sys

stop_word_list = [
    'a', 'about', 'above', 'after', 'again', 'against', 'all', 'am', 'an', 'and', 'any', 'are',
    "aren't", 'as', 'at', 'be', 'because', 'been', 'before', 'being', 'below', 'between', 'both',
    'but', 'by', "can't", 'cannot', 'could', "couldn't", 'did', "didn't", 'do', 'does', "doesn't",
    'doing', "don't", 'down', 'during', 'each', 'few', 'for', 'from', 'further', 'had', "hadn't",
    'has', "hasn't", 'have', "haven't", 'having', 'he', "he'd", "he'll", "he's", 'her', 'here',
    "here's", 'hers', 'herself', 'him', 'himself', 'his', 'how', "how's", 'i', "i'd", "i'll",
    "i'm", "i've", 'if', 'in', 'into', 'is', "isn't", 'it', "it's", 'its', 'itself', "let's", 'me',
    'more', 'most', "mustn't", 'my', 'myself', 'no', 'nor', 'not', 'of', 'off', 'on', 'once', 'only',
    'or', 'other', 'ought', 'our', 'ours', 'ourselves', 'out', 'over', 'own', 'same', "shan't", 'she',
    "she'd", "she'll", "she's", 'should', "shouldn't", 'so', 'some', 'such', 'than', 'that', "that's",
    'the', 'their', 'theirs', 'them', 'themselves', 'then', 'there', "there's", 'these', 'they',
    "they'd", "they'll", "they're", "they've", 'this', 'those', 'through', 'to', 'too', 'under',
    'until', 'up', 'very', 'was', "wasn't", 'we', "we'd", "we'll", "we're", "we've", 'were',
    "weren't", 'what', "what's", 'when', "when's", 'where', "where's", 'which', 'while', 'who',
    "who's", 'whom', 'why', "why's", 'with', "won't", 'would', "wouldn't", 'you', "you'd", "you'll",
    "you're", "you've", 'your', 'yours', 'yourself', 'yourselves'
]

def tokenize(text:str) -> list:
    """
    Reads in a text file and return a list of tokens

    :param file_path: Path to text file
    :return: List of tokens in that file

    Runtime Complexity: Linear (O(n)), where 'n' is depends on the size of file as
    total number of characters in the text file.
    The function iterates through each character in the text file once, performing
    constant-time operations (such as checking if a character is alphanumeric and
    appending to the tokens list).

    """

    tokens = []
    current_token = ''
    for char in text:
        # If the character is alphanumeric and in English, add it to the current token
        if char.isalnum() and ord(char) < 128:
            current_token += char
        # If the character is not alphanumeric and there's a current token, add it to the tokens list
        elif current_token:
            tokens.append(current_token.lower())
            current_token = ''
    # Add the last token if there's any
    if current_token.lower() not in stop_word_list:
        tokens.append(current_token)  # Convert token to lowercase
    return tokens


def computeWordFrequencies(tokens:list)->dict:
    """
    Compute word frequencies from a list of tokens.

    :param tokens: List of tokens
    :return: mapping each token to its frequency

    Runtime Complexity: Linear (O(n)), where 'n' is the number of tokens.
    The function iterates through each token in the list once. For each token,
    it performs a lookup in the word_frequency dictionary, which is an average
    constant-time operation due to dictionary hashing. Therefore, the overall
    time complexity is linear relative to the number of tokens.
    """
    word_frequency = {}
    for ele in tokens:
        if ele in word_frequency:
            #increase existing pair's frequency
            word_frequency[ele]+=1
        else:
            #update new pair's frequency
            word_frequency[ele] = 1
    return word_frequency


def print_out_token(word_frequency:dict)->None:
    """
    Print out tokens and their frequencies from a word frequency dictionary.

    :param: word_frequency: mapping each token with its number of occurences

    Runtime Complexity: O(n log n), where 'n' is the number of unique tokens.
    Since this function used sorted which has the time complexity of O(n log n), the overall time
    complexity is influenced even though we do iterate among all tokens in later iteration.
    """
    #first sorted by frequency decreasingly, then compare on character
    if not word_frequency:
        print(0)
    sorted_frequencies = sorted(word_frequency.items(), key = lambda x: (-x[1], x[0]))
    for token, count in sorted_frequencies:
        print(f"{token} - {count}")


if __name__ == '__main__':

    test = {"https://www.stat.uci.edu/": "\n\n\n\ndepartment of statistics - donald bren school of information & computer sciences \u2013 department of statistics - donald bren school of information & computer sciences\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\ndepartment of statistics - donald bren school of information & computer sciencesdepartment of statistics - donald bren school of information & computer sciences\nexplore\n\nchair\u2019s welcome\nwhat is statistics?\ncontact the department\ntutoring resources\n\n\nfaculty\n\nfaculty directory\njob opportunities\n\n\nresearch\ngraduate degrees\n\nm.s. & ph.d. in statistics\nmaster of data science\ncurrent course listings\ngraduate student directory\ninternships & employment opportunities\nemployers of uci statistics students\n\n\nundergraduate degrees\n\nb.s. in data science\nminor in statistics\ncurrent course listings\n\n\nnews & seminars\n\nnews\nseminars\n\n\ncenter for statistical consulting\n\n\n\n\n\n\n\n\nresearch\n\n\n\n\n\n\n\n\n\n\nfaculty directory\n\n\n\n\n\n\n\n\n\n\nm.s. & ph.d. in statistics\n\n\n\n\n\n\n\n\n\n\nuci launches new professional program: master of data science\n\n\n\n\n\n\n\n\n\n\n \n\n\n\n\n\n\n\n\n\n\n\nfor more than 20 years, uci\u2019s department of statistics has continued to grow as a leader in creating statistical methodology for use in data science applications. with an emphasis on research in statistical theory and interdisciplinary collaborations, the department has grown over the years to house the center for statistical consulting, providing statistical expertise through collaborative relationships with researchers across the campus and community, and was one of the first in the world to offer an undergraduate degree in data science. explore the statistics website to learn more about our accomplishments and how you can become part of our community.\n\u00a0\njob opportunitiesfor a listing of current academic positions open in the statistics department, visit the academic recruitment website.\n\u00a0\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\nlatest news\n\n\nuci\u2019s master of data science to launch part-time program in fall 2023\noctober 10, 2022\n\n\nnew faculty spotlight: statistics professor hengrui cai strives for real-world impact\nseptember 22, 2022\n\n\nsocal data science program off to a strong start\nseptember 21, 2022\n\n\nundergraduates conduct biostatistics research at new summer institute at uci\nseptember 13, 2022\n\n\nprofessors nan and gillen receive $1.8m grant to study statistical methods for alzheimer\u2019s research\naugust 29, 2022\n\n\n\n news archive\n\n\n \n\n\n\n\n\n\u00a9 2022 uc regents\nfeedback\nprivacy policy\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n"}
    a = tokenize(test["https://www.stat.uci.edu/"])
    print(len(a))




