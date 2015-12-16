import re

# TODO:
# 1. finish tests
# 2. tokenize


def convertToLowerCase(iterable):
    """Convert an iterable of strings to lower case"""
    return (i.lower() for i in iterable)


# TODO: make this less horrid and more functional
def replaceStringPatterns(text, sre_patterns, sentinels):
    """Apply an iterable of substitution operations to a string."""
    for func, val in zip(sre_patterns, sentinels):
        text = replacePattern(text, func, val)
    return text


def replacePattern(text, sre_pattern, sentinel):
    """Replaces parts of a string with a sentinel value"""
    return sre_pattern.sub(sentinel, text)


def getPatternMatcher(regex_str):
    """Get pattern matcher for any string beginning with `@`."""
    return re.compile(regex_str, re.UNICODE)


def getAtUserRegex():
    """Regex for substituation @whatever parts of a string."""
    return u'@[^\s]+'


def getUrlRegex():
    """A lonnnggg regex for replacing url parts of a string."""
    # Regex copied directly from here: https://gist.github.com/dperini/729294
    # See here for discussion: https://mathiasbynens.be/demo/url-regex
    return (
            # protocol identifier
            u"(?:(?:https?|ftp)://)"
            # user:pass authentication
            u"(?:\S+(?::\S*)?@)?"
            u"(?:"
            # IP address exclusion
            # private & local networks
            u"(?!(?:10|127)(?:\.\d{1,3}){3})"
            u"(?!(?:169\.254|192\.168)(?:\.\d{1,3}){2})"
            u"(?!172\.(?:1[6-9]|2\d|3[0-1])(?:\.\d{1,3}){2})"
            # IP address dotted notation octets
            # excludes loopback network 0.0.0.0
            # excludes reserved space >= 224.0.0.0
            # excludes network & broadcast addresses
            # (first & last IP address of each class)
            u"(?:[1-9]\d?|1\d\d|2[01]\d|22[0-3])"
            u"(?:\.(?:1?\d{1,2}|2[0-4]\d|25[0-5])){2}"
            u"(?:\.(?:[1-9]\d?|1\d\d|2[0-4]\d|25[0-4]))"
            u"|"
            # host name
            u"(?:(?:[a-z\u00a1-\uffff0-9]-?)*[a-z\u00a1-\uffff0-9]+)"
            # domain name
            u"(?:\.(?:[a-z\u00a1-\uffff0-9]-?)*[a-z\u00a1-\uffff0-9]+)*"
            # TLD identifier
            u"(?:\.(?:[a-z\u00a1-\uffff]{2,}))"
            u")"
            # port number
            u"(?::\d{2,5})?"
            # resource path
            u"(?:/\S*)?"
            u"$")
