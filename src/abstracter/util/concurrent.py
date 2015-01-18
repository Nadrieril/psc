import asyncio  
import aiohttp
import json


PROXY='http://kuzh.polytechnique.fr:8080'
CONNECTOR=aiohttp.ProxyConnector(proxy=PROXY) if PROXY else None

@asyncio.coroutine
def fetch_page(tag,url,dict,parsing_method=None):  
    response = yield from aiohttp.request(
        'GET', url,
        connector=CONNECTOR,
    )
    if response.status == 200:
        #print("data fetched successfully for: %s" % url)
        raw = yield from response.json()
        dict[tag]=parsing_method(raw) if parsing_method else raw#return raw
    else:
        print("data fetch failed for: %s" % url)
        print(response.content, response.status)


def requests(urls,parsing_method=None):
    """
    param urls : a dict of tag : url
    Be careful : too much urls = too much data
    Result is a list containing json objects (dicts)
    """
    print("Launching "+len(urls).__str__()+" requests !")
    dict={}
    loop = asyncio.get_event_loop()
    f=asyncio.wait([(fetch_page(tag,urls[tag],dict,parsing_method)) for tag in (urls)])
    loop.run_until_complete(f)
    print("Requests finished ! Returning "+len(dict).__str__()+" objects !")
    return dict