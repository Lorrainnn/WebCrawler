import re
from urllib.parse import urlparse, urljoin
from bs4 import BeautifulSoup
import posixpath
import url_checker
import resp_tools
import content_check

# set used to avoid repeat visiting a website
visited = set()
# count the number of bytes in the longest pages
longest_number = 0
# the url of longest page
longest_url = ""
# dictionary used to count word in each page
WordCount = {}
# dictionary used to track domain, eg www.ics.uci.edu
domain = {}
# dictionary to avoid trap by using depth.
depth = {}
# similarity dictionary used to store all the other pages' hash and used to compare similarity.
finger_print = []
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
# file extensions that we should not scrap for
FILE_EXTENSIONS = (r".*\.(css|js|bmp|gif|jpe?g|ico"
                + r"|png|tiff?|mid|mp2|mp3|mp4"
                + r"|wav|avi|mov|mpeg|ram|m4v|mkv|ogg|ogv|pdf"
                + r"|ps|eps|tex|ppt|pptx|doc|docx|xls|xlsx|names"
                + r"|data|dat|exe|bz2|tar|msi|bin|7z|psd|dmg|iso"
                + r"|epub|dll|cnf|tgz|sha1"
                + r"|thmx|mso|arff|rtf|jar|csv"
                + r"|rm|smil|wmv|swf|wma|zip|rar|gz)$")

def printall():
    # print and write file
    print("Longest url: " + longest_url)
    print("longest_number: ", end = '')
    print(longest_number)
    print(dict(sorted(WordCount.items(), key = lambda single: (single[1], single[0]))))
    print(domain)
    with open("result.txt", "w") as file1:
        file1.write("longest_number: " + str(longest_number) + "\n")
        file1.write("longest_number: " + longest_url + "\n")
        for key,value in dict(sorted(WordCount.items(), key = lambda single: (single[1], single[0]))).items():
            file1.write(key + " ->" + str(value) + '\n')
        for key,value in domain.items():
            file1.write(key + " " + str(value) + '\n')


def scraper(url, resp):
    # used to detect for undefined certificate error
    try:
        links = extract_next_links(url, resp)
        return links
    except Exception as e:
        print(str(e))
        return []

def extract_next_links(url, resp) -> list:
    # Implementation required.
    # url: the URL that was used to get the page
    # resp.url: the actual url of the page
    # resp.status: the status code returned by the server. 200 is OK, you got the page. Other numbers mean that there was some kind of problem.
    # resp.error: when status is not 200, you can check the error here, if needed.
    # resp.raw_response: this is where the page actually is. More specifically, the raw_response has two parts:
    #         resp.raw_response.url: the url, again
    #         resp.raw_response.content: the content of the page!
    # Return a list with the hyperlinks (as strings) scrapped from resp.raw_response.content
    
    #check whether it has a valid link
    if resp.status != 200:
        return []

    # Keep track of depth. if depth > 10, we will not visit it anymore. 
    # Here is how depth works: if we have 5 websites: a b c and a has b link (a ->b)
    # b has c link (b ->c), then depth of a =1 , depth of b =1, depth of c =1
    global depth
    if resp.url not in depth:
        depth[resp.url] = 1
    elif depth[resp.url] > 10:
        return []
    
    # check the robots.txt
    parsed = urlparse(resp.url) # for later use
    if resp_tools.robot_checker(url, resp):
        return [] # stops running if it receives false    

    html_content = resp_tools.decode_content(resp)
    
    # get the text and compute the length to check. if length =0 or too big, we don't access the url
    soup = BeautifulSoup(html_content, 'html.parser')
    content = soup.get_text()
    length = int(resp.raw_response.headers.get("Content-Length", len(content)))
    if length == 0 or length >= 1000000:
        return []

    #update the longest_url_website
    global longest_number, longest_url, finger_print
    if length > longest_number:
        longest_number = length
        longest_url = resp.url

    finger_print = content_check.similar_check(content, finger_print)
    # get all the urls from the resp.url and initialize a return url_set
    links = soup.find_all('a')
    
    # update word count
    for word in re.findall(r'[A-Za-z0-9]+', content.lower()):
        if word in WordCount:
            WordCount[word] += 1
        else:
            WordCount[word] = 1

    # update domain
    single_domain = parsed.hostname
    if single_domain in domain:
        domain[single_domain] += 1
    else:
        domain[single_domain] = 1
    
    return list(process_links(links, url, resp))

def process_links(links, url, resp) -> set:
    url_set = set()
    #for all the url, we normalize it, check whether is_valid and add it to the return_list
    for link in links:
        href = link.get('href')

        #combine the relative url and base url to absolute url        
        abs_url = urljoin(url, href) if href else url
        parsed = urlparse(abs_url)

        #process scheme by lowercasing it and remove default host
        new_scheme = parsed.scheme.lower()
        new_netloc = parsed.netloc.lower()
        #if http has default:80 and:443, remove it using replace
        if new_scheme == "http":
            new_netloc = new_netloc.replace(":80", "")
        if new_scheme == "https":
            new_netloc = new_netloc.replace(":443", "")

        #sort the query
        new_url = content_check.query_cleaner(parsed, new_scheme, new_netloc, 
                                              posixpath.normpath(parsed.path)) # normalizes the path
        
        # check whether the new url is visited, if not,
        # add it to our return url_set and visited set. 
        # set the depth of new_url = depth of resp.url + 1
        global visited
        if new_url not in visited and is_valid(new_url):
            url_set.add(new_url)
            visited.add(new_url)
            depth[new_url] = depth[resp.url] + 1

    return url_set

def is_valid(url):
    # Decide whether to crawl this url or not. 
    # If you decide to crawl it, return True; otherwise return False.
    # There are already some conditions that return False.
    try:
        parsed = urlparse(url)
        # 直接换成一行，为什么我要写这么多if，这些真的有用吗？？？
        # 隔壁罗老师把这么多东西改成了一大个if 嘿嘿
        
        # Check whether scheme is http or https
        if parsed.scheme not in {"http", "https"}:
            return False

        if ((not url_checker.check_domain(url)) or # check the domain
            (not url_checker.check_length(url)) or 
            (not url_checker.check_repeating(url)) or # check repeating file to avoid trap like in calender
            (not url_checker.check_robots_txt(url)) or # check are we allowed to crawl
            (not url_checker.check_exclude_url(url))):
                return False

        # given code
        return not re.match(FILE_EXTENSIONS, parsed.path.lower())

    except TypeError:
        print ("TypeError for ", urlparse(url))
        raise

