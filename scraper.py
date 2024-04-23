import re
import json
from urllib.parse import urlparse
from bs4 import BeautifulSoup
import posixpath
from urllib.parse import urlunparse
from urllib.parse import urljoin
from urllib.parse import unquote, urlencode, parse_qsl
import urllib.robotparser



def scraper(url, resp):
    links = extract_next_links(url, resp)
    return links

def extract_next_links(url, resp):
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
    if not resp.status == 200:
        return []

    #Find all the url in the html file
    html_content = resp.raw_response.content
    soup = BeautifulSoup(html_content, 'html.parser')
    links = soup.find_all('a')
    url_set = set()

    #for all the url, we normalize it, check whether is_valid and add it to the return_list
    for link in links:
        href = link.get('href')
        #remove fragment
        if href is not None:
            href = href.split('#')[0]

        #combine the relative url and base url to absolute url
        abs_url = urljoin(resp.url, href) if href else resp.url
        parsed = urlparse(abs_url)

        #process scheme by lowercase it and remove default host
        new_scheme = parsed.scheme.lower()
        new_netloc = parsed.netloc.lower()

        #if http has default:80 and:443, remove it using replace
        if new_scheme == "http":
            new_netloc = new_netloc.replace(":80", "")
        if new_scheme == "https":
            new_netloc = new_netloc.replace(":443", "")

        # normalize the path
        new_path = posixpath.normpath(parsed.path)

        #sort the query
        #use unquote to decode the query
        decoded_query = unquote(parsed.query)
        #make a list consisting of [key, value] pair
        key_value_querylist = parse_qsl(decoded_query, keep_blank_values = True)
        #sort the key_value_list
        sorted_query = sorted(key_value_querylist, key = lambda single:single[0])
        #encode it back to query
        new_query = urlencode(sorted_query,doseq = True)


        #combine all the modified scheme, netloc, path, query with removing fragment to the new url
        new_url = urlunparse((new_scheme, new_netloc, new_path, parsed.params, new_query, ""))

        # check whether the url is valid
        if is_valid(new_url):
            url_set.add(new_url)

        with open("temp_data.json","a") as f:
            parser = BeautifulSoup(resp.raw_response.content, 'html.parser')
            data = {new_url:parser.get_text().lower()}
            json.dump(data, f)
            f.write("\n")

    return list(url_set)

def is_valid(url):
    # Decide whether to crawl this url or not. 
    # If you decide to crawl it, return True; otherwise return False.
    # There are already some conditions that return False.
    try:
        parsed = urlparse(url)

        #check whether scheme is http or https
        if parsed.scheme not in {"http", "https"}:
            return False

        #check the domain
        if not check_domain(url):
            return False

        #check irrelevant file to avoid trap like in calender
        if not check_irrelevant(url):
            return False

        #check are we allowed to crawl
        if not check_robots_txt(url):
            return False

        #given code
        return not re.match(
            r".*\.(css|js|bmp|gif|jpe?g|ico"
            + r"|png|tiff?|mid|mp2|mp3|mp4"
            + r"|wav|avi|mov|mpeg|ram|m4v|mkv|ogg|ogv|pdf"
            + r"|ps|eps|tex|ppt|pptx|doc|docx|xls|xlsx|names"
            + r"|data|dat|exe|bz2|tar|msi|bin|7z|psd|dmg|iso"
            + r"|epub|dll|cnf|tgz|sha1"
            + r"|thmx|mso|arff|rtf|jar|csv"
            + r"|rm|smil|wmv|swf|wma|zip|rar|gz)$", parsed.path.lower())

    except TypeError:
        print ("TypeError for ", parsed)
        raise


def check_domain(url):
    # Define a regular expression pattern to match the desired domains
    domain_pattern = r'(.*\.ics\.uci\.edu/.*|.*\.cs\.uci\.edu/.*|.*\.informatics\.uci\.edu/.*|.*\.stat\.uci\.edu/.*)'

    # Search for the domain pattern in the URL
    match = re.search(domain_pattern, url)

    # If the domain matches, return True, else return False
    return bool(match)

def check_irrelevant(url):
    irrelevant_patterns = [
                        r'\bpdf\b',
                        r'calendar',
                        r'\?share',
                        r'upload',
                        r'\?action',
                        r'\?redirect',
                        r'/attachment',
                        r'\?attachment',
                        r'events',
                        r'wp-login',
                        r'\?ical']

    for pattern in irrelevant_patterns:
        if re.search(pattern, url):
            return False
    return True

def check_robots_txt(url):
    # check the robots.txt(politeness)
    # first we get the url for robots.txt
    parsed = urlparse(url)
    robot_url = parsed.scheme + "://" + parsed.netloc + "/robots.txt"
    robot_parser = urllib.robotparser.RobotFileParser()
    #set the url of robot parser to robots.txt
    robot_parser.set_url(robot_url)
    # check whether we are able to get the content in robots.txt
    robot_parser.read()
    if not robot_parser.can_fetch("IR US24 31754916,39263968,57585853", url):
        return False
    return True