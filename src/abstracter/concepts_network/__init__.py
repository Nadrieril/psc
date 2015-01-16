import networkx as nx
from networkx.readwrite import json_graph
from math import log
import matplotlib.pyplot as plt
import json
try:
    from abstracter.util.json_stream import *
except ImportError:
    pass
try:
    from abstracter.concepts_network.network import Network
except ImportError:
    from .network import Network

class ConceptNetwork(Network):
    """
    Data in a conceptnetwork is much more precise than in a general network.
    """

    def __init__(self):
        super(ConceptNetwork,self).__init__()

    def add_node(self,id,a,ic):
        """
        a : activation
        ic : importance conceptuelle
        """
        super(ConceptNetwork,self).add_node(id=id,a=a,ic=ic)

    def add_edge(self,fromId,toId,w,r,key=0):
        """
        w : weight
        r : relation
        """
        if not self.network.has_node(fromId):
            self.add_node(id=fromId,a=0,ic=0)
        if not self.network.has_node(toId):
            self.add_node(id=toId,a=0,ic=0)
        if self.network.has_edge(fromId,toId,key):
            key=key+1
        super(ConceptNetwork,self).add_edge(fromId=fromId,toId=toId,key=key,w=w,r=r)

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
            i = i + (arc[3]['w'] or 0) * self[arc[0]]['a']
        act = self[id]['a']
        i = i / (100 * divlog)  # neighbours
        d = act / (100 * (self[id]['ic'] or 1))  # self desactivation
        self[id]['a'] = int(min(act + i - d, 100))  # we do not go beyond 100, and activation is an integer


    ############################################
    ###JSON streams
    ##########################################

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



if __name__ == '__main__':
    def test():
        n=ConceptNetwork()
        n.add_node(id="toto",a=70,ic=5)
        n.add_node(id="babar",a=0,ic=6)
        n.add_edge(fromId="toto",toId="babar",r="haha",w=50)
        n.add_edge("toto","babar",r="hihi",w=10.261645654)
        print(n["toto"])
        print(n.get_edge("toto","babar",0))
        print(n.get_edge("toto","babar",1))
        for v in n.outArcs("toto"):
            print(v)
            print(v[3]["w"])
        print(n["toto"]['a'])
        n.compute_activation("babar")
        print(n["babar"]["a"])
        n.remove_edge("toto","babar",all=False,key=1)
        nx.draw(n.network)
        plt.show()   

    test()
    pass
