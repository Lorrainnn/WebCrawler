from urllib.parse import urlparse
import urllib.robotparser

def decode_content(resp):
    encode_information = resp.raw_response.headers.get("Content-Type").strip().split(';')
    # set the default to utf-8
    encode = 'utf-8'
    # if we find the page has its own encode, we replace encode with it
    for single in encode_information:
        if "charset=" in single:
            charset_value = single.strip().split('=')[1].strip()
            encode = charset_value.strip(' "\'')
    # get the content by decoding
    return resp.raw_response.content.decode(encode)

def robot_checker(url, resp):
    parsed = urlparse(resp.url)
    robot_url = parsed.scheme + "://" + parsed.netloc + "/robots.txt"
    # and build the robotfileparser
    robot_parser = urllib.robotparser.RobotFileParser()
    # set the url of robot parser to robots.txt
    robot_parser.set_url(robot_url)
    # read the allow
    robot_parser.read()
    # check whether we are able to get the content in robots.txt
    if not robot_parser.can_fetch("IR US24 Our 39263968", url):
        return True