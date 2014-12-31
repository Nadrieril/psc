from nltk.corpus import wordnet as wnc
from nltk import word_tokenize, sent_tokenize, pos_tag
from nltk.tokenize import PunktWordTokenizer
from nltk.tokenize import TreebankWordTokenizer
from abstracter.concepts_network import Network
import abstracter.parsers.tokenizer as tok
import abstracter.parsers.concepts_retriever as cr
from abstracter.util import json_stream
from abstracter.conceptnet5_client.api import api as cn5
import json
import os

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
	return tok.tokenize(text)


def tag(word_list):
	return pos_tag(word_list)

def read_concepts(filename="data/sample"):
	with open(filename+".txt",'r') as file,open(filename+"_concepts.txt",'w') as conceptsfile:
		print("Reading "+filename+" and calculating concepts...")
		concepts=cr.retrieve_concepts(file.read())
		print("Writing down...")
		json.dump(concepts,conceptsfile)




def polysemy(word):
	return len(wnc.synsets(word,pos=None)) 




			
SEED=["America","Arsenal","Aston","Barkley","Basel","Brazil","Cahill","Cup","England","Euro","Liverpool","Manchester","Norway","Sterling","wayne_rooney",
"Switzerland","Uruguay","World","apathy","appointment","atmosphere","attacker","back","brilliantly","busy","captain","celebrate", "comprehensively","decisive","defeat","display","eliminate","encouragement","exit","glamorous","imagination","opponent","partnership",
"penalty","performance","play","player","positive","preparation","pressure","prove","public","retire","summer","surreal", "team", "winner","worry","victory", "young"]

SMALL_SEED=["America","Arsenal","Brazil","Cup","England","wayne_rooney","appointment","atmosphere",
"attacker","back","brilliantly","busy","captain","celebrate"]
#,"defeat","eliminate","encouragement","exit",
#"penalty","performance","play","player","positive","preparation","pressure","prove","public",
# "team", "winner","worry","victory", "young"


#####################################################################
#DEPRECATED
#####################################################################

#read_concepts(filename="data/sample")


#print(cn5.get_similarity('sport','wayne_rooney'))

#for e in (cn5.search_edges(start="/c/en/sport",limit=10,toto="bouh")):
#	e.print_edge()

#for e in (cn5.search_edges_from("hockey")):
#	e.print_edge()

#print(cn5.get_similar_concepts('america'))
#for e in cn5.search_edges(start="/c/en/america"):
#	e.print_edge()

#print(cn5.get_similarity(concept1="democracy",concept2="sport"))

def expand_by_similarity(concept,network):
	"""
	network : Network object
	"""
	concepts=cn5.get_similar_concepts(concept)
	for c in concepts:
		if not network.has_node(c[0]):
			conceptic=polysemy(c[0])
			if conceptic==0:#TODO : check if it's a name
				conceptic=7
			network.add_node(id=c[0],ic=conceptic)
		edge=cn5.search_edge(start=concept,end=c[0])
		if edge:
			network.add_edge(fromId=concept,toId=edge.end,w=edge.weight/5,r=edge.rel)
		else:
			network.add_edge(fromId=concept,toId=c[0],w=c[1],r='SimilarTo')

def create_node(concept,network):
	if not network.has_node(concept):
		conceptic=polysemy(concept)
		if conceptic==0:#TODO : check if it's a name
			conceptic=7
		network.add_node(id=concept,ic=conceptic)	

def test2():
	n=Network()
	seed=SMALL_SEED
	with open("data/sample_concepts.txt",'r') as file:
		seed=json.load(file)
	for word in seed[1:4]:
		conceptic=polysemy(word)
		if conceptic==0:#TODO : check if it's a name
			conceptic=7
		if not n.has_node(word):
			n.add_node(id=word,ic=conceptic)
			expand_by_similarity(word,n)
	n.save_to_JSON_stream("network_example/network_example_6")
	n.draw("network_example/network_example_6.png")


MINIMUM_SIMILARITY=0.1

def expand_by_similarity_to(concept,network,filter):
	edges=cn5.search_edges_from(concept)
	for e in edges:
		sim=cn5.get_similarity(e.end,filter)
		if sim>MINIMUM_SIMILARITY and e.end != concept:
			create_node(e.end,network)
			network.add_edge(fromId=concept,toId=e.end,w=e.weight/5,r=e.rel)


def remove_not_activated(network):
	for n in network.network.node:
		if n['a'] ==0:
			network.remove_node(n)


def expand_with_conceptnetwork(concept,network):
	edges=cn5.search_edges(minWeight=2,start='/c/en/'+concept)
	for e in edges:
		if e.end != concept:
			create_node(e.end,network)
			network.add_edge(fromId=concept,toId=e.end,w=e.weight*20,r=e.rel)
	concepts=cn5.get_similar_concepts(concept=concept,limit=4)
	for c in concepts:
		if not network.has_node(c[0]):
			conceptic=polysemy(c[0])
			if conceptic==0:#TODO : check if it's a name
				conceptic=7
			network.add_node(id=c[0],ic=conceptic)
		edge=cn5.search_edge(start=concept,end=c[0])
		if edge:
			network.add_edge(fromId=concept,toId=edge.end,w=edge.weight/5,r=edge.rel)
		else:
			network.add_edge(fromId=concept,toId=c[0],w=c[1],r='SimilarTo')		


def remove_leaves(network):
	tosuppr=[]
	for n in network.network.node:
		has_succ=False
		for s in network.successors(n):
			has_succ=True
			pass
		if not has_succ:
			tosuppr.append(n)
	for n in tosuppr:
		network.remove_node(n)

def test3():
	n=Network()
	seed=SMALL_SEED	
	with open("data/sample_concepts.txt",'r') as file:
		seed=json.load(file)
	for word in seed:
		create_node(word,n)
		expand_by_similarity_to(word,n,filter="sport")
	n.save_to_JSON_stream("network_example/network_example_6")
	n.draw("network_example/network_example_6.png")

def test4():
	n=Network()
	seed=SMALL_SEED	
	with open("data/sample_concepts.txt",'r') as file:
		seed=json.load(file)
	for word in seed[1:10]:
		create_node(word,n)
		expand_by_similarity(word,n)
	n.save_to_JSON_stream("network_example/network_example_6")
	n.draw("network_example/network_example_6.png")

#print(cn5.get_similar_concepts_by_term_list(term_list=["america"]))


def test5():
	n=Network()
	seed=SMALL_SEED	
	with open("data/sample_concepts.txt",'r') as file:
		seed=json.load(file)
	print("etape 1...")
	for word in seed:
		create_node(word,n)
		n[word]['a']=50
		expand_with_conceptnet(word,n)
	print("activating...")
	activate_all_linked(n)
	print("etape 2...")
	temp=n.network.node.copy()
	for word in temp:
		if word not in seed and n[word]['a'] != 0:
			expand_with_conceptnet(word,n)
	print("activating...")
	activate_all_linked(n)
	print("saving...")
	n.save_to_JSON_stream("network_example/network_example_6")
	n.draw("network_example/network_example_6.png")


def test6():
	n=Network()
	n.load_from_JSON_stream(nodes_files=["network_example/network_example_6_nodes.jsons"],
		edges_files=["network_example/network_example_6_edges.jsons"])
	activate_all_linked(n)
	remove_not_activated(n)
	n.save_to_JSON_stream("network_example/network_example")
	n.draw("network_example/network_example.png")

#####################################################################




def create_node(concept,network):
	if not network.has_node(concept):
		conceptic=polysemy(concept)
		if conceptic==0:#TODO : check if it's a name
			conceptic=7
		network.add_node(id=concept,ic=conceptic)	
		return True
	return False


def remove_not_activated(network):
	temp=network.network.node.copy()
	for n in temp:
		if network[n]['a'] ==0:
			network.remove_node(n)


def expand_with_conceptnet(concept,network):
	#1 : expand with traditional links
	edges=cn5.search_edges(minWeight=1.8,start='/c/en/'+concept)
	for e in edges:
		if e.end != concept:
			create_node(e.end,network)
			if not network.has_edge(concept,e.end):
				network.add_edge(fromId=concept,toId=e.end,w=e.weight*20,r=e.rel)
	#2 : expand by similarity
	concepts=cn5.get_similar_concepts(concept=concept,limit=3)
	for c in concepts:
		if not network.has_node(c[0]):
			create_node(c[0],network)
		#edge=cn5.search_edge(start=concept,end=c[0])
		#if edge:
		#	network.add_edge(fromId=concept,toId=edge.end,w=edge.weight/5,r=edge.rel)
		#else:
			if not network.has_edge(concept,c[0]):
				network.add_edge(fromId=concept,toId=c[0],w=c[1]*70,r='SimilarTo')		

def activate_all_linked(network):
	for n in network.network.node:
		if network[n]['a']==0:
			has_linked=False
			for s in network.successors(n):
				has_linked=True
				pass
			elts=0
			for s in network.predecessors(n):
				elts+=1
				if elts>1:
					has_linked=True
					pass
			if has_linked:
				network[n]['a']=50




def add_to_network(nextname=None,seedname="data/sample.txt",networkname="network_example/network_example"):
	n=Network()
	seed=[]	
	with open(seedname,'r') as file:
		seed=json.load(file)
	n.load_from_JSON_stream(nodes_files=[networkname+"_nodes.jsons"],
		edges_files=[networkname+"_edges.jsons"])		
	previous=n.network.node.copy()
	print("etape 1...")
	for word in seed:
		create_node(word,n)
		n[word]['a']=50
		expand_with_conceptnet(word,n)
	print("activating...")
	activate_all_linked(n)
	print("etape 2...")
	temp=n.network.node.copy()
	for word in temp:
		if word not in previous and word not in seed and n[word]['a'] != 0:
			expand_with_conceptnet(word,n)
	print("activating...")
	activate_all_linked(n)
	print("saving...")	
	if not nextname:
		nextname=networkname+"2"
	n.save_to_JSON_stream(nextname)
	n.draw(filename=nextname+".png")



add_to_network(seedname="data/concepts.txt",networkname="network_example/network_example",
	nextname="network_example/network_example_2")
