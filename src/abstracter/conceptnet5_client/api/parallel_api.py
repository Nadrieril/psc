import urllib.parse
import abstracter.util.concurrent as co
from abstracter.conceptnet5_client.api.result import parse_relevant_edges,parse_similar_concepts
import abstracter.conceptnet5_client.api.settings as settings



"""
Conceptnet5 supports 3 API :
-LookUp
-Search (searching for edges)
-Association (get similarity between concepts)
 Lookup is for when you know the URI of an object in ConceptNet, and want to see a list of edges 
 that include it. Search finds a list of edges that match certain criteria.
  Association is for finding concepts similar to a particular concept or a list of concepts.
"""


###########################################################################
####LOOKUP
############################################################################


def lookup_url(concept,filter='/c/en/',limit=10,**kwargs):
    query_args = {"limit" : limit}
    for key, value in kwargs.items():
        if is_arg_valid(key, settings.SUPPORTED_LOOKUP_ARGS):
            query_args[key] = value
        else:
            raise Exception("LookUp argument '"+key+"' incorrect.")
    concept = concept.replace(' ', '_')
    enc_query_args = urllib.parse.urlencode(query_args)
    return ''.join(['%s/c/%s/%s?' % (settings.BASE_LOOKUP_URL, settings.LANGUAGE, concept)]) + enc_query_args


def search_concepts(concepts,filter='/c/en/',limit=10,**kwargs):
    """
    Returns a dict of search results for each concept.
    """
    #build urls dict
    urls={}
    for concept in concepts:
        urls[concept]=lookup_url(concept,filter,limit,**kwargs)
    return co.requests(urls,parsing_method=parse_relevant_edges)


###########################################################################
####ASSOCIATION
############################################################################

def association_url(concept='dog',filter='/c/en/',limit=10,**kwargs):
    query_args={"filter" : filter, "limit" : limit}
    for key, value in kwargs.items():
        if key in settings.SUPPORTED_ASSOCIATION_ARGS:
            query_args[key] = value
        else:
            raise Exception("Association argument '"+key+"' incorrect.")
    concept = concept.replace(' ', '_')
    enc_query_args = urllib.parse.urlencode(query_args)
    return ''.join(['%s/c/%s/%s?' % (settings.BASE_ASSOCIATION_URL, settings.LANGUAGE,concept)]) + enc_query_args


def get_similar_concepts(concepts,filter='/c/en/',limit=10,**kwargs):
    """
    Returns a dict of results for each concept.
    """
    #build urls dict
    urls={}
    for concept in concepts:
        urls[concept]=association_url(concept,filter,limit,**kwargs)
    return co.requests(urls,parsing_method=parse_similar_concepts)


###########################################################################
####SEARCH
############################################################################

def search_url(filter='/c/en/',limit=10,**kwargs):
    query_args={"filter" : filter, "limit" : limit}
    #query_args = {}
    for key, value in kwargs.items():
        if key in settings.SUPPORTED_SEARCH_ARGS:
            query_args[key] = value
        else:
            raise Exception("Search argument '"+key+"' incorrect.")
    enc_query_args = urllib.parse.urlencode(query_args)   
    return ''.join(['%s%s' % (settings.BASE_SEARCH_URL, '?')]) + enc_query_args


def search_edges_from(concepts,filter='/c/en/',limit=10,**kwargs):
    """
    Returns a dict of results for each concept.
    In kwargs we expect for example a minWeight
    """
    #build urls dict
    urls={}
    for concept in concepts:
        concept = concept.replace(' ', '_')
        urls[concept]=search_url(start='/c/'+settings.LANGUAGE+'/'+concept,filter=filter,limit=limit,**kwargs)
    return co.requests(urls,parsing_method=parse_relevant_edges)
