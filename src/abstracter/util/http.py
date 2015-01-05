import sys
import urllib.request
import urllib.parse
from urllib.error import HTTPError, URLError
import codecs
import json
from abstracter.util.file_cache import cache


#proxy server on the campus
urllib.request.install_opener(
    urllib.request.build_opener(
        urllib.request.ProxyHandler({'http': 'http://kuzh.polytechnique.fr:8080'})
    )
)
reader = codecs.getreader("utf-8")

@cache
def make_http_request(url):
    '''
    Makes and http request to the 'url', if response to that
    'url' is not cached yet.

    Returns the response in json format.
    '''
    #request = urllib2.Request(url)
    try:
        #data = urllib2.urlopen(request)
        data=urllib.request.urlopen(url)
    except HTTPError:
        print('Error code: %s' % e.code, 'HTTPError')
        sys.exit()
    except URLError:
        print('Reason: %s' % e.reason, 'URLError')
        sys.exit()
    return json.load(reader(data))
    #return json.load(data)

def make_simple_request(url):
    """
    Makes a request, without the cache.
    Returns the response in json format.
    """
    try:
        data=urllib.request.urlopen(url)
    except HTTPError:
        print('Error code: %s' % e.code, 'HTTPError')
        sys.exit()
    except URLError:
        print('Reason: %s' % e.reason, 'URLError')
        sys.exit()
    return json.load(reader(data))