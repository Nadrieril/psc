import json
import codecs
import urllib.request
import urllib.parse
from settings import *

reader = codecs.getreader("utf-8")

#https://developers.google.com/freebase/v1/search-cookbook

def keep_relevant(query_response):
	for result in response['result']:
		if result['score']>MINIMUM_RESULT_SCORE:
			yield result



if __name__=="__main__":

	data = {
	'query' : 'barack obama',
	'lang' : 'en',
	'filter':'(any type:/people/person)',
	'key': "AIzaSyBPhRSY6Q1iPx82tnkoWAzbAc4JqhNjiJs"
	}
	url_values = urllib.parse.urlencode(data)
	print(url_values)
	full_url = URL + '?' + url_values
	resp = urllib.request.urlopen(full_url)
	response = json.load(reader(resp))
	print(len(response['result']))
	#for result in response['result']:
	#    print(result['name'] + ' (' + str(result['score']) + ')')

	for res in keep_relevant(response):
		print(res['name'] + ' (' + str(res['score']) + ')')