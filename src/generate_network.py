from abstracter.concepts_network import ConceptNetwork
from abstracter.util import json_stream as js
from abstracter.conceptnet5_client.api import api as cn5
import abstracter.freebase_client as fb
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


def expand_by_conceptnet(network,word,importance):
	tag=False
	#1 : expand with traditional links
	try:
		edges=cn5.search_edges(minWeight=1.5,start='/c/en/'+word)
	except Exception as e:
		print("Warning, exception ")
		edges=[]
	#create the node, by the way
	if edges:
		tag=True
		create_node(word,ic=int(min(OTHER_IC+importance,100)),network=network,a=100)
	else:
		return False
	for e in edges:
		if e.end != word and len(e.end)<30:
			create_node(e.end,ic=int(min(OTHER_IC,100)),network=network,a=0)
			if not network.has_edge(word,e.end):
				network.add_edge(fromId=word,toId=e.end,w=int(min(e.weight*30,100)),r=e.rel)
	#2 : expand by similarity
	try:
		concepts=cn5.get_similar_concepts(concept=word,limit=3)
	except Exception as e:
		concepts=[]
		print("Warning, exception :")
		print(e)
	if concepts:
		tag=True
	for c in concepts:
		if c[0] !=word and len(c[0])<30:
			create_node(c[0],ic=DEFAULT_IC,network=network,a=0)
	#edge=cn5.search_edge(start=concept,end=c[0])
	#if edge:
	#	network.add_edge(fromId=concept,toId=edge.end,w=edge.weight/5,r=edge.rel)
	#else:
			if not network.has_edge(word,c[0]):
				network.add_edge(fromId=word,toId=c[0],w=int(min(c[1]*70,100)),r='SimilarTo')	
	return tag


def expand_node(network,concept):
	"""
	Expands a node, but add edges only if they link to an already existing node.
	If such an edge is created, node's activation becomes 100, for us to "tag" it as relevant.
	If not, the node keeps its activation of 0, and it will be destroyed.
	The function uses conceptnet5 and freebase.
	"""
	tag=False
	#1 : expand with traditional links
	try:
		edges=cn5.search_edges(minWeight=1.5,start='/c/en/'+concept)
	except Exception as e:
		print("Warning, exception : ")
		print(e)
		edges=[]
	for e in edges:
		if e.end != concept and len(e.end)<30 and network.has_node(e.end):
			tag=True
			network[concept]['a']=100
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
		if c[0] !=concept and len(c[0])<30 and network.has_node(c[0]):
			tag=True
			network[c[0]]['a']=100
			if not network.has_edge(concept,c[0]):
				network.add_edge(fromId=concept,toId=c[0],w=int(min(c[1]*70,100)),r='SimilarTo')
	try:
		data=fb.search_name(concept)
	except Exception as e:
		data={}
		print("Warning, exception :")
		print(e)
	if data:
		if 'to' in data and data['to'] and len(data['to'])<30 and network.has_node(data['to']):
			tag=True
			network[concept]['a']=100
			if not network.has_edge(data['from'],data['to']):
				weight=100*data['score']/(data['score']+200)#between 0 and 100
				network.add_edge(fromId=data['from'],toId=data['to'],w=int(weight),r="IsA")		
	return tag	


###############################################
##network treatment
############################################""

def expand_nodes(network,limit=1000):
	k=0
	q=0
	for n,d in network.nodes():
		k+=1
		if d['a']==0:
			if expand_node(network,n):
				q+=1
				if q%10==0:
					print(q.__str__()+" nodes expanded !")
		if k%10==0:
			print(k.__str__()+" nodes looked !")
		if k>limit:
			break

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

def clear_nodes(network,limit=1000):
	k=0
	q=0
	for n in network.nodes().copy():
		k+=1
		if network[n[0]]['a']==0:
			network.remove_node(n[0])
			q+=1
		if q%200==0:
			print(q.__str__()+" nodes removed !")
		if k%5000==0:
			print(k.__str__()+" nodes looked !")

		if k>limit:
			break	

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


def perform_operation(op,nodes_file,edges_file,result,limit=1000):
	print("loading...")
	n=ConceptNetwork()
	n.load_from_JSON_stream(nodes_files=[nodes_file],edges_files=[edges_file])
	print("searching...")
	op(n,limit)
	print("saving...")
	n.save_to_JSON_stream(result)
	print("done !")	



############################################
###adding a file
###########################################""

def add_file_to_network(file,network,expand_method,black_list,success_list,max):
	"""
	param expand_method : the method to use
	it has to take 3 arguments : network, concept/name/word and its importance
	param black_list : list of words to dismiss without searching
	"""
	print("adding...")
	k=0
	q=0
	for w in js.read_json_stream(file):
		k+=1
		#some verifications to do first
		if [w[0]] not in black_list and [w[0]] not in success_list:
			if re.match('^[a-zA-Z\s-]*$',w[0]) and len(w[0])<20 and w[1]>0 and not network.has_node(w[0]):
				q+=1
				if not expand_method(network=network,word=w[0],importance=w[1]):
					black_list.append(w[0])
				else:
					success_list.append(w[0])
				if q%10 ==0:
					print(q.__str__()+" queries done !")
		if k>max:
			break	


def add_to_network(nodes_file,edges_file,names_files,concepts_files,result,black_list=None,success_list=None,max=1000):
	"""
	SMALL NETWORK ONLY
	We use lists to keep the correct words (success_list) and the bad ones, which is not optimal.
	We use also a json_stream to save the black_list and success_list.
	It's because they are big lists, and it's more convenient not to write them down as a single JSON object
	param black_list : name of the file
	"""
	if not black_list:
		black_list=[]
	else:
		#with open(black_list,'r') as file:
		#	black_list=json.load(file)
		black_list=list(js.read_json_stream(black_list))
	if not success_list:
		success_list=[]
	else:
		#with open(success_list,'r') as file:
		#	success_list=json.load(file)
		success_list=list(js.read_json_stream(success_list))
	print("loading...")
	n=ConceptNetwork()
	if nodes_file and edges_file:
		n.load_from_JSON_stream(nodes_files=[nodes_file],edges_files=[edges_file])
	print("queries...")
	for f in names_files:
		add_file_to_network(f,network=n,expand_method=expand_by_freebase  ,black_list=black_list,success_list=success_list, max=max)
	for f in concepts_files:
		add_file_to_network(f,network=n,expand_method=expand_by_conceptnet,black_list=black_list,success_list=success_list, max=max)
	print("saving...")
	n.save_to_JSON_stream(result)
	js.write_json_stream(black_list,result+"_black_list.jsons")
	js.write_json_stream(success_list,result+"_success_list.jsons")
	#json.dumps(black_list,result+"_black_list.json")
	#json.dumps(success_list,result+"_success_list.jsons")
	print("done !")



DATA_DIR="concepts_names_data/"


#add_to_network(nodes_file="tchoupi_nodes.jsons",edges_file="tchoupi_edges.jsons",
#	names_files=[],concepts_files=["concepts.jsons"],
#	black_list="tchoupi_black_list.jsons",success_list="tchoupi_success_list.jsons",result="tchoupi",max=1000)


#perform_operation(op=tag_linked_nodes, nodes_file="tchoupi_nodes.jsons",edges_file="tchoupi_edges.jsons",
#	result="tchoupii",limit=1000)

#perform_operation(op=tag_linked_nodes, nodes_file="tchoupi_nodes.jsons",edges_file="tchoupi_edges.jsons",
#	result="tchoupii",limit=30000)

#perform_operation(op=expand_nodes, nodes_file="tchoupi_nodes.jsons",edges_file="tchoupi_edges.jsons",
#	result="tchoupii",limit=5000)

#perform_operation(op=tag_linked_nodes, nodes_file="tchoupii_nodes.jsons",edges_file="tchoupii_edges.jsons",
#	result="tchoupiii",limit=30000)

#perform_operation(op=clear_nodes, nodes_file="tchoupiii_nodes.jsons",edges_file="tchoupiii_edges.jsons",
#	result="tchoupiiii",limit=30000)

#perform_operation(op=deactivate_nodes, nodes_file="tchoupiiii_nodes.jsons",edges_file="tchoupiiii_edges.jsons",
#	result="tchoupiiii",limit=30000)