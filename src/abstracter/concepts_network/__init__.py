import networkx as nx
from networkx.readwrite import json_graph
from math import log
import matplotlib.pyplot as plt
import json

#import src.util.json_stream
import os.path, sys
#sys.path.append(os.path.join(os.path.dirname(os.path.realpath(__file__)), os.pardir))
from ..util.json_stream import *
#TODO : change the line sys.path.append... and make sure imports from subdirectories will still work
#TODO : SEE FOR ARC AND CONCEPT the adjustments to made in the constructors

def returnsConceptIterator(f):
    def wrap(self, *args, **kwargs):
        ret = f(self, *args, **kwargs)
        for c in ret:
            yield Concept(self.network, c)
    return wrap

def returnsArcIterator(f):
    def wrap(self, *args, **kwargs):
        ret = f(self, *args, **kwargs)
        for (i, j, key, data) in ret:
            yield Arc(self.network, i, j, key, data)
    return wrap


class Network:
    def __init__(self, filename=None):
        self.network = nx.MultiDiGraph()
        if filename:
            with open(filename, 'w') as file:
                dico = json.load(file)
                self.network = nx.MultiDiGraph(dico)

    def get(self, id):
        return Concept(self.network, id)

    def add_node(self,node):
        self.network.add_node(node.id)

    def add_edge(self,id1,id2):
        self.network.add_edge(id1,id2)

    ###########################################################
    ###JSON generating and decoding
    ##############################################

    def save_to_JSON(self, filename="temp.json"):
        with open(filename, 'w') as file:
            json.dump(json_graph.node_link_data(self.network), file)

    def load_from_JSON(self,filename="temp.json"):
        with open(filename,'r') as file:
            self.network=json_graph.node_link_graph(json.load(file))

    def load_nodes_from_stream(self,filename="temp_nodes.jsons"):
        self.network.add_nodes_from(read_json_stream(filename))

    def load_edges_from_stream(self,filename="temp_edges.jsons"):
        self.network.add_edges_from(read_json_stream(filename))

    def load_from_JSON_stream(self,nodes_files,edges_files):
        """
        We load from a bunch of files, assuming that
        they contain node and edge data
        """
        for f in nodes_files:
            self.load_nodes_from_stream(f)
        for f in edges_files:
            self.load_edges_from_stream(f)


    def save_to_JSON_stream(self,filenamebase="temp"):
        nodes_writer=JSONStreamWriter(filenamebase+"_nodes.jsons")
        for n in self.network.nodes(data=True):
            nodes_writer.write(n)
        nodes_writer.close()
        edges_writer=JSONStreamWriter(filenamebase+"_edges.jsons")
        for e in self.network.edges(data=True):
            edges_writer.write(e)
        edges_writer.close()



class Concept:
    def __init__(self, network, id,ic=0,activation=0):
        self.network=network
        self.id=id
        if not network.has_node(id):
            self.network.add_node(id)#no error if the node already exists
            self.activation=activation
            self.ic=ic
        #self.__setattr__("network",network)#self.network = network
        #self.__setattr__("id",0)
        #self.__setattr__("activation",0)
        #self.ic = ic

    def __getattr__(self, attr):
        if attr in ["network","id"]:
            return self.__dict__[attr]
        else:
            return self.network.node[self.id][attr]

    def __setattr__(self, attr, value):
        if attr in ["network","id"]:
            self.__dict__[attr]=value
        else:
            self.network.node[self.id][attr] = value

    @returnsConceptIterator
    def successors(self):
        return self.network.successors_iter(self.id)

    @returnsConceptIterator
    def predecessors(self):
        return self.network.predecessors_iter(self.id)

    @returnsArcIterator
    def outArcs(self):
        return self.network.out_edges_iter(self.id, data=True, keys=True)

    @returnsArcIterator
    def inArcs(self):
        return self.network.in_edges_iter(self.id, data=True, keys=True)


    def compute_activation(self):
        """
        computes the new node activation, using :
        -divlog : logarithmic divisor (connexity)
        -activation of neighbours
        -self-desactivation
        """
        divlog = log(3 + len(self.inArcs())) / log(3)
        divlog = 1  # deactivated for now
        i = 0
        for arc in self.inArcs():
            i = i + (arc.weight or 0) * arc.origin.activation
            # does not take
        act = self.activation
        i = i / (100 * divlog)  # neighbours
        d = act / (100 * (self.ic or 1))  # self desactivation
        self.activation = min(act + i - d, 100)  # we do not go beyond 100


    def __str__(self):
        return("Concept : "+self.id+", activation : "+self.activation)




class Arc:
    def __init__(self, network, fromId, toId, key=0, data=None):
        self.network = network
        self.fromId = fromId
        self.toId = toId
        self.key = key
        if (not network.has_edge(fromId,toId)):
        # or (network[fromId][toId]['data'] != data):
            self.network.add_edge(fromId,toId,key)#must look if network.has_edge()
            self.data=data


    def __getattr__(self, attr):
        if attr in ["network","fromId","toId","key"]:
            return self.__dict__[attr]
        else:
            return self.network[self.fromId][self.toId][self.key][attr]

    def __setattr__(self, attr, value):
        if attr in ["network","fromId","toId","key"]:
            self.__dict__[attr]=value
        else:
            self.network[self.fromId][self.toId][self.key][attr] = value

    def origin(self):
        return Concept(self.network, self.fromId)

    def destination(self):
        return Concept(self.network, self.toId)


if __name__ == '__main__':
    pass
