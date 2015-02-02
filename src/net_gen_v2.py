import abstracter.conceptnet5_client.api.concurrent_api as ca
from abstracter.concepts_network import ConceptNetwork
from abstracter.util import json_stream as js
from abstracter.conceptnet5_client.api import api as cn5
import abstracter.freebase_client as fb
import re
from abstracter.conceptnet5_client.api.result import *
import os

"""
Generate network from a file, maybe adding nodes to another already existing network.
"""
####################################



NAME_IC=80#on 100
OTHER_IC=40#on 100
DEFAULT_IC=40


DATA_DIR="concepts_names_data/"
NETWORK=ConceptNetwork()
BL=set()
SL=set()

################################
#utils
############################
def polysemy(word):
	return len(wnc.synsets(word,pos=None)) 


def create_node(concept,ic=DEFAULT_IC,a=0):
	if not NETWORK.has_node(concept):
		NETWORK.add_node(id=concept,ic=ic,a=a)	
		return True
	return False

def create_edge(fromId,toId,weight,rel):
	if not NETWORK.has_edge(fromId=fromId,toId=toId):
		NETWORK.add_edge(fromId=fromId,toId=toId,w=weight,r=rel)
		return True
	return False

def add_list(the_list,word):
	if word not in the_list:
		#the_list.append(word)
		the_list.add(word)



################################
###expand methods
###################################

def expand_names(words,from_existing=False,to_existing=False):
	"""
	Warning : words is a dict or a list
	"""
	temp=not(type(words) is list)
	try:
		dict=fb.search_names(list(word for word in words))
	except Exception as e:
		print("Warning, exception :")
		print(e)
		dict={}
	for word in dict:
		data=dict[word]
		if data:
			if not from_existing:	
				add_list(SL,word)
				#SL.append(word)
			weight=100*data['score']/(data['score']+200)#between 0 and 100
			if len(data['from'])<40:
				if not from_existing:	
					create_node(concept=data['from'],ic=int(min(NAME_IC+(words[word] if temp else 0),100)),a=100)
				if 'to' in data and data['to'] and len(data['to'])<30:
					if not(to_existing) or NETWORK.has_node(data['to']):
						create_node(concept=data['to'],a=0)
						create_edge(fromId=data['from'],toId=data['to'],weight=int(weight),rel="IsA")
		else:
			add_list(BL,word)
			#BL.append(word)


def expand_edges(words,from_existing=False,to_existing=False):
	"""
	Warning : words is a dict or a list
	"""
	temp=not(type(words) is list)
	try:
		dict=ca.search_edges_from(list(word for word in words),filter='/c/en/',minWeight=1.3,limit=10)
	except Exception as e:
		print("Warning, exception :")
		print(e)
		dict={}
	for word in dict:
		edges=dict[word]
		if edges:
			if not from_existing:	
				add_list(SL,word)
				#SL.append(word)
				create_node(word,ic=int(min(OTHER_IC+(words[word] if temp else 0),100)),a=100)
		else:
			add_list(BL,word)
			#BL.append(word)
		for e in edges:
			if e.end != word and len(e.end)<30:
				if not(to_existing) or NETWORK.has_node(e.end):
					create_node(e.end,ic=int(min(OTHER_IC,100)),a=0)
					create_edge(fromId=word,toId=e.end,weight=int(min(e.weight*30,100)),rel=e.rel)

def expand_lookup(words,from_existing=False,to_existing=False):
	"""
	Warning : words is a dict, or a list
	"""
	temp=not(type(words) is list)
	try:
		dict=ca.search_concepts(list(word for word in words),filter='/c/en/',limit=10)
	except Exception as e:
		print("Warning, exception :")
		print(e)
		dict={}
	for word in dict:
		edges=dict[word]
		if edges:
			if not from_existing:
				add_list(SL,word)	
				#SL.append(word)
				create_node(word,ic=int(min(OTHER_IC+(words[word] if temp else 0),100)),a=100)
		else:
			add_list(BL,word)
			#BL.append(word)
		for e in edges:
			if e.start != word and len(e.start)<30:
				if not(from_existing) or NETWORK.has_node(e.start):
					create_node(e.start,ic=int(min(OTHER_IC,100)),a=0)	
			if e.end != word and len(e.end)<30:
				if not(to_existing) or NETWORK.has_node(e.end):
					create_node(e.end,ic=int(min(OTHER_IC,100)),a=0)
			if NETWORK.has_node(e.start) and NETWORK.has_node(e.end):
				create_edge(fromId=e.start,toId=e.end,weight=int(min(e.weight*30,100)),rel=e.rel)


def expand_similarity(words,from_existing=False,to_existing=False):
	"""
	Warning : words is a dict or a list
	"""
	try:
		dict=ca.get_similar_concepts(words,limit=3,filter='/c/en/')
	except Exception as e:
		dict={}
		print("Warning, exception :")
		print(e)
	for word in dict:
		concepts=dict[word]
		if concepts:
			add_list(SL,word)
			#SL.append(word)
		else:
			add_list(BL,word)
			#BL.append(word)
		for c in concepts:
			if c[0] !=word and len(c[0])<30:
				if not from_existing:
					create_node(c[0],ic=DEFAULT_IC,a=0)
				if not(to_existing) or NETWORK.has_node(c[0]):
					create_node(c[0],ic=DEFAULT_IC,a=0)
					create_edge(fromId=word,toId=c[0],weight=int(min(c[1]*70,100)),rel='SimilarTo')	


###############################################
##network treatment
############################################""
def tag_linked_nodes(limit=1000):
	k=0
	q=0
	print("tag linked nodes on current network...")
	for n,d in NETWORK.nodes():
		k+=1
		if NETWORK[n]['a'] <100 and len(list(NETWORK.predecessors(n)))+len(list(NETWORK.successors(n))) > 1:
			NETWORK[n]['a']=100
			q+=1
			if q%100==0:
				print(q.__str__()+" nodes reactivated !")
		if k%500==0:
			print(k.__str__()+" nodes looked !")
		if k>limit:
			break
	print(k.__str__()+" nodes looked !")
	print(q.__str__()+" nodes reactivated !")	


def tag_much_linked_nodes(limit=1000):
	k=0
	q=0
	print("tag linked nodes on current network...")
	for n,d in NETWORK.nodes():
		k+=1
		if NETWORK[n]['a'] <100 and len(list(NETWORK.predecessors(n))) > 1:
			NETWORK[n]['a']=100
			q+=1
			if q%100==0:
				print(q.__str__()+" nodes reactivated !")
		if k%500==0:
			print(k.__str__()+" nodes looked !")
		if k>limit:
			break	
	print(k.__str__()+" nodes looked !")
	print(q.__str__()+" nodes reactivated !")

def clear_nodes(filter='a',limit=1000):
	k=0
	q=0
	print("clear nodes on current network with filter "+filter)
	for n in NETWORK.nodes().copy():
		k+=1
		if NETWORK[n[0]][filter]==0:
			NETWORK.remove_node(n[0])
			q+=1
			if q%200==0:
				print(q.__str__()+" nodes removed !")
		if k%5000==0:
			print(k.__str__()+" nodes looked !")
		if k>limit:
			break
	print(k.__str__()+" nodes looked !")
	print(q.__str__()+" nodes removed !")	

def clear_ic(limit):
	clear_nodes(filter='ic',limit=limit)

def clear_act(limit):
	clear_nodes(filter='a',limit=limit)


def deactivate_nodes(limit=1000):
	print("deactivate nodes...")
	k=0
	for n in NETWORK.nodes():
		NETWORK[n[0]]['a']=0
		k+=1
		if k%500==0:
			print(k.__str__()+" nodes looked !")
		if k>limit:
			break


##########################################


def use_method_on_file(file,expand_method,max,to_existing,from_existing):
	"""
	param expand_method : the method to use
	it has to take words as argument, plus to_existing, from_existing
	"""
	print("Using method "+expand_method.__name__+" on file "+file.__repr__()+"...")
	print("to_existing_nodes : "+to_existing.__str__()+", from_existing : "\
		+from_existing.__str__())
	dict={}
	k=0
	for w in js.read_json_stream(file):
		if re.match('^[a-zA-Z\s-]*$',w[0]) and len(w[0])<20 and w[1]>0 and not w[0] in SL \
		and not w[0] in BL and not NETWORK.has_node(w[0]):
			dict[w[0]]=w[1]
			k+=1
			if len(dict)>500:
				expand_method(words=dict,to_existing=to_existing,from_existing=from_existing)
				dict={}
			if k>max:
				break
	if len(dict)>0:
		expand_method(words=dict,to_existing=to_existing,from_existing=from_existing)
	print("Looked at "+k.__str__()+" elements.")


def use_method_on_network(expand_method,max,to_existing,from_existing,not_act_only=False):
	"""
	param expand_method : the method to use
	"""
	print("Using method "+expand_method.__name__+" on current network...")
	print("to_existing_nodes : "+to_existing.__str__()+", from_existing : "\
		+from_existing.__str__()+", not activated only :"+not_act_only.__str__())
	list=[]
	k=0
	for n,d in NETWORK.nodes():
		if not_act_only:
			if d['a']==0:
				list.append(n)
		else:
			list.append(n)
		k+=1
		if len(list)>500:
			expand_method(words=list,to_existing=to_existing,from_existing=from_existing)
			list=[]
		if k>max:
			break
	if len(list)>0:
		expand_method(words=list,to_existing=to_existing,from_existing=from_existing)	
	print("Looked at "+k.__str__()+" nodes.")

####################################################

def load_dir(name):
	print("Loading network "+name+"...")
	NETWORK.load_from_JSON_stream(nodes_files=[name+"/"+name+"_nodes.jsons"],\
		edges_files=[name+"/"+name+"_edges.jsons"])
	for n in js.read_json_stream(name+"/"+name+"_black_list.jsons"):
		add_list(BL,n[0])#BL.append(n)
	for n in js.read_json_stream(name+"/"+name+"_success_list.jsons"):
		add_list(SL,n[0])
		#SL.append(n)

def save_dir(name):
	print("Saving to network "+name+"...")
	if not os.path.isdir(name):
		os.makedirs(name)
	NETWORK.save_to_JSON_stream(name+"/"+name)
	js.write_json_stream(list(BL),name+"/"+name+"_black_list.jsons")
	js.write_json_stream(list(SL),name+"/"+name+"_success_list.jsons")	

def print_network_status():
	print("Current network has %i nodes and %i edges." % (len(NETWORK.nodes()),len(NETWORK.edges())))
	print("Current black list has %i entries" % (len(BL)))
	print("Current success list has %i entries\n\n" % (len(SL)))
	

##############################
###script
###petite soupe de méthodes à tester, pour voir ce qui marche le mieux
#4 méthodes : expand_edges, expand_names, expand_lookup, expand_similarity
#4 techniques différentes
#dans chaque appel, arguments : faut-il considérer uniquement les noeuds non activés (non taggés) ?
#faut-il considérer uniquement les liens vers des noeuds existants  ou partant de noeuds existants ?
#########################

##example for creating a small network

#import sys
#oldout=sys.stdout
#sys.stdout = open('log.txt', 'w')
#print_network_status()
#use_method_on_file(DATA_DIR+"names.jsons",expand_names,max=1000,to_existing=False,from_existing=False)
#print_network_status()
#use_method_on_file(DATA_DIR+"concepts.jsons",expand_lookup,max=1000,to_existing=False,from_existing=False)
#print_network_status()
#tag_linked_nodes(limit=100000)
#clear_ic(limit=100000)
#clear_act(limit=100000)
#deactivate_nodes(limit=10000)
#print_network_status()
#save_dir("test")

##end of example


load_dir("wayne_3")


#use_method_on_network(expand_similarity,max=5000,to_existing=False,from_existing=False,not_act_only=False)

#use_method_on_network(expand_edges,max=500,to_existing=False,from_existing=True,not_act_only=False)
#print_network_status()

#use_method_on_network(expand_edges,max=30000,to_existing=False,from_existing=False,not_act_only=True)
#print_network_status()

#use_method_on_network(expand_similarity,max=5000,to_existing=False,from_existing=False,not_act_only=False)


#tag_linked_nodes(limit=100000)


#clear_ic(limit=100000)
#clear_act(limit=100000)
#deactivate_nodes(limit=100000)
#print_network_status()


save_dir("wayne_4")
