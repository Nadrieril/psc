from abstracter.parsers.normalize import retrieve_concepts
from abstracter.parsers.tokenizer import get_named_entities
from abstracter.util.json_stream import *
import json
import os

text="""

    
Virgil van Dijk has already scored six times for Celtic this seasonThe defender says his attacking instincts were helped by Johan CruyffHe scored his first goal at Parkhead against Partick Thistle on Wednesday 
Celtic defender Virgil van Dijk has revealed the attacking side of his game was indirectly influenced by the great Johan Cruyff.The Dutchman's talents as a centre-back have led to him being linked with a move to England in the January transfer window with Arsenal reportedly one of his suitors.However, he showed his prowess in the opposition penalty box against Partick Thistle on Wednesday night when he notched his sixth goal of the season - his first of his Hoops career at Parkhead - in the 1-0 home win to ease Celtic three points clear of Inverness at the top of the Scottish Premiership.      
    Dutch defender Virgil van Dijk has scored six times already so far for Celtic  this season      
    Van Dijk has revealed that his attacking flair is influenced by Holland legend Johan Cruyff (second left)The 23-year-old, who started his career as a youth at Willem II, claimed his sharpness in front of goal was honed as a kid playing on pitches named after Holland's most famous player -although he does not see his future as a striker.'I have never played as a striker regularly or anything but when I was younger I was always the winger or striker,' said the former Groningen player.'We have Johan Cruyff courts in Holland. They're small pitches where you play games of five-a-side.'The level is very high and a lot of professional footballers like to play there as well.'So that's what I did when I was younger and sometimes you can see it a little bit on the pitch.'But I love to defend as well, that's the main thing and the important thing for me.      
    Van Dijk (second left) is mobbed by his team-mates after scoring against Partick Thistle on Wednesday      
    Van Dijk's (centre) Celtic side are three points clear of Inverness at the top of the Scottish Premiership'I can't remember when I became a defender but when I was at Willem II I was a defender and I'm still a defender.'I want to be there for the rest of my career.'If I can score a goal and help the team and win games it's going to be fun as well.'Last year I think I had five in total and I always want to improve myself. I just want to win games and be a champion.'
    
    
    
    
  
"""

def parse_article(filename):
	with open(filename,'r') as file:
		return (retrieve_concepts(file.read()))
	return []


DEFAULT_DATA_DIRECTORY="crawlerpsc/2014_12_04/"
DEFAULT_RESULTS_DIRECTORY="crawler_concepts/2014_12_04/"
DEFAULT_CONCEPT_FILE="concepts.jsons"

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
				with open(results_directory+"%i_%i.json" % (i,j),'w') as file:
					json.dump(temp,file)
					print("successful with : "+data_directory+"%i/%i" % (i,j))
			j+=1
		j=0
		i+=1



def parse_files_and_retrieve_concepts(directory=DEFAULT_RESULTS_DIRECTORY,max_files=10,
	concept_file=DEFAULT_CONCEPT_FILE):
	"""
	Warning : concepts are put into a single list.
	"""
	i=0
	j=0
	all_concepts={}
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

#fusion()

#parse_directory(max_subdirectories=10,max_files=100,data_directory="crawlerpsc/2014_12_05/",results_directory="crawler_concepts/2014_12_04/")
#parse_files_and_retrieve_concepts(max_files=1000)



