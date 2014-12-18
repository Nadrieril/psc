from nltk import wordnet as wn
from nltk.corpus import wordnet as wnc
from nltk import word_tokenize, sent_tokenize, pos_tag
from nltk.tokenize import PunktWordTokenizer
from nltk.tokenize import TreebankWordTokenizer
from abstracter.concepts_network import *
from abstracter.parsers import tokenizer
from abstracter.util import json_stream
from abstracter.conceptnet5_client.conceptnet5 import conceptnet5 as cn5
import json

"""
These methods do not intend to be optimal, 
but have to provide an easy way to create a small conceptnetwork
for our research.

Here, we implement the following :
- reading and tokenizing the text downto words
- tag these words with a POS from nltk
- creating the network from these words by using wordnet data
- we use polysemy to compute concept degree of abstraction
- we use path_similarity to compute approximately similarity between all our nodes :

synset1.path_similarity(synset2): 
Return a score denoting how similar two word senses are, 
based on the shortest path that connects the senses in the is-a
(hypernym/hypnoym) taxonomy. The score is in the range 0 to 1. 
By default, there is now a fake root node added to verbs so for
cases where previously a path could not be found---and None 
was returned---it should return a value. The old behavior can 
be achieved by setting simulate_root to be False. A score of 1 
represents identity i.e. comparing a sense with itself will 
return 1.
(from http://www.nltk.org/howto/wordnet.html)

"""


#sample_corpus_reader=corpus.PlaintextCorpusReader(os.getcwd()+'/sample_corpus','.*\.txt')



DISMISSED_WORDS=[",",";","."]
#use also PunktWordTokenizer() or TreebankWordTokenizer()


def tokenize(text):
	#word_list=TreebankWordTokenizer().tokenize(text);
	#res=[]
	#for word in word_list:
	#	if word.rstrip('.'):
	#		res.append(word.rstrip('.'))
	#		#cause we do not keep the .
	return tokenizer.tokenize(text)


def tag(word_list):
	return pos_tag(word_list)

########################################################

def read_and_tokenize(filename="data/sample"):
	"""
	We read the text and tokenize it, but we don't create the network.
	"""
	with open(filename+".txt",'r') as file,open(filename+"_words.txt",'w') as wordsfile:
		word_list=tokenize(file.read())
		print("Writing words down...")
		json.dump(word_list,wordsfile)
	tagged_list=pos_tag(word_list)
	with open(filename+"_tags.txt",'w') as tagsfile:
		print("Writing POS-tagged words down...")
		json.dump(tagged_list,tagsfile)
	print("All done.")


def read_text(filename="data/sample"):
	"""
	Write down a new file at each state, to see how it progresses
	"""
	with open(filename+".txt",'r') as file,open(filename+"_words.txt",'w') as wordsfile:
		word_list=tokenize(file.read())
		print("Writing words down...")
		json.dump(word_list,wordsfile)	
	tagged_list=pos_tag(word_list)
	with open(filename+"_tags.txt",'w') as tagsfile:
		print("Writing POS-tagged words down...")
		json.dump(tagged_list,tagsfile)
	wordnet_tagged_list=tag_words_for_wordnet(tagged_list)
	with open(filename+"_wordnet_parsed.txt",'w') as wfile:
		print("Writing wordnet-tagged words down...")
		json.dump(wordnet_tagged_list,wfile)
	print("Generating network...")
	conceptnetwork=create_network_from_words(wordnet_tagged_list)
	conceptnetwork.save_to_JSON(filename+"_network.txt")
	


def tag_words_for_wordnet(tagged_list):
	#nltk.pos_tag uses the Penn Treebank project
	#list of tags available at : http://www.ling.upenn.edu/courses/Fall_2007/ling001/penn_treebank_pos.html
	wordnet_tagged_list=[]
	final_list=[]
	
	for w in tagged_list:
		v=w[0]
		tag=w[1]
		if v in DISMISSED_WORDS:
			pass
		elif tag=='FW':#foreign word
			t=wnc.NOUN
			wordnet_tagged_list.append([v,t])
		elif tag in ["JJ","JJR","JJS"]:
			t=wnc.ADJ
			wordnet_tagged_list.append([v,t])
		elif tag in ["MD","NN","NNS"]:
			t=wnc.NOUN
			wordnet_tagged_list.append([v,t])
		elif tag in ["NNP","NNPS"]:#not tag
			t=None
			final_list.append([v,t])
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
	
	#correspondance={wnc.NOUN : ".n.01", wnc.ADJ : ".a.01", wnc.ADV : ".r.01", wnc.VERB : ".v.01"}
	for (v,tag) in wordnet_tagged_list:
		vmorphed=wnc.morphy(v,tag)
		if vmorphed and [vmorphed,tag] not in final_list:
			final_list.append([vmorphed,tag])
		elif [v,tag] not in final_list:
			final_list.append([v,tag])
	final_list.sort()
	return final_list
	

def remove_co_occurrences(wordnet_tagged_list):
	"""
	could have been useful, but already done in the method
	tag_words_for_wordnet
	"""
	pass


def create_network_from_words(wordnet_tagged_list):
	"""
	Create network (small one)
	We use wordnet data to approach ic, by using polysemy
	Idea : the more a word is an abstract concept, the more 
	it has different meanings
	First, we create all concepts with this approach
	If it's a proper noun, it has no wordnet tag, thus we only create
	a corresponding concept with high ic


	Then, we create edges.
	We create a dictionary of synsets for each concept.
	We keep only one sens possible, the first, which is not good
	(we could capture the real sense in the text)

	We use a similarity measure in term of path between node, based
	on the shortest path connecting the node in the is-a relationship
	(from 0 to 1, with 1 they are synonyms)


	"""
	conceptnetwork=Network()
	for v,tag in wordnet_tagged_list:
		if tag:
			polysemy=len(wnc.synsets(v,pos=tag))
			tmp_concept=Concept(network=conceptnetwork.network,id=v,ic=polysemy)
		else:#no tag, such as a proper noun
			tmp_concept=Concept(network=conceptnetwork.network,id=v,ic=5)

	#at this point, all nodes have been created
	#then, we study edges
	#following code to build edges from wordnet, using isa relations
	wnsynsets={}
	for v,tag in wordnet_tagged_list:
		if tag and wnc.synsets(v,pos=tag):#if it s not empty
			wnsynsets[v]=wnc.synset(wnc.synsets(v,pos=tag)[0].name())
	#not beautiful : only keeping the first sense possible of the word
	for v,tag in wordnet_tagged_list:
		for v2,tag2 in wordnet_tagged_list:
			if v in wnsynsets and v2 in wnsynsets:
				if (not v==v2) and wnsynsets[v] and wnsynsets[v2]:
					tmp=wnsynsets[v].path_similarity(wnsynsets[v2])
					if tmp >0.1:
						tmp_arc=Arc(network=conceptnetwork.network,fromId=v,toId=v2,data=tmp)
	return conceptnetwork



def polysemy(word):
	return len(wnc.synsets(word,pos=None)) 

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

def expand_network_from_seed(list,max_nodes=10,network=Network()):
	"""
	Given list of some relevant concepts, we create a conceptnetwork using :
	-conceptnet5 data
	-wordnet polysemy
	Notes :
	- a node can't expand more than a fixed number of edges (see conceptnet5.py)
	- there is a random component when we get the edges from conceptnet5
	"""
	nodenumber=0
	while nodenumber<max_nodes and len(list)>0:
		word=list[0]
		#print(word)
		conceptic=polysemy(word)
		if conceptic==0:#TODO : check if it's a name
			conceptic=7
		#print(conceptic)
		concept=Concept(network.network,word,ic=conceptic)
		nodenumber+=1
		cn5.expand_concept(word,network.network)
		list.remove(word)
		for concept2 in concept.successors():
			conceptic=polysemy(concept2.id)
			if conceptic==0:#TODO : check if it's a name
				conceptic=7
			concept2.ic=conceptic
			list.append(concept2.id)

			
SEED=["America","Arsenal","Aston","Barkley","Basel","Brazil","Cahill","Cup","England","Euro","Liverpool","Manchester","Norway","Sterling","wayne_rooney",
"Switzerland","Uruguay","World","apathy","appointment","atmosphere","attacker","back","brilliantly","busy","captain","celebrate", "comprehensively","decisive","defeat","display","eliminate","encouragement","exit","glamorous","imagination","opponent","partnership",
"penalty","performance","play","player","positive","preparation","pressure","prove","public","retire","summer","surreal", "team", "winner","worry","victory", "young"]

SMALL_SEED=["America","Arsenal","Brazil","Cup","England","wayne_rooney","appointment","atmosphere",
"attacker","back","brilliantly","busy","captain","celebrate","defeat","eliminate","encouragement","exit",
"penalty","performance","play","player","positive","preparation","pressure","prove","public",
 "team", "winner","worry","victory", "young"]


def test():
	n=Network()
	expand_network_from_seed(SMALL_SEED,max_nodes=100,network=n)
	n.save_to_JSON_stream("network_example/network_example_2")
	nx.draw(n.network)
	#plt.show()
	plt.savefig("network_example/network_example_2.png")

test()


#print polysemy('human')


#read_text("data/sample")

#n=Network();
#n.load_from_JSON("data/sample_network.txt")

#plt.show()

 #read_and_tokenize("network_example/sample")

#n=Network()
#n.load_from_JSON("data/sample_network.txt")
#n.save_to_JSON_stream("network_example/network_example")
#nx.draw(n.network)
#plt.savefig("network_example/network_example.png")

#n.load_nodes_from_stream("data/test_nodes.jsons");
#n.load_edges_from_stream("data/test_edges.jsons")

#n.load_from_JSON_stream(nodes_files=["data/test_nodes.jsons"],edges_files=["data/test_edges.jsons"])

#n.save_to_JSON_stream("data/test2")

#n=Network()
#toto=Concept(n.network,id='wayne_rooney')
#cn5.expand_concept('wayne_rooney',n.network)
#n.save_to_JSON_stream("network_example/network_example_1")
#nx.draw(n.network)
#plt.savefig("network_example/network_example_1.png")
