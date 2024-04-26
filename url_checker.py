from urllib.parse import urlparse


def check_not_allowed(forbidden_url, url):
    return url not in forbidden_url

#check whether scheme is http or https
def check_valid_scheme(parsed):
    return parsed.scheme in set(["http", "https"])

#check the domain
def check_domain(parsed):
    return not (parsed.netloc.endswith(".informatics.uci.edu") or parsed.netloc.endswith(".ics.uci.edu") or parsed.netloc.endswith(".cs.uci.edu") or parsed.netloc.endswith(".stat.uci.edu"))

# no calendar, stayconnected. pdf
def check_calendar(url):
    return not ("calendar" in url or "stayconnected" in url)

# no len > 300 url
def check_length(url):
    return len(url) < 300


  


    