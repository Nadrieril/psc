from abstracter.parsers.normalize import retrieve_words_only,retrieve_names_only
from abstracter.parsers.tokenizer import get_named_entities
from abstracter.util.json_stream import *
import json
import os


#def parse_article_2(filename):
#	with open(filename,'r') as file:
#		return (retrieve_concepts(file.read())
#	return []


def parse_article(filename):
	with open(filename,'r') as file:
		text=file.read() 
		return [retrieve_words_only(text),retrieve_names_only(text)]
	return []


DEFAULT_DATA_DIRECTORY="crawlerpsc/2014_12_04/"
DEFAULT_RESULTS_DIRECTORY="concepts/2014_12_04/"
DEFAULT_CONCEPTS_FILE="all_concepts.jsons"
DEFAULT_NAMES_FILE="all_names.jsons"

def parse_directory(max_subdirectories=10,max_files=100,data_directory=DEFAULT_DATA_DIRECTORY,
	results_directory=DEFAULT_RESULTS_DIRECTORY):
	if not os.path.isdir(results_directory):
		os.makedirs(results_directory)
	i=0
	j=0
	while(os.path.exists(data_directory+"%i/%i" % (i,j)) and i<max_subdirectories):
		while(os.path.exists(data_directory+"%i/%i" % (i,j)) and j<max_files):
			temp=parse_article(data_directory+"%i/%i" % (i,j))
			if temp:
				with open(results_directory+"%i_%i_concepts.json" % (i,j),'w') as file:
					json.dump(temp[0],file)
				with open(results_directory+"%i_%i_names.json" % (i,j),'w') as file:
					json.dump(temp[1],file)
					print("successful with : "+data_directory+"%i/%i" % (i,j))
			j+=1
		j=0
		i+=1




def unify_all_names(directory=DEFAULT_RESULTS_DIRECTORY,max_files=10,
	names_file=DEFAULT_NAMES_FILE):
	"""
	Retrieve all names and put them into a single dict.
	The value associated to each name represents the number of articles in which it appears.
	The result is put into a single jsonstream.
	max_files : maximum number of files to analyze in the directory.
	"""
	i=0
	j=0
	all_names={}
	k=0
	while(os.path.exists(directory+"%i_%i_names.json" % (i,j)) and k<max_files):
		while(os.path.exists(directory+"%i_%i_names.json" % (i,j)) and k<max_files):
			k+=1
			temp=[]
			with open(directory+"%i_%i_names.json" % (i,j),'r') as file:
				temp=json.load(file)
				print("successful loading of "+directory+"%i/%i" % (i,j))
			if temp:
				for c in temp:
					if c in all_names:
						all_names[c]+=1
					else:
						all_names[c]=1
			j+=1
		j=0
		i+=1	
	writer=JSONStreamWriter(names_file)
	for d in all_names.items():
		writer.write(d)
	writer.close()


def unify_all_concepts(directory=DEFAULT_RESULTS_DIRECTORY,max_files=10,
	concepts_file=DEFAULT_CONCEPTS_FILE):
	"""
	Retrieve all concepts and put them into a single dict.
	The result is put into a single jsonstream.
	max_files : maximum number of files to analyze in the directory.
	"""
	i=0
	j=0
	all_concepts={}
	k=0
	while(os.path.exists(directory+"%i_%i_concepts.json" % (i,j)) and k<max_files):
		while(os.path.exists(directory+"%i_%i_concepts.json" % (i,j)) and k<max_files):
			k+=1
			temp=[]
			with open(directory+"%i_%i_concepts.json" % (i,j),'r') as file:
				temp=json.load(file)
				print("successful loading of "+directory+"%i/%i" % (i,j))
			if temp:
				for c in temp:
					if c in all_concepts:
						all_concepts[c]+=temp[c]
					else:
						all_concepts[c]=temp[c]
			j+=1
		j=0
		i+=1	
	writer=JSONStreamWriter(concepts_file)
	for d in all_concepts.items():
		writer.write(d)
	writer.close()

def fusion(max_files=1000):
	directory="crawler_concepts/2014_12_04/"
	concept_file="concepts2.jsons"
	i=0
	j=0
	all_concepts={}
#	with open("concepts.jsons") as file:
	for c in read_json_stream("concepts.jsons"):
		all_concepts[c[0]]=c[1]
	k=0
	while(os.path.exists(directory+"%i_%i.json" % (i,j)) and k<max_files):
		while(os.path.exists(directory+"%i_%i.json" % (i,j)) and k<max_files):
			k+=1
			temp=[]
			with open(directory+"%i_%i.json" % (i,j),'r') as file:
				temp=json.load(file)
				print("successful loading of "+directory+"%i/%i" % (i,j))
			if temp:
				for c in temp:
					if c in all_concepts:
						all_concepts[c]+=1
					else:
						all_concepts[c]=0
			j+=1
		j=0
		i+=1	
	writer=JSONStreamWriter(concept_file)
	for d in all_concepts.items():
		writer.write(d)
	writer.close()

###################################################
####EXAMPLE
###################################################

#parse_directory(max_subdirectories=10,max_files=100,data_directory="crawlerpsc/2014_12_05/",results_directory="concepts/2014_12_05/")
#unify_all_names(directory="concepts/2014_12_05/",max_files=1000,names_file="all_names_2014_12_05.jsons")
#unify_all_concepts(directory="concepts/2014_12_05/",max_files=1000,concepts_file="all_concepts_2014_12_05.jsons")



