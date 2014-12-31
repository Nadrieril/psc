import json
import codecs
import urllib.request
import urllib.parse
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
	print("searching freebase : "+url_values)
	full_url = URL + '?' + url_values
	resp = urllib.request.urlopen(full_url)
	return json.load(reader(resp))['result']



if __name__=="__main__":

	#print (search(query='barack obama',lang='en',filter='(any type:/people/person)'))
	#print (search(query='barack_obama',lang='en',filter='(any type:/people/person)',limit=2,exact=True))
	print (search(filter='(all type:/people/person member_of:france)',limit=10,exact=False))
#	print(search(filter='(all discovered_by:heisenberg)',limit=10))
