from abstracter.parsers.retriever import retrieve_words_names
from abstracter.util.json_stream import *
import json
import os


def parse_article(filename):
	with open(filename,'r') as file:
		text=file.read() 
		return retrieve_words_names(text)
	return []


DEFAULT_DATA_DIRECTORY="crawlerpsc/"
DEFAULT_RESULTS_DIRECTORY="concepts/"
CONCEPTS_NAMES_DATA_DIRECTORY="concepts_names_data/"
#DEFAULT_CONCEPTS_FILE="all_concepts.jsons"
#DEFAULT_NAMES_FILE="all_names.jsons"

def parse_directory(max_subdirectories=10,max_files=100,data_directory=DEFAULT_DATA_DIRECTORY,
	results_directory=DEFAULT_RESULTS_DIRECTORY,subdirectory="2014_12_04"):
	if not os.path.isdir(results_directory+subdirectory+"/"):
		os.makedirs(results_directory+subdirectory+"/")
	i=0
	j=0
	while(os.path.exists(data_directory+"%s/%i/%i" % (subdirectory,i,j)) and i<max_subdirectories):
		while(os.path.exists(data_directory+"%s/%i/%i" % (subdirectory,i,j)) and j<max_files):
			temp=parse_article(data_directory+"%s/%i/%i" % (subdirectory,i,j))
			if temp:
				with open(results_directory+"%s/%i_%i_concepts.json" % (subdirectory,i,j),'w') as file:
					json.dump(temp[0],file)
				with open(results_directory+"%s/%i_%i_names.json" % (subdirectory,i,j),'w') as file:
					json.dump(temp[1],file)
					print("successful with : "+data_directory+"%s/%i/%i" % (subdirectory,i,j))
			j+=1
		j=0
		i+=1




def unify_all_names(directory=DEFAULT_RESULTS_DIRECTORY,max_files=10,subdirectory="2014_12_04",
	names_file=None):
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
	while(os.path.exists(directory+"%s/%i_%i_names.json" % (subdirectory,i,j)) and k<max_files):
		while(os.path.exists(directory+"%s/%i_%i_names.json" % (subdirectory,i,j)) and k<max_files):
			k+=1
			temp=[]
			with open(directory+"%s/%i_%i_names.json" % (subdirectory,i,j),'r') as file:
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
	if not names_file:
		if not os.path.isdir(CONCEPTS_NAMES_DATA_DIRECTORY):
			os.makedirs(CONCEPTS_NAMES_DATA_DIRECTORY)
		names_file=CONCEPTS_NAMES_DATA_DIRECTORY+subdirectory+"_all_names.jsons"
	writer=JSONStreamWriter(names_file)
	for d in all_names.items():
		writer.write(d)
	writer.close()


def unify_all_concepts(directory=DEFAULT_RESULTS_DIRECTORY,max_files=10,subdirectory="2014_12_04",
	concepts_file=None):
	"""
	Retrieve all concepts and put them into a single dict.
	The result is put into a single jsonstream.
	max_files : maximum number of files to analyze in the directory.
	"""
	i=0
	j=0
	all_concepts={}
	k=0
	while(os.path.exists(directory+"%s/%i_%i_concepts.json" % (subdirectory,i,j)) and k<max_files):
		while(os.path.exists(directory+"%s/%i_%i_concepts.json" % (subdirectory,i,j)) and k<max_files):
			k+=1
			temp=[]
			with open(directory+"%s/%i_%i_concepts.json" % (subdirectory,i,j),'r') as file:
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
	if not concepts_file:
		if not os.path.isdir(CONCEPTS_NAMES_DATA_DIRECTORY):
			os.makedirs(CONCEPTS_NAMES_DATA_DIRECTORY)
		concepts_file=CONCEPTS_NAMES_DATA_DIRECTORY+subdirectory+"_all_concepts.jsons"	
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

from re import match
from glob import glob

def unify(directory=CONCEPTS_NAMES_DATA_DIRECTORY,max_files=10,names_file="names.jsons",concepts_file="concepts.jsons"):
	"""
	Unifies all dicts of concepts and list of names into two single files.
	Retrieves all data from the default directory, with a maximum number of files.
	Suppress bad characters.
	"""
	#(_, _, filenames) = os.walk(directory).next()
	filenames=glob(directory+"*names.jsons")[0:max_files]
	fileconcepts=glob(directory+"*concepts.jsons")[0:max_files]
	thedict={}
	for name in filenames:
		for c in read_json_stream(name):
			#avoid bad words
			if match('^[a-zA-Z\s-]*$',c[0]) and len(c[0]) < 20:
				if c[0] not in thedict:
					thedict[c[0]]=1
				else:
					thedict[c[0]]+=c[1]
		print("successful reading of :"+name)
	writer=JSONStreamWriter(names_file)
	for d in thedict.items():
		writer.write(d)
	writer.close()
	thedict={}
	for name in fileconcepts:
		for c in read_json_stream(name):
			#avoid bad words
			if match('^[a-zA-Z\s-]*$',c[0]) and len(c[0]) < 20:
				if c[0] not in thedict:
					thedict[c[0]]=1
				else:
					thedict[c[0]]+=c[1]
		print("successful reading of :"+name)
	writer=JSONStreamWriter(concepts_file)
	for d in thedict.items():
		writer.write(d)
	writer.close()





###################################################
####EXAMPLE
###################################################

#parse_directory(max_subdirectories=10,max_files=100,data_directory="crawlerpsc/2015_01_01/",results_directory="concepts/2015_01_01/")
#unify_all_names(subdirectory="2015_01_01",max_files=1000,names_file="all_names_2015_01_01.jsons")
#unify_all_concepts(directory="concepts/2014_12_04/",max_files=1000,concepts_file="all_concepts_2014_12_04.jsons")

#parse_directory(max_subdirectories=10,max_files=100,data_directory="crawlerpsc/",
#	results_directory="concepts/",subdirectory="2015_01_02")

#parse_directory(max_subdirectories=1,max_files=10,subdirectory="2015_01_03")
#unify_all_names(subdirectory="2015_01_03",max_files=1000)
#unify_all_concepts(subdirectory="2015_01_03",max_files=1000)

#unify()