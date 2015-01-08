from abstracter.concepts_network import Network
from abstracter.util import json_stream as js
from abstracter.conceptnet5_client.api import api as cn5
import abstracter.freebase_client as fb
import json
import os
import re
from abstracter.conceptnet5_client.api.result import *

"""
Generate network or expand it.
We use node activation to ping the nodes to keep.
"""

def polysemy(word):
	return len(wnc.synsets(word,pos=None)) 

NAME_IC=80#on 100
OTHER_IC=40#on 100
DEFAULT_IC=40

def freebase_search(word,network,important=1):
	#print("searching for : "+word)
	data=fb.search_name(word)
	if data:
		weight=100*data['score']/(data['score']+200)#between 0 and 100
		create_node(concept=data['from'],ic=int(min(NAME_IC+important,100)),network=network,a=100)
		if 'to' in data and data['to']:
			create_node(concept=data['to'],network=network,a=0)
			network.add_edge(fromId=data['from'],toId=data['to'],w=int(weight),r="IsA")




def conceptnet_search(concept,network,important=1):
	#print("searching for : "+concept)
	#1 : expand with traditional links
	edges=cn5.search_edges(minWeight=1.8,start='/c/en/'+concept)
	for e in edges:
		if e.end != concept:
			create_node(e.end,ic=int(min(OTHER_IC+important,100)),network=network,a=100)
			if not network.has_edge(concept,e.end):
				network.add_edge(fromId=concept,toId=e.end,w=int(min(e.weight*30,100)),r=e.rel)
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
				network.add_edge(fromId=concept,toId=c[0],w=int(min(c[1]*70,100)),r='SimilarTo')		


def generate(names_file="data/names.jsons",concepts_file="data/concepts.jsons",max1=100,max2=100):
	network=Network()
	try:
		k=0
		for c in js.read_json_stream(names_file):
			k+=1
			freebase_search(c[0],network,important=c[1])
			print("reste "+ (max1-k).__str__())
			if k>max1:
				break
		k=0
		for c in js.read_json_stream(concepts_file):
			k+=1
			conceptnet_search(c[0],network,important=c[1])
			print("reste "+ (max2-k).__str__())
			if k>max2:
				break
	except Exception as e:
		print(type(e))
		print(e.args )
		pass
	network.save_to_JSON_stream("wayne")


def create_node(concept,network,ic=DEFAULT_IC,a=0):
	if not network.has_node(concept):
		network.add_node(id=concept,ic=ic,a=a)	
		return True
	return False


def determine_word_ic(word):
	pass

def expand_by_freebase(network,name,importance):
	try:
		data=fb.search_name(name)
	except Exception as e:
		data={}
		print("Warning, exception :")
		print(e)
	if data:
		weight=100*data['score']/(data['score']+200)#between 0 and 100
		if len(data['from'])<40:
			create_node(concept=data['from'],ic=int(min(NAME_IC+importance,100)),network=network,a=100)
			if 'to' in data and data['to'] and len(data['to'])<30:
				create_node(concept=data['to'],network=network,a=0)
				if not network.has_edge(data['from'],data['to']):
					network.add_edge(fromId=data['from'],toId=data['to'],w=int(weight),r="IsA")	


def expand_by_conceptnet(network,concept,importance):
	#1 : expand with traditional links
	try:
		edges=cn5.search_edges(minWeight=1.8,start='/c/en/'+concept)
	except Exception as e:
		print("Warning, exception ")
		edges=[]
	#create the node, by the way
	if edges:
		create_node(concept,ic=int(min(OTHER_IC+importance,100)),network=network,a=100)
	for e in edges:
		if e.end != concept and len(e.end)<30:
			create_node(e.end,ic=int(min(OTHER_IC,100)),network=network,a=0)
			if not network.has_edge(concept,e.end):
				network.add_edge(fromId=concept,toId=e.end,w=int(min(e.weight*30,100)),r=e.rel)
	#2 : expand by similarity
	try:
		concepts=cn5.get_similar_concepts(concept=concept,limit=3)
	except Exception as e:
		concepts=[]
		print("Warning, exception :")
		print(e)
	for c in concepts:
		if c[0] !=concept and len(c[0])<30:
			create_node(c[0],ic=DEFAULT_IC,network=network,a=0)
	#edge=cn5.search_edge(start=concept,end=c[0])
	#if edge:
	#	network.add_edge(fromId=concept,toId=edge.end,w=edge.weight/5,r=edge.rel)
	#else:
			if not network.has_edge(concept,c[0]):
				network.add_edge(fromId=concept,toId=c[0],w=int(min(c[1]*70,100)),r='SimilarTo')	

def add_concepts_to_network(file,network,max=1000):
	"""
	Select a file "all_concepts" and add them to the network.
	The file contains a json stream of ['word',importance] where importance is an int (number of occurrences)
	"""
	print("adding words...")
	k=0
	q=0
	for w in js.read_json_stream(file):
		k+=1
		#some verifications to do first
		if re.match('^[a-zA-Z\s-]*$',w[0]) and len(w[0])<20 and w[1]>0 and not network.has_node(w[0]):
			q+=1
			expand_by_conceptnet(network=network,concept=w[0],importance=w[1])
		if q%10 ==1:
			print(q.__str__()+" queries done !")
		if k>max:
			break

def add_names_to_network(file,network,max=1000):
	"""
	Select a file "all_names" and add them to the network.
	The file contains a json stream of ['word',importance] where importance is an int (number of occurrences)
	"""
	print("adding names...")
	k=0
	q=0
	for w in js.read_json_stream(file):
		k+=1
		if re.match('^[a-zA-Z\s-]*$',w[0]) and len(w[0])<20 and w[1]>0 and not network.has_node(w[0]):
			q+=1
			expand_by_freebase(network,name=w[0],importance=w[1])
		if q%10==1:
			print(q.__str__()+" queries done !")
		if k>max:
			break


def add_to_network(nodes_file,edges_file,names_files,concepts_files,result,max=1000):
	"""
	Load network, add information, save network in the same file.
	"""
	#loading
	print("loading...")
	n=Network()
	n.load_from_JSON_stream(nodes_files=[nodes_file],edges_files=[edges_file])
	print("queries...")
	for f in names_files:
		add_names_to_network(f,network=n,max=max)
	for f in concepts_files:
		add_concepts_to_network(f,network=n,max=max)
	print("saving...")
	n.save_to_JSON_stream(result)
	print("done !")

DATA_DIR="concepts_names_data/"

#add_to_network("wayne_nodes.jsons","wayne_edges.jsons",	names_files=[DATA_DIR+"2014_12_04_names.jsons"],
#	concepts_files=[DATA_DIR+"2014_12_04_concepts.jsons"],result="wayne")
#add_to_network("wayne_nodes.jsons","wayne_edges.jsons",	names_files=[DATA_DIR+"2015_01_04_all_names.jsons"],
#	concepts_files=[DATA_DIR+"2015_01_04_all_concepts.jsons"],result="wayne",max=300)

#if you are motivated (maybe 1 hour) :
add_to_network("wayne_nodes.jsons","wayne_edges.jsons",	names_files=["names.jsons"],
	concepts_files=["concepts.jsons"],result="wayne",max=2000)
