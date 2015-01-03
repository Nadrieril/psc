import json
import codecs
import urllib.request
import urllib.parse
try:
	from abstracter.freebase_client.settings import *
except ImportError:
	from settings import *

reader = codecs.getreader("utf-8")

#TODO : PARSE QUERY RESULTS
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
	#print("searching freebase : "+url_values)
	full_url = URL + '?' + url_values
	resp = urllib.request.urlopen(full_url)
	return json.load(reader(resp))['result']

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


if __name__=="__main__":

	#for i in (search(query='ezequiel lavezzi',lang='en',filter='(any type:/people/person)',limit=2)):
	#	print(i)
	#print((search(query='ezequiel lavezzi',lang='en',filter='(any type:/people/person)',limit=2))[0])
	#print (search(query='barack_obama',lang='en',filter='(any type:/people/person)',limit=2,exact=True))
	#print (search(filter='(all type:/people/person member_of:france)',limit=10,exact=False))
#	print(search(filter='(all discovered_by:heisenberg)',limit=10))
	print(search_name("albert rusnak"))
