import networkx as nx
from networkx.readwrite import json_graph
from math import log
import matplotlib.pyplot as plt
import json
try:
    from abstracter.util.json_stream import *
except ImportError:
    pass

#import os.path, sys
#sys.path.append(os.path.join(os.path.dirname(os.path.realpath(__file__)), os.pardir))

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
    """
    Class representing a concept network.
    It uses the package networkx.
    The only methods to access in other modules are :
    -add_node
    -add_edge
    -has_node
    -has_edge
    -remove_node
    -remove_edge
    -compute_activation
    -successors
    -predecessors
    -JSON generating & loading

    A concept has an activation (a), importance conceptuelle (ic)
    An edge has a weight (w) (always) and a relation (r), maybe more data
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

    def add_node(self,id,ic=2,activation=0,**kwargs):
        self.network.add_node(id)
        self[id]['ic']=ic
        self[id]['a']=activation
        for akey,avalue in kwargs.items():
            self[id][akey]=avalue

    def add_edge(self,fromId,toId,key=0,**kwargs):
        """
        Add an edge with as many data as you want.
        Of course, it's supposed to contain a weight and a relation,
        but we can deal without (no weight is treated like a weight 0)
        """
        if not self.network.has_node(fromId):
            self.add_node(id=fromId)
        if not self.network.has_node(toId):
            self.add_node(id=toId)
        if self.network.has_edge(fromId,toId,key):
            key=key+1
        self.network.add_edge(fromId,toId,key)
        for akey,avalue in kwargs.items():
            if akey=="relation":
                akey='r'
            elif akey=="weight":
                akey="w"
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

    @returnsArcIterator
    def outArcs(self,id):
        return self.network.out_edges_iter(id, data=True, keys=True)

    @returnsArcIterator
    def inArcs(self,id):
        return self.network.in_edges_iter(id, data=True, keys=True)


    def compute_activation(self,id):
        """
        computes the new node activation, using :
        -divlog : logarithmic divisor (connexity)
        -activation of neighbours
        -self-desactivation
        """
        #divlog = log(3 + len(self.inArcs(id))) / log(3)
        divlog = 1  # deactivated for now
        i = 0
        for arc in self.inArcs(id):
            i = i + (arc.w or 0) * self[arc.fromId]['a']
        act = self[id]['a']
        i = i / (100 * divlog)  # neighbours
        d = act / (100 * (self[id]['ic'] or 1))  # self desactivation
        self[id]['a'] = int(min(act + i - d, 100))  # we do not go beyond 100, and activation is an integer



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

    def draw(self,filename=None):
        nx.draw(self.network)
        pos=nx.spring_layout(self.network)
        nx.draw_networkx_labels(self.network,pos=pos,font_family='sans-serif')
        if filename:
            plt.savefig(filename)
        plt.show()


#deprecated ??
class Concept:
    def __init__(self, network, id,ic=2,activation=0):
        self.network=network
        self.id=id
        if not network.has_node(id):
            #print("creating concept "+id)
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


    def compute_activation(self,id):
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

    def __str__(self):
        return ("%s --> %s, %d, data=" % (self.fromId,self.toId,self.key) + self.data.__str__())


if __name__ == '__main__':
    def test():
        n=Network()
        n.add_node(id="toto",activation=70,ic=5)
        n.add_node(id="babar",activation=0,ic=6)
        n.add_edge(fromId="toto",toId="babar",key=0,autreargdumythe="haha",w=50)
        n.add_edge("toto","babar",r="hihi",w=10.261645654)
        print(n.get_edge("toto","babar",0))
        print(n.get_edge("toto","babar",1))
        for v in n.outArcs("toto"):
            print(v)
        print(n["toto"]['a'])
        n.compute_activation("babar")
        print(n["babar"]["a"])
        n.remove_edge("toto","babar",all=False,key=1)
        nx.draw(n.network)
        plt.show()   

    pass

