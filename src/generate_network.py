from abstracter.concepts_network import Network
from abstracter.util import json_stream as js
from abstracter.conceptnet5_client.api import api as cn5
import abstracter.freebase_client as fb
import json
import os


"""
Generate network from scratch.
Use freebase, but do not cache its results. Use conceptnet5 and cache the results.
Using activation to ping the nodes to keep.
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


def create_node(concept,network,ic=DEFAULT_IC,a=0):
	if not network.has_node(concept):
		network.add_node(id=concept,ic=ic,a=a)	
		return True
	return False

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


#generate(max1=4000,max2=1000)

for e in cn5.search_edges_from("dog"):
	print(e)

def add_names_to_network(network):
	"""
	Select a file "all_names"
	"""
	pass

def add_concepts_to_network(network):

	pass


def add_to_network(network_files,names_files,concepts_files):
	"""
	Load network, add information, save network in the same file.
	"""
	pass