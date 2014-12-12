from nltk import wordnet as wn
from nltk.corpus import wordnet as wnc
from nltk import word_tokenize, sent_tokenize, pos_tag
from nltk.tokenize import PunktWordTokenizer
from nltk.tokenize import TreebankWordTokenizer
from nltk import pos_tag
import os
import json

"""
These methods do not intend to be optimal, 
but have to provide an easy way to create a small conceptnetwork
for our research
"""


#sample_corpus_reader=corpus.PlaintextCorpusReader(os.getcwd()+'/sample_corpus','.*\.txt')


WORD_TOKENIZER=TreebankWordTokenizer()
POS_TAGGER=pos_tag
DISMISSED=[",",";","."]
#use also PunktWordTokenizer() or TreebankWordTokenizer()

def read_text(filename="data/sample"):
	"""
	Write down a new file at each state, to see how it progresses
	"""
	with open(filename+".txt",'r') as file,open(filename+"_words.txt",'w') as wordsfile:
		word_list=WORD_TOKENIZER.tokenize(file.read())
		print("Writing words down...")
		json.dump(word_list,wordsfile)	
	tagged_list=POS_TAGGER(word_list)
	with open(filename+"_tags.txt",'w') as tagsfile:
		print("Writing POS-tagged words down...")
		json.dump(tagged_list,tagsfile)
	with open(filename+"_wordnet_parsed.txt",'w') as wfile:
		print("Writing wordnet-tagged wors down...")
		json.dump((tag_words_for_wordnet(tagged_list)),wfile)
	


def tag_words_for_wordnet(tagged_list):
	
	#nltk.pos_tag uses the Penn Treebank project
	#list of tags available at : http://www.ling.upenn.edu/courses/Fall_2007/ling001/penn_treebank_pos.html
	wordnet_tagged_list=[]
	t=""
	for w in tagged_list:
		v=w[0]
		tag=w[1]
		if v in DISMISSED:
			pass
		elif tag=='FW':#foreign word
			t=wnc.NOUN
			wordnet_tagged_list.append([v,t])
		elif tag in ["JJ","JJR","JJS"]:
			t=wnc.ADJ
			wordnet_tagged_list.append([v,t])
		elif tag in ["MD","NN","NNS","NNP","NNPS"]:
			t=wnc.NOUN
			wordnet_tagged_list.append([v,t])
		elif tag in ["RB","RBR","RBS"]:
			t=wnc.ADV
			wordnet_tagged_list.append([v,t])
		elif tag in ["VB","VBD","VBG","VBN","VBP","VBZ"]:
			t=wnc.VERB
			wordnet_tagged_list.append([v,t])
		#we're not interested by other tags (especially small words)

	#the .01 here refers is a lexical id, used by wordnet to make 
	#a difference between different senses of the same word
	#n for nou, v for verb, a for adjective, r for adverb
	final_list=[]
	correspondance={wnc.NOUN : ".n.01", wnc.ADJ : ".a.01", wnc.ADV : ".r.01", wnc.VERB : ".v.01"}
	for (v,tag) in wordnet_tagged_list:
		vmorphed=wnc.morphy(v,tag)
		if vmorphed:
			final_list.append(vmorphed+correspondance[tag])
		else:
			final_list.append(v+correspondance[tag])
	return final_list
	


def create_network_from_words(word_list):
	conceptnetwork=Network()
	pass


def keep_important_words(word_list):
	"""
	There is room for a use of tf-idf in order to keep important
	words only
	But it's already the case with the POS
	"""
	return word_list

def create_network_from_sample(path):
	"""
	Given a text sample, we create a conceptnetwork using only nltk 
	data, such as wordnet (similarity measures can be used)
	"""
	pass


read_text("data/sample")
