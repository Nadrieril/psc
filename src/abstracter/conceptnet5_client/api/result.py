import ast

from abstracter.conceptnet5_client.api.data_settings import RELEVANT_EDGES_ATTRIBUTES,USEFUL_CONCEPTNET_EDGES,MINIMUM_WEIGHT_ALLOWED,MAX_UNDERSCORES_ALLOWED
import json

"""
Methods for parsing a query result
"""


# These are the primary keys returned by a query (in raw json data)
SUPPORTED_KEYS = ['numFound', 'maxScore', 'edges', 'terms', 'similar']
#numFound : number of edges found

def rel_to_word(relation='/r/HasA'):
    return relation.split('/')[2]

def concept_to_word(concept='/c/en/dog'):
    return concept.split('/')[3]

def is_relevant_concept(word):
    return len(word.split('_'))<MAX_UNDERSCORES_ALLOWED+2

def parse_similar_concepts(json_data):
    """
    Transforms [['/c/en/dog',0.995654654]] into ['dog',0.995]
    """
    return list([concept_to_word(w[0]),int(w[1]*1000)/1000] for w in json_data["similar"])



def parse_relevant_edges(json_data,clean_self_ref=True):
    edges = []
        
    if not 'edges' in json_data:
        return edges
    for edge_str in json_data['edges']:
        e = Edge(edge_str)
        if e.rel in USEFUL_CONCEPTNET_EDGES:# and e.weight*USEFUL_CONCEPTNET_EDGES[e.rel] > MINIMUM_WEIGHT_ALLOWED: unuseful
            e.rel=rel_to_word(e.rel)
            e.start=concept_to_word(e.start)
            e.end=concept_to_word(e.end)
            if is_relevant_concept(e.start) and is_relevant_concept(e.end):
                if clean_self_ref:
                    if e.start != e.end:
                        edges.append(e)
                else:
                    edges.append(e)
    return edges


        
class Edge(object):
    '''
    This class implements the methods for representing a single edge and manipulating it.
    '''
    def __init__(self, edge_str):
        edge_dict = ast.literal_eval(str(edge_str))
        for attribute in RELEVANT_EDGES_ATTRIBUTES:
            self.__dict__[attribute]=(edge_dict[attribute])

    
    def print_assertion(self):
        '''
        Prints the lemmas of this edge with start, rel, end lemmas.
        '''
        print('%s %s %s' % (self.start_lemmas, self.rel, self.end_lemmas))

    
    def print_edge(self):
        '''
        Prints the normalized edge data with start node, rel, end node.
        '''
        print('(%s -> %s -> %s , %d)' % (self.start, self.rel, self.end,self.weight))

    
    def print_all_attrs(self):
        '''
        Prints all attributes regarding to this edge.
        '''
        attrs = vars(self)
        print('\n'.join('%s: %s' % item for item in attrs.items()))