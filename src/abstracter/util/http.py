import sys
import urllib.request
import urllib.parse
from urllib.error import HTTPError, URLError
import codecs
import json
import hashlib
import os

##########################################
###SETTINGS
########################################

#proxy server on the campus
urllib.request.install_opener(
    urllib.request.build_opener(
        urllib.request.ProxyHandler({'http' : 'http://kuzh.polytechnique.fr:8080'})
    )
)

reader = codecs.getreader("utf-8")

CACHE_DIR='cached_data/'
DISABLE_CACHE=True


########################################################


def make_http_request_with_cache(url):
    cache_key = hashlib.sha1(url.encode('utf-8')).hexdigest()
    if not os.path.exists(CACHE_DIR):
        os.makedirs(CACHE_DIR)
    print('Looking for cache: %s' % url)

    # Check the value is cached, if cached return cached content
    for path, dirs, files in os.walk(CACHE_DIR):
        for filename in files:
            if filename == cache_key:
                print('Cache found: %s' % url)
                fullpath = os.path.join(CACHE_DIR, filename)
                data = open(fullpath, 'r').read()
                return json.load(reader(data))
    print('Cache not found, making request: %s' % url)
    try:
        #data = urllib2.urlopen(request)
        data=urllib.request.urlopen(url)
    except HTTPError:
        print('Error code: %s' % e.code, 'HTTPError')
        sys.exit()
    except URLError:
        print('Reason: %s' % e.reason, 'URLError')
        sys.exit()
    json_data = json.load(reader(data))
    if cache:
        with open(os.path.join(CACHE_DIR, cache_key), 'w') as f:
            json.dump(json_data, f) 
    return json_data


#@cache
#def make_http_request(url):
#    '''
#    Makes and http request to the 'url', if response to that
#    'url' is not cached yet.
#
#    Returns the response in json format.
#    '''
#    #request = urllib2.Request(url)
#    try:
#        #data = urllib2.urlopen(request)
#        data=urllib.request.urlopen(url)
#    except HTTPError:
#        print('Error code: %s' % e.code, 'HTTPError')
#        sys.exit()
#    except URLError:
#        print('Reason: %s' % e.reason, 'URLError')
#        sys.exit()
#    return json.load(reader(data))
#    #return json.load(data)

def make_http_request_without_cache(url):
    """
    Makes a request, without the cache.
    Returns the response in json format.
    """
    try:
        data=urllib.request.urlopen(url)
    except HTTPError as e:
        print('HTTPError')
        sys.exit()
    except URLError as e:
        print('URLError : ')
        sys.exit()
    return json.load(reader(data))


if DISABLE_CACHE:
    make_http_request=make_http_request_without_cache
else:
    make_http_request=make_http_request_with_cache
