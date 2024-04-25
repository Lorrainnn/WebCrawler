import re
from urllib.parse import urlunparse, unquote, urlencode, parse_qsl

def similar_check(content, current_fingerprint) -> list:
    # similarity system, we first generate a fingerprint by hash consecutive 3 words.
    words = re.findall(r'[A-Za-z0-9]+', content.lower())
    single_fg = []
    for index in range(len(words) - 2):
        single_list = [words[index], words[index + 1], words[index + 2]]
        single_hash = hash("".join(single_list))
        single_fg.append(single_hash)
    #for every fingerprint we have, we compute the fingerprint using
    # intersection / union. if similarity is bigger then 0.8, not access it.
    for fg in current_fingerprint:
        intersection = len(set(single_fg).intersection(set(fg)))    
        union = len(set(single_fg).union(set(fg)))
        if union != 0 and intersection * 1.0 / union > 0.8:
            return []
    # if valid, we append the new fingerprint to our fingerprint list
    current_fingerprint.append(single_fg)
    
    return current_fingerprint

def query_cleaner(parsed, new_scheme, new_netloc, new_path):
    decoded_query = unquote(parsed.query)
    #make a list consisting of [key, value] pair
    key_value_querylist = parse_qsl(decoded_query, keep_blank_values = True)
    #sort the key_value_list
    sorted_query = sorted(key_value_querylist, key = lambda single:single[0])
    #encode it back to query
    new_query = urlencode(sorted_query,doseq = True)

    #combine all the modified scheme, netloc, path, query with removing fragment to the new url
    return urlunparse((new_scheme, new_netloc, new_path, parsed.params, new_query, ""))