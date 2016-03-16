import re


def replace_pattern(text, pattern, sentinel):
    """Replaces parts of a string with a sentinel value"""
    words = text.split()
    return ' '.join([word if not len(pattern.findall(word)) else sentinel for word in words])


def replace_user(text, sentinel='user'):
    user_regex = get_regex('@[^\s]+')
    return replace_pattern(text, user_regex, sentinel)


def replace_url(text, sentinel='url'):
    url_regex = get_regex('https?:\/\/\w+\.\w+')
    return replace_pattern(text, url_regex, sentinel)


def replace_number(text, sentinel='num'):
    number_regex = get_regex('[-+]?[.\d]*[\d]+[:,.\d]*')
    return replace_pattern(text, number_regex, sentinel)


def get_regex(regex_str):
    return re.compile(regex_str, re.UNICODE)


def get_num_regex():
    """Regex for substituation @whatever parts of a string."""
    return '/[-+]?[.\d]*[\d]+[:,.\d]*/'
    # return u'[^a-zA-Z]'


def get_url_regex():
    """Crude regex for matching urls."""
    # tld = 'com|ru|net|org|de|jp|uk|br|pl|in|it|fr|au|info|biz|co|io|ly|gd'
    return 'https?:\/\/\S+\b|www\.(\w+\.)+\S*/'
    # return '(https?:\/\/)?(?:\w+\.)?(\w+)*\.(?:{tld})'.format(tld=tld)
