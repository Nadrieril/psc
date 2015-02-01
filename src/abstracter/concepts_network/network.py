import networkx as nx
from networkx.readwrite import json_graph
from math import log
import matplotlib.pyplot as plt
import json



class Network:
    """
    Class representing a network.
    It uses the package networkx.
    """
    def __init__(self):
        self.network = nx.MultiDiGraph()

    ###########################################################
    ###Nodes and edges
    ##############################################

    def __getitem__(self, id):
        try:
            return self.network.node[id]
        except KeyError:
            return None

    def get_node(self,id):
        return self.network.node[id]

    def add_node(self,id,**kwargs):
        self.network.add_node(id)
        for akey,avalue in kwargs.items():
            self[id][akey]=avalue

    def add_edge(self,fromId,toId,key=0,**kwargs):
        """
        Add an edge with as many data as you want.
        Of course, it's supposed to contain a weight and a relation,
        but we can deal without (no weight is treated like a weight 0)
        """
        self.network.add_edge(fromId,toId,key)
        for akey,avalue in kwargs.items():
            self.network[fromId][toId][key][akey]=avalue
  
    def remove_node(self,id):
        self.network.remove_node(id)

    def remove_edge(self,fromId,toId,key=None,all=True):
        if all:
            while self.has_edge(fromId,toId):
                self.network.remove_edge(fromId,toId)
        else:
            if self.has_edge(fromId,toId,key):
                self.network.remove_edge(fromId,toId,key)

    def has_node(self,id):
        return self.network.has_node(id)

    def has_edge(self,fromId,toId,key=None):
        return self.network.has_edge(fromId,toId,key)

    def predecessors(self,id):
        return self.network.predecessors_iter(id)

    def successors(self,id):
        return self.network.successors_iter(id)

    def get_edge(self,fromId,toId,key=0):
        return self.network[fromId][toId][key]

    def outArcs(self,id):
        return self.network.out_edges_iter(id, data=True, keys=True)

    def inArcs(self,id):
        return self.network.in_edges_iter(id, data=True, keys=True)

    def nodes(self,data=True):
        return self.network.nodes(data)

    def edges(self):
        return self.network.edges()

    ###########################################################
    ###JSON generating and decoding
    ##############################################

    def save_to_JSON(self, filename="temp.json"):
        with open(filename, 'w') as file:
            json.dump(json_graph.node_link_data(self.network), file)

    def load_from_JSON(self,filename="temp.json"):
        with open(filename,'r') as file:
            self.network=json_graph.node_link_graph(json.load(file))


    def draw(self,filename=None):
        nx.draw(self.network)
        pos=nx.spring_layout(self.network)
        nx.draw_networkx_labels(self.network,pos=pos,font_family='sans-serif')
        if filename:
            plt.savefig(filename)
        plt.show()


