import re

# TODO:
# 1. finish tests
# 2. wordize


def convert_to_lowercase(iterable):
    """Convert an iterable of strings to lower case"""
    return (i.lower() for i in iterable)


# TODO: make this less horrid and more functional
def remove_pattern(text, pattern):
    """Apply an iterable of substitution operations to a string."""
    words = text.split()
    return ' '.join([word for word in words if pattern.match(word) is None])


def replace_pattern(text, pattern, sentinel):
    """Replaces parts of a string with a sentinel value"""
    words = text.split()
    return ' '.join([word if pattern.match(word) is None else sentinel for word in words ])


def get_pattern_matcher(regex_str):
    """Get pattern matcher for any string beginning with `@`."""
    return re.compile(regex_str, re.UNICODE)


def get_at_user_regex():
    """Regex for substituation @whatever parts of a string."""
    return u'@[^\s]+'


def get_num_regex():
    """Regex for substituation @whatever parts of a string."""
    return u'[^a-zA-Z]'


def get_url_regex():
    """Crude regex for matching urls."""
    tld = 'com|ru|net|org|de|jp|uk|br|pl|in|it|fr|au|info|biz|co|io|ly|gd'
    return '(https?:\/\/)?(?:\w+\.)?(\w+)*\.(?:{tld})'.format(tld=tld)
