import abstracter.conceptnet5_client.api.parallel_api as pa
from abstracter.concepts_network import ConceptNetwork
from abstracter.util import json_stream as js
from abstracter.conceptnet5_client.api import api as cn5
import abstracter.freebase_client as fb
import re
from abstracter.conceptnet5_client.api.result import *
import os

"""
Generate network or expand it.
We use node activation to ping the nodes to keep.
"""


DATA_DIR="concepts_names_data/"
NETWORK_DIR="wayne2/"
OUTPUT_LOG="log.txt"

def polysemy(word):
	return len(wnc.synsets(word,pos=None)) 

NAME_IC=80#on 100
OTHER_IC=40#on 100
DEFAULT_IC=40



def create_node(concept,network,ic=DEFAULT_IC,a=0):
	if not network.has_node(concept):
		network.add_node(id=concept,ic=ic,a=a)	
		return True
	return False


def determine_word_ic(word):
	pass

def expand_by_freebase(network,word,importance):
	try:
		data=fb.search_name(word)
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
		return True
	else:
		return False


def expand_names(network,words,sl_writer=None,bl_writer=None):
	"""
	Warning : words is a dict
	"""
	#1 : expand with traditional links
	try:
		dict=fb.search_names(list(word for word in words))
	except Exception as e:
		print("Warning, exception :")
		print(e)
		dict={}
	#create the node, by the way
	for word in dict:
		data=dict[word]
		if data:
			if sl_writer:
				sl_writer.write([word])
			weight=100*data['score']/(data['score']+200)#between 0 and 100
			if len(data['from'])<40:
				create_node(concept=data['from'],ic=int(min(NAME_IC+words[word],100)),network=network,a=100)
				if 'to' in data and data['to'] and len(data['to'])<30:
					create_node(concept=data['to'],network=network,a=0)
					if not network.has_edge(data['from'],data['to']):
						network.add_edge(fromId=data['from'],toId=data['to'],w=int(weight),r="IsA")
		elif bl_writer:
			bl_writer.write([word])


def expand_edges(network,words,sl_writer=None,bl_writer=None):
	"""
	Warning : words is a dict
	"""
	#1 : expand with traditional links
	try:
		dict=pa.search_edges_from(list(word for word in words),filter='/c/en/',minWeight=1.5,limit=10)
	except Exception as e:
		print("Warning, exception :")
		print(e)
		dict={}
	#create the node, by the way
	for word in dict:
		edges=dict[word]
		if edges:
			if sl_writer:
				sl_writer.write([word])
			create_node(word,ic=int(min(OTHER_IC+words[word],100)),network=network,a=100)
		elif bl_writer:
			bl_writer.write([word])
		for e in edges:
			if e.end != word and len(e.end)<30:
				create_node(e.end,ic=int(min(OTHER_IC,100)),network=network,a=0)
				if not network.has_edge(word,e.end):
					network.add_edge(fromId=word,toId=e.end,w=int(min(e.weight*30,100)),r=e.rel)	


def expand_similarity(network,words,sl_writer=None,bl_writer=None):
	"""
	Warning : words is a list
	"""
	#1 : expand with traditional links
	try:
		dict=pa.get_similar_concepts(words,limit=3,filter='/c/en/')
	except Exception as e:
		dict={}
		print("Warning, exception :")
		print(e)
	for word in dict:
		concepts=dict[word]
		#if concepts and sl_writer:
		#	sl_writer.write([word])
		#elif not concepts and bl_writer:
		#	bl_writer.write([word])
		for c in concepts:
			if c[0] !=word and len(c[0])<30:
				create_node(c[0],ic=DEFAULT_IC,network=network,a=0)
				if not network.has_edge(word,c[0]):
					network.add_edge(fromId=word,toId=c[0],w=int(min(c[1]*70,100)),r='SimilarTo')	


def expand_to_existing_nodes(network,words):
	"""
	Expands a node, but add edges only if they link to an already existing node.
	If such an edge is created, node's activation becomes 100, for us to "tag" it as relevant.
	If not, the node keeps its activation of 0, and it will be destroyed.
	The function uses conceptnet5 and freebase.
	"""
	try:
		dict=pa.search_edges_from(words,filter='/c/en/',minWeight=1.5,limit=10)
	except Exception as e:
		print("Warning, exception :")
		print(e)
		dict={}
	for word in dict:
		edges=dict[word]
		for e in edges:
			if e.end != word and len(e.end)<30 and network.has_node(e.end):
				network[word]['a']=100
				if not network.has_edge(word,e.end):
					network.add_edge(fromId=word,toId=e.end,w=int(min(e.weight*30,100)),r=e.rel)
	try:
		dict=fb.search_names(words)
	except Exception as e:
		print("Warning, exception :")
		print(e)
		dict={}
	#create the node, by the way
	for word in dict:
		data=dict[word]
		if data and network.has_node(data['from']):
			if 'to' in data and data['to'] and len(data['to'])<30 and network.has_node(data['to']):
				network[word]['a']=100
				if not network.has_edge(data['from'],data['to']):
					weight=100*data['score']/(data['score']+200)#between 0 and 100
					network.add_edge(fromId=data['from'],toId=data['to'],w=int(weight),r="IsA")	


def expand_to_new_nodes(network,words):
	"""
	Expands a node, but add edges only if they link to an already existing node.
	If such an edge is created, node's activation becomes 100, for us to "tag" it as relevant.
	If not, the node keeps its activation of 0, and it will be destroyed.
	The function uses conceptnet5 and freebase.
	"""
	try:
		dict=pa.search_edges_from(words,filter='/c/en/',minWeight=1.5,limit=10)
	except Exception as e:
		print("Warning, exception :")
		print(e)
		dict={}
	for word in dict:
		edges=dict[word]
		for e in edges:
			if e.end != word and len(e.end)<30 and network.has_node(e.end):
				network[word]['a']=100
				if not network.has_edge(word,e.end):
					create_node(e.end,ic=int(min(OTHER_IC,100)),network=network,a=0)
					network.add_edge(fromId=word,toId=e.end,w=int(min(e.weight*30,100)),r=e.rel)
	try:
		dict=fb.search_names(words)
	except Exception as e:
		print("Warning, exception :")
		print(e)
		dict={}
	#create the node, by the way
	for word in dict:
		data=dict[word]
		if data:
			if 'to' in data and data['to'] and len(data['to'])<30:
				if not network.has_edge(data['from'],data['to']):
					create_node(concept=data['to'],network=network,a=0)
					weight=100*data['score']/(data['score']+200)#between 0 and 100
					network.add_edge(fromId=data['from'],toId=data['to'],w=int(weight),r="IsA")	



def expand_nodes(network,words):
	"""
	Expands a node.
	If such an edge is created, node's activation becomes 100, for us to "tag" it as relevant.
	If not, the node keeps its activation of 0, and it will be destroyed.
	The function uses conceptnet5.
	"""
	try:
		dict=pa.search_edges_from(words,filter='/c/en/',minWeight=1.5,limit=10)
	except Exception as e:
		print("Warning, exception :")
		print(e)
		dict={}
	for word in dict:
		for e in edges:
			if e.end != word and len(e.end)<30 and network.has_node(e.end):
				network[concept]['a']=100
				if not network.has_edge(concept,e.end):
					network.add_edge(fromId=concept,toId=e.end,w=int(min(e.weight*30,100)),r=e.rel)




###############################################
##network treatment
############################################""


def tag_linked_nodes(network,limit=1000):
	k=0
	q=0
	for n,d in network.nodes():
		k+=1
		if network[n]['a'] <100 and len(list(network.predecessors(n)))+len(list(network.successors(n))) > 1:
			network[n]['a']=100
			q+=1
			if q%100==0:
				print(q.__str__()+" nodes reactivated !")
		if k%500==0:
			print(k.__str__()+" nodes looked !")
		if k>limit:
			break	

def tag_much_linked_nodes(network,limit=1000):
	k=0
	q=0
	for n,d in network.nodes():
		k+=1
		if network[n]['a'] <100 and len(list(network.predecessors(n))) > 1:
			network[n]['a']=100
			q+=1
			if q%100==0:
				print(q.__str__()+" nodes reactivated !")
		if k%500==0:
			print(k.__str__()+" nodes looked !")
		if k>limit:
			break	

def clear_nodes(network,filter='a',limit=1000):
	k=0
	q=0
	for n in network.nodes().copy():
		k+=1
		if network[n[0]][filter]==0:
			network.remove_node(n[0])
			q+=1
		if q%200==0:
			print(q.__str__()+" nodes removed !")
		if k%5000==0:
			print(k.__str__()+" nodes looked !")

		if k>limit:
			break	

def clear_ic(network,limit):
	clear_nodes(network,filter='ic',limit=limit)

def clear_act(network,limit):
	clear_nodes(network,filter='a',limit=limit)


def deactivate_nodes(network,limit=1000):
	k=0
	for n in network.nodes():
		network[n[0]]['a']=0
		k+=1
		if k%500==0:
			print(k.__str__()+" nodes looked !")
		if k>limit:
			break


##########################################



############################################
###adding a file
###########################################""

def use_method_on_file(file,network,expand_method,bl_writer,sl_writer,max):
	"""
	param expand_method : the method to use
	it has to take 2 arguments : network, words, optional : sl_writer and bl_writer
	param black_list : list of words to dismiss without searching
	"""
	dict={}
	k=0
	for w in js.read_json_stream(file):
		if re.match('^[a-zA-Z\s-]*$',w[0]) and len(w[0])<20 and w[1]>0 and not network.has_node(w[0]):
			dict[w[0]]=w[1]
			k+=1
			if len(dict)>500:
				expand_method(network=network,words=dict,bl_writer=bl_writer,sl_writer=sl_writer)
				dict={}
			if k>max:
				break
	if len(dict)>0:
		expand_method(network=network,words=dict,bl_writer=bl_writer,sl_writer=sl_writer)


def use_method_on_network(network,expand_method,max,not_act_only=False):
	"""
	param expand_method : the method to use
	it has to take 2 arguments : network, words (words is only a list)
	"""
	list=[]
	k=0
	for n,d in network.nodes():
		if not_act_only:
			if d['a']==0:
				list.append(n)
		else:
			list.append(n)
		k+=1
		if len(list)>500:
			expand_method(network=network,words=list)
			list=[]
		if k>max:
			break
	if len(list)>0:
		expand_method(network=network,words=list)	



def create_network(names_file,concepts_file,name,max=1000):
	"""
	Create new network from two files.
	"""
	if not os.path.isdir(NETWORK_DIR):
		os.makedirs(NETWORK_DIR)
	name=NETWORK_DIR+name
	bl_writer=js.JSONStreamWriter(name+"_black_list.jsons")
	sl_writer=js.JSONStreamWriter(name+"_success_list.jsons")
	n=ConceptNetwork()
	print("queries...")
	use_method_on_file(concepts_file,n,expand_edges,bl_writer,sl_writer,max)
	use_method_on_file(names_file,n,expand_names,bl_writer,sl_writer,max)
	use_method_on_network(n,expand_to_existing_nodes,max)
	print("saving...")
	n.save_to_JSON_stream(name)
	#use_method_on_network(n,expand_similarity,max)
	print("saving...")
	n.save_to_JSON_stream(name)
	tag_linked_nodes(n,limit=100000)
	#clear_nodes(n,limit=100000)
	#deactivate_nodes(n,limit=100000)
	print("saving...")
	n.save_to_JSON_stream(name)
	bl_writer.close()
	sl_writer.close()
	print("done !")

def initialize(names_file,concepts_file,name,max=1000):
	"""
	Create new network from two files.
	"""
	if not os.path.isdir(NETWORK_DIR):
		os.makedirs(NETWORK_DIR)
	name=NETWORK_DIR+name
	bl_writer=js.JSONStreamWriter(name+"_black_list.jsons")
	sl_writer=js.JSONStreamWriter(name+"_success_list.jsons")
	n=ConceptNetwork()
	print("queries...")
	use_method_on_file(concepts_file,n,expand_edges,bl_writer,sl_writer,max)
	use_method_on_file(names_file,n,expand_names,bl_writer,sl_writer,max)
	print("saving...")
	n.save_to_JSON_stream(name)
	#use_method_on_network(n,expand_similarity,max)
	print("saving...")
	n.save_to_JSON_stream(name)
	bl_writer.close()
	sl_writer.close()
	print("done !")	

def perform_operation(op,nodes_file,edges_file,result,limit=1000,not_act_only=False):
	print("loading...")
	n=ConceptNetwork()
	n.load_from_JSON_stream(nodes_files=[nodes_file],edges_files=[edges_file])
	print("performing operation : "+op.__str__())
	use_method_on_network(n,op,limit,not_act_only=not_act_only)
	print("saving...")
	n.save_to_JSON_stream(NETWORK_DIR+result)
	print("done !")	

def perform_net_operation(op,nodes_file,edges_file,result,limit=1000,not_act_only=False):
	print("loading...")
	n=ConceptNetwork()
	n.load_from_JSON_stream(nodes_files=[nodes_file],edges_files=[edges_file])
	print("performing network operation : "+op.__str__())
	op(n,limit)
	print("saving...")
	n.save_to_JSON_stream(NETWORK_DIR+result)
	print("done !")	

#create_network("names.jsons","concepts.jsons","tchoupi",max=200)

#initialize("names.jsons","concepts.jsons","wayne2",max=20000)

#perform_operation(expand_similarity,
#	"wayne2/wayne2_nodes.jsons","wayne2/wayne2_edges.jsons","wayne3",limit=10000)

#perform_operation(expand_to_existing_nodes,
#	"wayne2/wayne2_nodes.jsons","wayne2/wayne2_edges.jsons","wayne4",limit=100000,not_act_only=True)


#perform_net_operation(tag_linked_nodes,
#	"wayne2/wayne4_nodes.jsons","wayne2/wayne4_edges.jsons","wayne4",limit=100000)

#perform_net_operation(clear_ic,
#	"wayne2/wayne4_nodes.jsons","wayne2/wayne4_edges.jsons","wayne4",limit=100000)


#perform_operation(expand_to_new_nodes,
#	"wayne2/wayne5_nodes.jsons","wayne2/wayne5_edges.jsons","wayne5",limit=100000,not_act_only=True)

#perform_net_operation(tag_linked_nodes,
#	"wayne2/wayne5_nodes.jsons","wayne2/wayne5_edges.jsons","wayne5",limit=100000)

#perform_operation(tag_much_linked_nodes,
#	"wayne2/wayne5_nodes.jsons","wayne2/wayne5_edges.jsons","wayne5",limit=100000)


perform_net_operation(clear_act,
	"wayne2/wayne5_nodes.jsons","wayne2/wayne5_edges.jsons","wayne6",limit=100000)

#perform_operation(deactivate_nodes,
#	"wayne2/wayne5_nodes.jsons","wayne2/wayne5_edges.jsons","wayne5",limit=100000)

