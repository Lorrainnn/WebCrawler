import re
from urllib.parse import urlparse
import urllib.robotparser

def check_domain(url):
    # Define a regular expression pattern to match the desired domains
    domain_pattern = r'(.*\.ics\.uci\.edu/.*|.*\.cs\.uci\.edu/.*|.*\.informatics\.uci\.edu/.*|.*\.stat\.uci\.edu/.*)'

    # Search for the domain pattern in the URL
    match = re.search(domain_pattern, url)

    # If the domain matches, return True, else return False
    return bool(match)

def check_length(url):
    return len(url)<200

def check_repeating(url):
    # check for repeating directories
    # Source: https://support.archive-it.org/hc/en-us/articles/208332963-Modify-your-crawl-scope-with-a-Regular-Expression#RepeatingDirectories
    if re.match(r"^.*?(/.+?/).*?\1.*$|^.*?/(.+?/)\2.*$", url):
        return False
    return True

def check_exclude_url(url):
    # Set of patterns to be blocked
    irrelevant_pattern = {"pdf", "calendar", "?share", "upload", "?action", "?redirect", "/attachment", "?attachment", "events", "wp-login", "?ical"}

    # Check if the URL contains any of the blocked patterns
    for pattern in irrelevant_pattern:
        if pattern in url:
            return True

    # If none of the patterns match, include the URL
    return False

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