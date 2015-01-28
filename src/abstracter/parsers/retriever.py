import abstracter.parsers.normalizer as norm
import abstracter.parsers.tokenizer as tok
import re

"""
Functions to retrieve concepts and names from a text.
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


_digits = re.compile('\d')
def contains_digits(d):
    return bool(_digits.search(d))

DISMISS=['ve']

def _links_to(entity_list,name):
    """
    See if the name is not in the entity_list.
    For example : Wayne or Rooney is in ["Wayne Rooney], since it refers obviously to the same person.
    We avoid taking a Family Name or a First Name for the whole name.
    :param entity_list: List of entities (string)
    :type name: str
    :rtype: boolean
    """
    if entity_list:
        temp=name
        for e in entity_list:
            if temp in e:
                temp=e
        return temp
    return None


def get_names(sents):
    """
    Sents : generator of sentences ; each sentence contains words and POS
    (from tokenize_and_tag)
    """
    named_entities=[]
    for sent in sents:
        temp=[]
        for key,val in sent:
            if val=='NNP':
                temp.append(key)
            else:#end of name
                if temp:
                    named_entities.append(' '.join(temp))
                temp=[]
    return named_entities    

def get_important_words(sents):
    """
    Sents : generator of sentences ; each sentence contains words and POS
    (from tokenize_and_tag)
    Returns a list of important words in the text (dismiss some, dismiss one letter words)
    """
    for sent in sents:
        for key,val in sent:
            if val in USEFUL_TAGS and not contains_digits(key) and len(key)>1 and key not in DISMISS:
                yield ([key,val])


def retrieve_words_only(sents):
    """
    We retrieve words in their normal form and count their occurrences in a dictionary.
    Thus, if a concept is used n times, it is counted n times.
    """
    words=norm.normalize(get_important_words(sents))
    concepts={}
    for word in words:
        if word in concepts:
            concepts[word]+=1
        else:
            concepts[word]=1
    #return the dictionary
    return concepts

def old_retrieve_names_only(sents):
	"""
	Get a list of all names in the text.
	Every name appear only once.
	"""
	names=list(s.lower() for s in get_names(sents))
	namescopy=names.copy()
	res=[]#suppress duplicated names and add names to res
	for name in namescopy:
		names.remove(name)
		if not _links_to(names,name):
			res.append(name)
			names.append(name)  
	return res  

def retrieve_names_only(sents):
    """
    Get a list of all names in the text.
    Every name appear only once.
    """
    names=list(s.lower() for s in get_names(sents))
    res={}
    for name in names:
        name2=_links_to(names,name)
        if not name2 in res:
            res[name2]=1
        else:
            res[name2]=res[name2]+1
    return res 


def retrieve_words_names(text):
	sents=list(tok.tokenize_and_tag(text))
	return [retrieve_words_only(sents),retrieve_names_only(sents)]

