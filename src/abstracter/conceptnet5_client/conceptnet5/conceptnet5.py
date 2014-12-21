from abstracter.conceptnet5_client.utils.debug import print_debug
from abstracter.conceptnet5_client.web.api import LookUp, Search, Association
from abstracter.conceptnet5_client.utils.result import Result
from abstracter.conceptnet5_client.inference.path import Path

from abstracter.concepts_network import *

"""
Summary of methods used by other modules
for example methods to expand a conceptnetwork
"""

def get_edges(concept='dog'):
    lookup = LookUp(limit=50)
    data = lookup.search_concept(concept)
    r = Result(data)
    edges = r.parse_relevant_edges()
    return edges



