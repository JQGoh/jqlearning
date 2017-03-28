#! /usr/bin/env python3
import textwrap
import re


def regex_rules(words, extract=0):
    """A function which returns the regular expression (regex) pattern for the 
    provided keywords.

    Parameters
    ----------
    words : list
        A list of keywords or regex patterns.
    
    extract : int, default 0
        - 0 : Only the provided keywords or regex patterns.
        - 1 : Including words/word adjacent to the keywords or regex patterns.
        - 2 : Including the whole sentence having the keywords or regex
              patterns. It assumes a sentence is sandwiched by two periods
              or start/end boundaries.
            
    Returns
    -------
    patterns : list
        A list of regex rules containing the keywords in the 'words', 
        according to the rules defined by 'extract'.
    """
    assert type(words) is list, "words is not in a list format"
    for word in words:
        assert type(word) is str, "words must have elements of strings"

    patterns = []
    for word in words:
        if extract == 0:
            # \b means \x08, a backspace. So we need \\b
            pattern = '\\b(' + word + ')\\b'
        elif extract == 1:
            # \w or \\w are the same
            # The usage of () implies a backreference, need (?: )
            pattern = '(?:\w+\s+|\\b)(?:' + word + ')(?:\s+\w+|\\b)'
        elif extract == 2:
            pattern = "(?:\.?|^)[^.]*\\b(?:" + word + ")\\b[^.]*(?:\.?|$)" 
        patterns.append(pattern)
    return patterns


def regex(text, keyword, rule):
    """A simple function used to test the text extraction
    based on the designed regular expression patterns.

    Parameters
    ----------
    text : str
        The input text.

    keyword : list
        A list of keywords or regex patterns.

    rule : int
        Same as the 'extract' in the regex_rules function.
    """
    print(text)
    patterns = regex_rules(keyword, rule)
    print(patterns)
    for pattern in patterns:
        text_extracted = re.findall(pattern, text, re.I)
        if text_extracted:
            print(text_extracted)
    print('*'*80)

if __name__ == "__main__":
    rule0 = 0
    rule1 = 1
    rule2 = 2 

    text1 = textwrap.dedent("""
    Johnathan likes to play badminton. John likes to play basketball. 
    Max likes computer games, but Johnathan prefer board games instead.
    Michael and Max love to play soccer.
    """)
    keyword1 = ['John|Max', 'games']
    regex(text1, keyword1, rule0)
    regex(text1, keyword1, rule1)
    
    text0 = textwrap.dedent("""
    I visited the company a few years ago.
    They    visit    ABC company in this coming
    weekend, and they would like to have another visit. Visit to ABC company 
    makes people feeling great. I am keen to arrange a
    
    new visit
    
    by the end of the year. 
    """)
    keyword0 = ['visit']
    regex(text0, keyword0, rule1)
    regex(text0, keyword0, rule2)

    text2 = textwrap.dedent("""
    Hi there, we are from an international company. We provide excellent
    services and some of our clients are from MNC. We have been in the 
    business for more than 50 years.

    Enroll into a yearly contract with us and get your air-conditioning
    serviced at $25 per unit.
    """)
    keyword2 = ['(?:\$?\d+\.?\d?\d?|price|charges?)(?: is| nett| per)?(?:/| per | an | one | half | every | each )(?:unit|(?!hour |hr )\w+)\\b']
    regex(text2, keyword2, rule2)
