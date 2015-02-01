import urllib.parse
from abstracter.util.http import *
from abstracter.freebase_client.settings import *
from abstracter.util.http import make_https_request
import abstracter.util.concurrent as co


def keep_relevant(query_response):
	for result in response['result']:
		if result['score']>MINIMUM_RESULT_SCORE:
			yield result


def search(lang='en',limit=10,**kwargs):
	data={'key' : USER_KEY, 'lang' : lang, 'limit' : limit}
	for key,val in kwargs.items():
		if key in SEARCH_PARAMETERS:
			data[key]=val
		else:
			pass
	url_values = urllib.parse.urlencode(data)
	full_url = URL + '?' + url_values
	resp=make_https_request(full_url).json()
	return resp['result']


def search_name(name):
	data=search(query=name,lang='en',limit=2)
	res={}
	if data:
		dat=data[0]
		score=dat['score']
		name=dat['name']
		res['from']=name.lower().replace(' ','_')
		res['score']=score
		if 'notable' in dat:
			res['to']=dat['notable']['name'].lower().replace(' ','_')#IsA relation
	return res

#################################
###concurrent requests
################################

def search_name_url(name,**kwargs):
	data={'query' : name,'key' : USER_KEY, 'lang' : 'en', 'limit' : 2}
	for key,val in kwargs.items():
		if key in SEARCH_PARAMETERS:
			data[key]=val
		else:
			pass
	url_values = urllib.parse.urlencode(data)
	return URL + '?' + url_values


def search_names(names,**kwargs):
	urls={}
	for name in names:
		urls[name]=search_name_url(name.replace(' ', '_'),**kwargs)
	return co.requests(urls,parsing_method=parse_results)

def parse_results(query_result):
	"""
	Parsing a json object
	"""
	res={}
	data=query_result['result']
	if data:
		dat=data[0]
		score=dat['score']
		name=dat['name']
		res['from']=name.lower().replace(' ','_')
		res['score']=score
		if 'notable' in dat:
			res['to']=dat['notable']['name'].lower().replace(' ','_')#IsA relation
	return res



if __name__=="__main__":

	#for i in (search(query='ezequiel lavezzi',lang='en',filter='(any type:/people/person)',limit=2)):
	#	print(i)
	#print((search(query='ezequiel lavezzi',lang='en',filter='(any type:/people/person)',limit=2))[0])
	#print (search(query='barack_obama',lang='en',filter='(any type:/people/person)',limit=2,exact=True))
	#print (search(filter='(all type:/people/person member_of:france)',limit=10,exact=False))
#	print(search(filter='(all discovered_by:heisenberg)',limit=10))
	print(search_name("albert rusnak"))
