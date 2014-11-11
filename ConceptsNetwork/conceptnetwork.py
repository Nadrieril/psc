#!usr/bin/python3.4
# -*-coding:utf-8 -*

import pygraphviz as pgv
import json
from node import Node

__all__=['ConceptNetwork']

class ConceptNetwork:
    """our Concept Network. You do not need to add nodes manually.
    important methods (used in other files) :
    -self.seek(node_name)
    -self.to_graph
    
    -net1 = Network.load("file.txt");
    -net1.save("file.txt")
    
    """
    
    def __init__(self, simple=None, graph=None):
        """create new RC
        two ways to do it :
        -by adding a simple network, easy way of representation
        -by adding another graph (not recommanded, use the simple network instead)
        """
        
        self.network = []
        self.graph = pgv.AGraph(directed=True, overlap=False)
        
        if(simple):
            for node in simple.nodes:
                self.add_node(Node(node[0], node[1], node[2]))
            
            for (node,t) in simple.links:
                if(len(t)==3):
                    self.seek(node).add_link_to(self.seek(t[0]), int(t[1]), self.seek(t[2]))
                else:
                    self.seek(node).add_link_to(self.seek(t[0]), int(t[1]))

        if(graph):  #deprecated : if a graph was passed in argument
            print("warning, deprecated use")
            #for i in graph.nodes():
            #   liste = i.__str__().split("_")
            #    self.add_node(Node(liste[0], int(liste[1]),
            #    (int(i.attr['fontsize'])-10)*100/40))
            #for i in graph.edges():
            #    l1 = i[0].__str__().split("_")
            #    name1 = l1[0]
            #    l2 = i[1].__str__().split("_")
            #    name2 = l2[0]
            #    self.add_link(self.seek(name1), self.seek(name2),int(i.attr['weight']), self.seek(i.attr['label'])
            #                if 'label' in i.attr else None)    
        else:
            for node in self.network:
                self.graph.add_node(node.__str__(), shape='box')
                for n, t in node.linksOut.items():
                    if len(t)==1:
                        self.graph.add_edge(node.__str__(), n.__str__(),weight=t[0])
                    else:
                        self.graph.add_edge(node.__str__(), n.__str__(),
                        label=t[1].__str__(), weight=t[0])
        #we don't want the layout to change much, thus fontsize is defined as 50
        for n1 in self.network:
            self.graph.get_node(n1.__str__()).attr['fontsize'] = 40
        self.graph.layout()

    def add_node(self, n):
        """
        adding manually a new node
        """
        if not(n in self.network):
            self.network.append(n)
            self.graph.add_node(n.__str__(), shape='box')

    def add_link(self, n1, n2, proximity, label=None):
        """
        adding manually a new link
        """
        n1.add_link_to(n2, proximity, label)
        if(label):
            self.graph.add_edge(n1.__str__(), n2.__str__(),
                                label=label, weight=proximity)
        else:
            self.graph.add_edge(n1.__str__(), n2.__str__(), weight=proximity)



    def seek(self, node_name):
        """
        seek for a node named "node_name"
        """
        res = None
        for node in self.network:
            if(node.name == node_name):
                res = node
        return(res)


    def to_graph(self):
        """
        in order to gain memory, the graph is already part of the object
        this method aims to modify, make it readable and return it
        """
        for n1 in self.network:
            self.graph.get_node(n1.__str__()).attr['fontsize'] = (
                (n1.activation)*25/100+15)
            # if len(n1.linksOut)+len(n1.linksIn) = =0:
            #     self.graph.get_node(n1.__str__()).attr['style'] = "invis"
            # else:
            #     self.graph.get_node(n1.__str__()).attr['style'] = ""
        for n1 in self.network:
            for d, l in n1.linksOut.items():
                if(len(l)==2):
                    self.graph.get_edge(
                        n1.__str__(), d.__str__()).attr['weight'] = l[0]
                else:
                    self.graph.get_edge(
                        n1.__str__(), d.__str__()).attr['weight'] = l[0]
        return self.graph
        
        
     

    def save(self, filename):
        """writes a file containing the JSON code of the concept network
        """
        SimpleNetwork(self).save(filename)

    @staticmethod
    def load(filename):
        """
        loads a file in JSON and creates a concept network
        """
        return(ConceptNetwork(SimpleNetwork.load(filename)))


class SimpleNetwork:
    """
    A much simpler representation of the concept network,
    designed to be used with json for pretty printing/reading in files
    
    You don't have to use the class SimpleNetwork in other files. 
    Use only the Network methods.
    """
    def __init__(self, net=None):
        """
        creates new simplenetwork, hopefully from a concept network
        """
        self.nodes=[]
        self.links=[]
        if(net):
            for n in net.network:
                self.nodes.append((n.name, n.ic, n.activation))
                for n2, l in n.linksOut.items():
                    if(len(l)==2):
                        self.links.append( (n.name, [n2.name, l[0],l[1].name]) )
                    else:
                        self.links.append( (n.name, [n2.name, l[0]]) ) 

    def to_JSON(self):
        """
        encodes the simpleNetwork into JSON
        """
        return(jsonpickle.encode(self, max_depth=3, keys=True))

    
    def save(self, filename):
        """writes a file containing the JSON code of the network
        """
        file=open(filename, 'w')
        json.dump((self.nodes, self.links), file, indent=2, separators=(',', ':'))
        file.close()

    @staticmethod
    def load(filename):
        """
        loads a file in JSON and creates a simpleNetwork
        """
        snet=SimpleNetwork()
        with open(filename, 'r') as file:
            (snet.nodes, snet.links)=json.load(file)
            file.close()
        return(snet)


if __name__ == "__main__":

    A = pgv.AGraph("RC.dot")
    net1 = Network(simple=None, graph=A)
    A.layout()
    A.draw("initial.png")
    simple=SimpleNetwork(net1)
    simple.save("test2.txt")

    
    net1=Network(SimpleNetwork.load("test2.txt"))
    net1=Network.load("test2.txt")
    simple2=SimpleNetwork(net1)
    simple2.save("test3.txt")
