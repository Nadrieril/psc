import requests
"""
Making http and https requests, using requests.
example :

>>> url = http://conceptnet5.media.mit.edu/data/5.3/assoc/c/en/barack_obama?limit=3&filter=%2Fc%2Fen%2F
>>> print(make_http_request(url).json())
"""

##########################################
###PROXY SETTINGS
########################################


HTTPS_PROXY={'https' : 'http://kuzh.polytechnique.fr:8080'}
HTTP_PROXY={'http' : 'http://kuzh.polytechnique.fr:8080'}
#HTTP_PROXY=None
#HTTPS_PROXY=None

########################################################

def make_https_request(url):
    return requests.get(url,proxies=HTTPS_PROXY)#.json()

def make_http_request(url):
    return requests.get(url,proxies=HTTP_PROXY)#.json()

