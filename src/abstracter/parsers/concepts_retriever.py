from nltk.corpus import wordnet as wn
from nltk import word_tokenize, sent_tokenize, pos_tag
try:
	from abstracter.parsers.tokenizer import get_named_entities,custom_sent_tokenize
except ImportError:
	from tokenizer import get_named_entities,custom_sent_tokenize

import re#regular expressions

DISMISSED_WORDS=[",",";",".","'s","n't"]

USEFUL_TAGS=["JJ","NN","NNS","VB","VBD","VBG","VBN","VBP","VBZ"];
NOT_USEFUL_TAGS=["CC","NNP","NNPS","RB","RBR","RBS","JJR","JJS","MD"]
#R : adverbs
#J : adjectives
#V : verbs
#N : nouns
# 1.  CC	Coordinating conjunction
# 2.	CD	Cardinal number
# 3.	DT	Determiner
# 4.	EX	Existential there
# 5.	FW	Foreign word
# 6.	IN	Preposition or subordinating conjunction
# 7.	JJ	Adjective
# 8.	JJR	Adjective, comparative
# 9.	JJS	Adjective, superlative
# 10.	LS	List item marker
# 11.	MD	Modal
# 12.	NN	Noun, singular or mass
# 13.	NNS	Noun, plural
# 14.	NNP	Proper noun, singular
# 15.	NNPS	Proper noun, plural
# 16.	PDT	Predeterminer
# 17.	POS	Possessive ending
# 18.	PRP	Personal pronoun
# 19.	PRP$	Possessive pronoun
# 20.	RB	Adverb
# 21.	RBR	Adverb, comparative
# 22.	RBS	Adverb, superlative
# 23.	RP	Particle
# 24.	SYM	Symbol
# 25.	TO	to
# 26.	UH	Interjection
# 27.	VB	Verb, base form
# 28.	VBD	Verb, past tense
# 29.	VBG	Verb, gerund or present participle
# 30.	VBN	Verb, past participle
# 31.	VBP	Verb, non-3rd person singular present
# 32.	VBZ	Verb, 3rd person singular present
# 33.	WDT	Wh-determiner
# 34.	WP	Wh-pronoun
# 35.	WP$	Possessive wh-pronoun
# 36.	WRB	Wh-adverb

SPECIAL_MORPH={"'s":"","'m" : "am",
"'ve" : "have"}

def _links_to(entity_list,name):
	"""
	:param entity_list: List of entities (string)
	:type name: str
	:rtype: boolean
	"""
	if entity_list:
		for e in entity_list:
			if name in e:
				return True
	return False


def refactor(text):
	for key in SPECIAL_MORPH:
		text=text.replace(key," "+SPECIAL_MORPH[key])
	return text

_digits = re.compile('\d')
def contains_digits(d):
    return bool(_digits.search(d))

def retrieve_concepts(arg):
	"""
	-retrieve names
	-suppress duplicated names (clady and ryan clady -> ryan clady)
	-keep only adjectives, nouns, verbs, adverbs
	-morph with wordnet
	"""
	text=refactor(arg)
	names=get_named_entities(text)
	namescopy=names.copy()
	concepts=[]
	totag=[]
	#suppress duplicated names
	for name in namescopy:
		names.remove(name)
		if not _links_to(names,name):
			concepts.append(name.lower())
		names.append(name)
	#tokenize and tag
	for sent in custom_sent_tokenize(text):
		split = word_tokenize(sent)
		tokens = pos_tag(split)
		for key,val in tokens:
			if val in USEFUL_TAGS and key not in DISMISSED_WORDS and not contains_digits(key):
				totag.append([key,val])    
	#tag for wordnet and morph
	for w in totag:
		v=w[0].lower()
		tag=w[1]
		if tag=='FW':#foreign word
			pass
		elif tag in ["JJ","JJR","JJS"]:
			t=wn.ADJ
		elif tag in ["MD","NN","NNS"]:
			t=wn.NOUN
		elif tag in ["RB","RBR","RBS"]:
			t=wn.ADV
		elif tag in ["VB","VBD","VBG","VBN","VBP","VBZ"]:
			t=wn.VERB
		vmorphed=wn.morphy(v,t)
		if vmorphed==v or not vmorphed:#if the tag is not useful
			#print(vmorphed)
			vmorphed=wn.morphy(v)
		#print("morphy : "+v+","+t+"="+(vmorphed if vmorphed else ""))	
		if vmorphed and vmorphed not in concepts:
			concepts.append(vmorphed)
		elif v not in concepts:
			concepts.append(v)
	#sort in alphabetical order
	concepts.sort()
	return concepts


if __name__=="__main__":
	pass
