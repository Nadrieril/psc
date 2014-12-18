import sys
import urllib
import urllib2


from abstracter.conceptnet5_client.utils.debug import print_debug
from abstracter.conceptnet5_client.web.api import LookUp, Search, Association
from abstracter.conceptnet5_client.utils.result import Result
from abstracter.conceptnet5_client.utils.pprint import pprint_paths
from abstracter.conceptnet5_client.inference.path import Path

from abstracter.concepts_network import *
#TODO :#move this to a config file
urllib2.install_opener(
    urllib2.build_opener(
        urllib2.ProxyHandler({'http': 'http://kuzh.polytechnique.fr:8080'})
    )
)

"""
Summary of methods used by other modules
for example methods to expand a conceptnetwork
"""


#useful edges with associated weight
#these weights are arbitrary
USEFUL_CONCEPTNET_EDGES = { '/r/IsA' : 1,
'/r/RelatedTo' : 0.8,
'/r/CapableOf' : 0.3,
'/r/AtLocation' : 0.7,
'/r/Antonym' : 0.2,
'/r/Desires' : 0.2,
'/r/HasProperty' : 0.8,
'/r/HasA' : 0.7,
'/r/UsedFor' : 0.4
}

NOT_USEFUL_CONCEPTNET_EDGES = ['/r/NotCapableOf','/r/ReceivesAction']

MINIMUM_WEIGHT_ALLOWED = 0.5#which is weight of the edge in conceptnet5 * arbitrary 
#weight to keep most important information
#for example, (/c/en/dog -> /r/CapableOf -> /c/en/sense_fear , 3) is not relevant
#(/c/en/dog -> /r/HasA -> /c/en/fur , 4) is relevant
#(/c/en/dog -> /r/RelatedTo -> /c/en/pet , 4) is very relevant


def get_edges(concept='dog'):
    lookup = LookUp(limit=50)
    data = lookup.search_concept(concept)
    r = Result(data)
    edges = r.parse_all_edges()
    return edges


def expand_concept(concept,network,one_word=False):
    edges=get_edges(concept)
    for e in edges:
        if e.rel in USEFUL_CONCEPTNET_EDGES and e.weight*USEFUL_CONCEPTNET_EDGES[e.rel] > MINIMUM_WEIGHT_ALLOWED:
            if (one_word and '_' not in e.end and '_' not in e.start) or not one_word:
                a=Arc(network,fromId=concept_to_word(e.start),toId=concept_to_word(e.end),weight=e.weight,data=rel_to_word(e.rel))
    return

def rel_to_word(relation='/r/HasA'):
	return relation.split('/')[2]

def concept_to_word(concept='/c/en/dog'):
	return concept.split('/')[3]