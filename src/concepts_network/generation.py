from nltk import wordnet as wn
from nltk import word_tokenize, sent_tokenize, pos_tag
from nltk.tokenize import PunktWordTokenizer
import os
import json

"""
These methods do not intend to be optimal, 
but have to provide an easy way to create a small conceptnetwork
for our research
"""


#sample_corpus_reader=corpus.PlaintextCorpusReader(os.getcwd()+'/sample_corpus','.*\.txt')


WORD_TOKENIZER=PunktWordTokenizer()
#use also WordPunktTokenizer() or TreebankWordTokenizer()

def read_text(filename="data/sample"):
	with open(filename+".txt",'r') as file:
		with open(filename+"_sentences.txt",'w') as sentfile:
			json.dump(sent_tokenize(file.read()),sentfile)
	with open(filename+".txt",'r') as file:
		with open(filename+"_words.txt",'w') as wordsfile:
			json.dump(WORD_TOKENIZER.tokenize(file.read()),wordsfile)


def create_network_from_words(word_list):
	pass


def keep_important_words(word_list):
	"""
	There is room for a use of tf-idf in order to keep important
	words only
	"""
	return word_list

def create_network_from_sample(path):
	"""
	Given a text sample, we create a conceptnetwork using only nltk 
	data, such as wordnet (similarity measures can be used)
	"""
	pass


read_text()