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

