import sys
import urllib.request
import urllib.parse
from urllib.error import HTTPError, URLError

import codecs
reader = codecs.getreader("utf-8")

try: 
    import simplejson as json
except ImportError: 
    import json


from abstracter.conceptnet5_client.utils.debug import print_debug
from abstracter.conceptnet5_client.cache.file_cache import cache


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