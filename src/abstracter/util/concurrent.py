import asyncio  
import aiohttp
import json


PROXY='http://kuzh.polytechnique.fr:8080'
CONNECTOR=aiohttp.ProxyConnector(proxy=PROXY) if PROXY else None

@asyncio.coroutine
def fetch_page(tag,url,dict):  
    response = yield from aiohttp.request(
        'GET', url,
        connector=CONNECTOR,
    )
    if response.status == 200:
        print("data fetched successfully for: %s" % url)
        raw = yield from response.json() 
        dict[tag]=raw#return raw
    else:
        print("data fetch failed for: %d" % url)
        print(response.content, response.status)


def requests(urls):
    """
    param urls : a dict of tag : url
    Be careful : too much urls = too much data
    Result is a list containing json objects (dicts)
    """
    dict={}
    loop = asyncio.get_event_loop()
    f=asyncio.wait([(fetch_page(tag,urls[tag],dict)) for tag in (urls)])
    loop.run_until_complete(f)
    print("Requests finished ! Returning "+len(dict).__str__()+" objects !")
    return dict