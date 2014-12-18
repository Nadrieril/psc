import sys
import urllib
import urllib2



from abstracter.conceptnet5_client.utils.debug import print_debug
from abstracter.conceptnet5_client.web.api import LookUp, Search, Association
from abstracter.conceptnet5_client.utils.result import Result
from abstracter.conceptnet5_client.utils.pprint import pprint_paths
from abstracter.conceptnet5_client.inference.path import Path

urllib2.install_opener(
    urllib2.build_opener(
        urllib2.ProxyHandler({'http': 'http://kuzh.polytechnique.fr:8080'})
    )
)

def demonstrate_lookup(concept):
    print ("Demonstrating LookUp concept API")
    lookup = LookUp(offset=1, limit=1)
    data = lookup.search_concept(concept)
    r = Result(data)
    edges = r.parse_all_edges()
    for edge in edges:
        edge.print_edge()
        edge.print_all_attrs()
    print
    
    print ("Demonstrating LookUp concept API cleaning self referencing edges")
    lookup = LookUp(offset=1, limit=1)
    data = lookup.search_concept(concept)
    r = Result(data)
    r.print_raw_result()
    print


def demonstrate_source_lookup(source_uri):
    print ("Demonstrating LookUp source API")
    lookup = LookUp()
    data = lookup.search_source(source_uri)
    r = Result(data)
    r.print_raw_result()
    print


def demonstrate_search():
    print ("Demonstrating Search API")
    s = Search(rel='/c/en/be_often_compare_to')
    data = s.search()
    r = Result(data)
    r.print_raw_result()
    print
    
    s = Search(text='mariah carey', surfaceText='dion', something='anything')
    data = s.search()
    r = Result(data)
    r.print_raw_result()
    print


def demonstrate_association():
    print ("Demonstrating Association API")
    a = Association(filter='/c/en/dog', limit=1)
    data = a.get_similar_concepts('cat')
    r = Result(data)
    r.print_raw_result()
    print
    
    a = Association()
    data = a.get_similar_concepts_by_term_list(['toast', 'cereal', 'juice', 'egg'])
    r = Result(data)
    r.print_raw_result()
    print
    r.parse_all_edges()
    print


def demonstrate_concepts_tuples_by_relations():
    concepts = ['/c/en/cat', '/c/en/animal', '/c/en/living']
    #relations = ['/r/IsA', '/r/HasProperty', '/r/AtLocation', '/r/LocatedNear'] 
    #relations = ['/r/HasPrerequisite', '/r/HasSubevent'] 
    #relations = ['/r/HasPrerequisite', '/r/HasFirstSubevent'] 
    relations = ['/r/ReceivesAction', '/r/HasProperty'] 
    p = Path(concepts, relations)
    concepts_tuples = p.get_all_tuples_of_concepts()
    pprint_paths(sys.stdout, concepts_tuples) 


def demonstrate_relations_tuples_by_concepts():
    concepts = ['/c/en/person', '/c/en/human', '/c/en/animal', '/c/en/creature']
    relations = []
    p = Path(concepts, relations)
    relations_tuples = p.get_all_tuples_of_relations()
    for t in relations_tuples:
        print(t)
    #pprint_paths(sys.stdout, relations_tuples) 


def demonstrate_path_existence_check():
    concepts = ['/c/en/thunder', '/c/en/noise', '/c/en/loud']
    #concepts = ['/c/en/thunder', '/c/en/noise', '/c/en/sound', '/c/en/loud']
    relations = ['/r/IsA', '/r/HasProperty'] 
    p = Path(concepts, relations)
    p.print_path()  
    print('Asking path existence...')
    exist = p.does_exist(print_where_breaks=True)
    if exist:
        print('Path exist')

#useful edges with associated weight
#these weights are arbitrary
USEFUL_CONCEPTNET_EDGES = { '/r/IsA' : 1,
'/r/RelatedTo' : 0.5,
'/r/CapableOf' : 0.3,
'/r/AtLocation' : 0.3,
'/r/Antonym' : 0.2,
'/r/Desires' : 0.2,
'/r/HasProperty' : 0.6,
'/r/HasA' : 0.5,
'/r/UsedFor' : 0.4
}

NOT_USEFUL_CONCEPTNET_EDGES = ['/r/NotCapableOf','/r/ReceivesAction']


def get_edges(concept='dog'):
    #relations=['/r/IsA']
    attributes=[]
    lookup = LookUp(offset=5, limit=50)
    data = lookup.search_concept(concept)
    r = Result(data)
    edges = r.parse_all_edges()
    for edge in edges:
        #if(edge.rel in         #
        #edge.print_edge()
        #+edge.weight
        #print(edge.rel)
        print('(%s -> %s -> %s , %d)' % (edge.start, edge.rel, edge.end,edge.weight))
        #edge.print_all_attrs()
    print

    
def main():
    get_edges()
    #demonstrate_lookup('see movie')
    #demonstrate_search()
    #demonstrate_association()
    #demonstrate_source_lookup('/s/contributor/omcs/rspeer')
    #demonstrate_source_lookup('/s/rule/sum_edges')
    #demonstrate_source_lookup('/s/wordnet/3.0')

    #demonstrate_concepts_tuples_by_relations()
    #demonstrate_relations_tuples_by_concepts()
    #demonstrate_path_existence_check()

if __name__ == '__main__':
    main()
