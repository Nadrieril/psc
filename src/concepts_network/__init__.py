import networkx as nx
from networkx.readwrite import json_graph
from math import log
import matplotlib.pyplot as plt
import json

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

    def save_to_JSON(self, filename="temp.txt"):
        with open(filename, 'w') as file:
            json.dump(json_graph.node_link_data(self.network), file)

    def load_from_JSON(self,filename="temp.txt"):
        with open(filename,'r') as file:
            self.network=json_graph.node_link_graph(json.load(file))


class Concept:
    def __init__(self, network, id,ic=0,activation=0):
        self.network=network
        self.network.add_node(id)#no error if the node already exists
        self.id=id
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
        return("toto")
        #return("Concept : "+self.id+", activation : "+self.activation)




class Arc:
    def __init__(self, network, fromId, toId, key=0, data=None):
        self.network = network
        self.network.add_edge(fromId,toId,key)#must look if network.has_edge()
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

    def origin(self):
        return Concept(self.network, self.fromId)

    def destination(self):
        return Concept(self.network, self.toId)


if __name__ == '__main__':

    n = Network()


    c1=Concept(network=n.network,id="Toto",ic=5)
    c2=Concept(network=n.network,id="Babar",ic=4)
    c3=Concept(network=n.network,id="Babar",ic=6)
    a=Arc(network=n.network,fromId="Toto",toId="Babar",key=0,data="Beuh")
    #print(c1.activation)
    #print(c1)

    n.save_to_JSON("test.txt")

    print(json_graph.node_link_data(n.network))
    #n.add_node(c1)
    #
    nx.draw(n.network)
    plt.savefig("test.png")
    plt.show()

    n.load_from_JSON("test.txt")
    nx.draw(n.network)
    plt.savefig("test.png")
    plt.show()
