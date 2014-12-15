from nltk import word_tokenize, sent_tokenize, pos_tag
from nltk.tokenize import PunktWordTokenizer
from nltk.tokenize import TreebankWordTokenizer

"""
Custom word tokenizer, which has to recognize english common words
and names
some code comes from 
https://github.com/commonsense/metanl/commit/55c0099900057ae975f87e28183fa8fcdfcd328b
which is by now deprecated
"""

def tokenize(text):
    """
    Split a text into tokens (words, morphemes, names and punctuation).
    """
    return list(_tokenize_gen(text))


def _tokenize_gen(text):
    for sent in sent_tokenize(text):
        for word in word_tokenize(sent):
            yield word


def custom_word_tokenize(sent):
	return nltk.word_tokenize(sent)


#not from me
def string_pieces(s, maxlen=1024):
    """
    Takes a (unicode) string and yields pieces of it that are at most `maxlen`
    characters, trying to break it at punctuation/whitespace. This is an
    important step before using a tokenizer with a maximum buffer size.
    """
    if not s:
        return
    i = 0
    while True:
        j = i + maxlen
        if j >= len(s):
            yield s[i:]
            return
        # Using "j - 1" keeps boundary characters with the left chunk
        while unicodedata.category(s[j - 1]) not in BOUNDARY_CATEGORIES:
            j -= 1
            if j == i:
                # No boundary available; oh well.
                j = i + maxlen
                break
        yield s[i:j]
        i = j