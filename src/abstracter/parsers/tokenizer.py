from nltk import word_tokenize, sent_tokenize, pos_tag
from nltk.tokenize import PunktWordTokenizer
from nltk.tokenize import TreebankWordTokenizer
import nltk
import re

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
    return custom_word_tokenize(text)


def custom_sent_tokenize(text):
    sents=sent_tokenize(text)
    #sents=[]
    #nlsplit = sent_tokenize(text)
    #for para in nlsplit:
    #    #sents.append(para.replace("'s",""))
    return sents

def custom_word_tokenize(text):
    """
    Tokenizer which recognizes also named entities.
    However, it does not make links between them.
    It keeps also ponctuation.
    """
    words=[]
    named_entities=get_named_entities(text)
    for sent in custom_sent_tokenize(text):
        split = word_tokenize(sent)
        tokens = pos_tag(split)
        temp = []
        for key,val in tokens:
            if val != 'NNP':
                words.append(key)
            else:
                temp.append(key)
                if ' '.join(temp) in named_entities:
                    words.append(' '.join(temp))
                    temp=[]
    return words


pattern = '[A-Z][^A-Z]*'
def get_named_entities(text):
    named_entities = []
    tot = set()
    for sent in custom_sent_tokenize(text):
      split = word_tokenize(sent)
      tokens = pos_tag(split)
      temp = []
      for key,val in tokens:
        if val == 'NNP' and len(key) >= 3 and key[0].istitle(): #make sure uppercase too
          temp.append(key)
        else:
          if temp:
            cap_list = re.findall(pattern, ''.join(temp))
            tot.add(tuple(temp))
            if len(cap_list) >= 2:
              #also want to check if the thing is just letters
              ngs = nltk.ngrams(cap_list,2)
              for n in ngs:
                #sometimes we get acronyms, don't want that
                if not any([len(word)==1 for word in n]):
                  tot.add(n)
            temp = []
      if temp:
        tot.add(tuple(temp))
    named_entities = []
    #string the phrases
    for ph in tot:
      named_entities.append(' '.join(ph))
    return named_entities

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


if __name__=="__main__":
    text="""Peyton Manning will have a new left tackle protecting his blindside after the Denver Broncos placed Ryan Clady on season-ending injured reserve Wednesday.

Clady hurt his left foot Sunday when New York Giants defensive lineman Cullen Jenkins rolled up on him while the Broncos were trying to run out the clock in their 41-23 win. Clady will soon undergo surgery for what's being called a Lisfranc tear, which involves a separation of ligaments and joints in the foot.

Chris Clark, a fifth-year journeyman, will take the place of Clady - the undisputed leader on the line - and make his first career start at left tackle Monday night when the Broncos (2-0) host the Oakland Raiders (1-1).

''Stepping up into a role like this, it's not going to be hard for me to adjust,'' said Clark, who received a two-year contract extension on Monday. ''It's not about filling a guy's shoes for me. It's about me creating my legacy, just helping the team the best way I can and doing my job.''

Still, those are some big cleats for Clark to fill.
"""
    print(custom_word_tokenize(text))