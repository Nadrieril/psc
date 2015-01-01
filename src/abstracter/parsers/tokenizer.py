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
USEFUL_TAGS=["JJ","NN","NNS","VB","VBD","VBG","VBN","VBP","VBZ"];
NOT_USEFUL_TAGS=["CC","NNP","NNPS","RB","RBR","RBS","JJR","JJS","MD"]
#R : adverbs
#J : adjectives
#V : verbs
#N : nouns
# 1.  CC    Coordinating conjunction
# 2.    CD  Cardinal number
# 3.    DT  Determiner
# 4.    EX  Existential there
# 5.    FW  Foreign word
# 6.    IN  Preposition or subordinating conjunction
# 7.    JJ  Adjective
# 8.    JJR Adjective, comparative
# 9.    JJS Adjective, superlative
# 10.   LS  List item marker
# 11.   MD  Modal
# 12.   NN  Noun, singular or mass
# 13.   NNS Noun, plural
# 14.   NNP Proper noun, singular
# 15.   NNPS    Proper noun, plural
# 16.   PDT Predeterminer
# 17.   POS Possessive ending
# 18.   PRP Personal pronoun
# 19.   PRP$    Possessive pronoun
# 20.   RB  Adverb
# 21.   RBR Adverb, comparative
# 22.   RBS Adverb, superlative
# 23.   RP  Particle
# 24.   SYM Symbol
# 25.   TO  to
# 26.   UH  Interjection
# 27.   VB  Verb, base form
# 28.   VBD Verb, past tense
# 29.   VBG Verb, gerund or present participle
# 30.   VBN Verb, past participle
# 31.   VBP Verb, non-3rd person singular present
# 32.   VBZ Verb, 3rd person singular present
# 33.   WDT Wh-determiner
# 34.   WP  Wh-pronoun
# 35.   WP$ Possessive wh-pronoun
# 36.   WRB Wh-adverb

def tokenize(text):
    """
    Split a text into tokens (words, morphemes, names and punctuation).
    """
    return custom_word_tokenize(refactor(text))

def refactor(text):
    res=text
    for c in ALWAYS_REMOVE:
        res=res.replace(c," ")
    return res


MAJ=("ABCDEFGHIJKLMNOPQRSTUVWXYZÀÈÉÙŒ")
PUNKT=(";.,?!:_()'/’\u2019()[]=")

ALWAYS_REMOVE="()[]="

def normalizer_tokenize(text,named_entities):
    words=[]
    for sent in custom_sent_tokenize(text):
        sent2=sent
        for i in MAJ:
            sent2=sent2.replace(i," "+i)
        for i in PUNKT:
            sent2=sent2.replace(i," ")
        split=word_tokenize(sent2)
        tokens=pos_tag(split)
        temp = []
        for key,val in tokens:
            if val != 'NNP':
                words.append([key,val])
            else:
                temp.append(key)
                if ' '.join(temp) in named_entities:
                    words.append([' '.join(temp),'NNP'])
                    temp=[]
    return words        

_digits = re.compile('\d')
def contains_digits(d):
    return bool(_digits.search(d))

DISMISS=['s','t','ve','m']

def concepts_tokenize(text):
    """
    Does not keep named entities
    """
    words=[]
    for sent in custom_sent_tokenize(text):
        sent2=sent
        for i in MAJ:
            sent2=sent2.replace(i," "+i)
        for i in PUNKT:
            sent2=sent2.replace(i," ")
        split=word_tokenize(sent2)
        tokens=pos_tag(split)
        for key,val in tokens:
            if val in USEFUL_TAGS and not contains_digits(key) and key not in DISMISS:#suppress NNP !!
                words.append([key,val])
    return words       


BOUNDARIES=["!",".","?","\n","'"]

def custom_sent_tokenize(text):
    temp=[]
    sents=[]
    car2=' '
    for car in text:
        if (car in MAJ and car2 != ' '):
            sents.append(''.join(temp))
            temp=[]
            temp.append(car)
        elif car not in BOUNDARIES:
            temp.append(car)
        else:
            sents.append(''.join(temp))
            temp=[]
        car2=car
    return sents

def custom_word_tokenize(text):
    """
    Tokenizer which recognizes named_entities, and keeps the order of the words.
    """
    words=[]
    for sent in custom_sent_tokenize(text):
        split = word_tokenize(sent)
        tokens = pos_tag(split)
        temp = []
        for key,val in tokens:
            if val=='NNP':
                temp.append(key)
            else:
                if temp:
                    words.append(' '.join(temp))
                    temp=[]
                words.append(key)
        if temp:
            words.append(' '.join(temp))
            temp=[]
    return words

#def get_named_entities(text):
#    named_entities = []
#    tot = set()
#    for sent in custom_sent_tokenize(text):
#      split = word_tokenize(sent)
#      tokens = pos_tag(split)
#      temp = []
#      for key,val in tokens:
#        if val == 'NNP' and len(key) >= 3 and key[0].istitle(): #make sure uppercase too
#          temp.append(key)
#        else:
#          if temp:
#            cap_list = re.findall(pattern, ''.join(temp))
#            tot.add(tuple(temp))
#            if len(cap_list) >= 2:
#              #also want to check if the thing is just letters
#              ngs = nltk.ngrams(cap_list,2)
#              for n in ngs:
#                #sometimes we get acronyms, don't want that
#                if not any([len(word)==1 for word in n]):
#                  tot.add(n)
#            temp = []
#      if temp:
#        tot.add(tuple(temp))
##    named_entities = []
#    #string the phrases
#    for ph in tot:
#      named_entities.append(' '.join(ph))
#    return named_entities

def get_named_entities(text):
    named_entities=[]
    for sent in custom_sent_tokenize(text):
        sent2=sent
        for i in MAJ:
            sent2=sent2.replace(i," "+i)
        for i in PUNKT:
            sent2=sent2.replace(i," ")
        split = word_tokenize(sent2)
        tokens = pos_tag(split)
        temp = []
        for key,val in tokens:
            if val=='NNP':
                temp.append(key)
            else:#end of name
                if temp:
                    named_entities.append(' '.join(temp))
                temp=[]
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
        while (s[j - 1]) not in BOUNDARIES:
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
    #for s in string_pieces(text):
    #    print(s)
    #print(custom_word_tokenize(text))
    print(tokenize(text))