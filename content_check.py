import re
def similar_check(content, current_fingerprint) -> list:
    # similarity system, we first generate a fingerprint by hash consecutive 3 words.
    words = re.findall(r'[A-Za-z0-9]+', content.lower())
    single_fg = []
    for index in range(len(words) - 2):
        single_list = [words[index], words[index + 1], words[index] + 2]
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