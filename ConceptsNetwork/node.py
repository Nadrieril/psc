#!usr/bin/python3.4
# -*-coding:utf-8 -*

from numpy import log
import matplotlib.pyplot as plt


class Node:
    """Nodes in our concept network
    -activation lies between 0 and 100
    -weight between 0 and 100
    
    important methods (used in other file) :
    -compute_activation
    
    """

    def __init__(self, name, ic, activation=None):
        self.linksIn = {}
        self.linksOut = {}
        self.name = name
        self.ic = ic
        self.has_observer=False
        if activation:
            self.activation = activation
        else:
            self.activation = 0


    def add_link_from(self, node, proximity, label=None):
        """adds a link from node to self
        """
        if(node in self.linksIn):
            del self.linksIn[node]
        
        if(not(label)):
            self.linksIn.update({node: [proximity]})
        else:
            self.linksIn.update({node: [proximity, label]})

        if(self in node.linksOut):
            del node.linksOut[self]
        
        if(not(label)):
            node.linksOut.update({self: [proximity]})
        else:
            node.linksOut.update({self: [proximity, label]})

    def add_link_to(self, node, proximity, label=None):
        """adds a link from self to node
        """
        if(self in node.linksIn):
            del node.linksIn[self]
        
        if(not(label)):
            node.linksIn.update({self: [proximity]})
        else:
            node.linksIn.update({self: [proximity, label]})

        if(node in self.linksOut):
            del self.linksOut[node]
        
        if(not(label)):
            self.linksOut.update({node: [proximity]})
        else:
            self.linksOut.update({node: [proximity, label]})


    def __str__(self):
        """overrides __str__
        """
        return("{0}".format(self.name))

    def add_observer(self, obs):
        """adds an observer (class NodeObserver)
        to monitor node activation during the process
        """
        self.has_observer=True
        self.observer = obs


    def compute_activation(self):
        """computes the new node activation, using :
        -divlog : logarithmic divisor (connexity)
        -activation of neighbours
        -self-desactivation
        """
        divlog = log(3+len(self.linksIn))/log(3)
        divlog = 1  #deactivated for now
        i = 0
        for n, l in self.linksIn.items():
            i = i+l[0]*n.activation
            #does not take 
        i = i/(100*divlog)  #neighbours
        d = self.activation/(100*self.ic)  #self desactivation
        self.activation = self.activation+i-d
        self.activation = min(self.activation, 100)  #we do not go beyond 100


class NodeObserver:
    """created to monitor node activation"""
    def __init__(self):
        self.times = []#moments where node activation is modified
        self.activations = []#node activations

    def update(self, time, activation):
        self.times.append(time)
        self.activations.append(activation)

    def draw(self):
        # draws a graph of node activation during time
        print(self.times)
        print(self.activations)
        plt.figure()
        plt.plot(self.times, self.activations)
        plt.show()


# test
if __name__ == "__main__":
    elephant = Node("elephant", 5, 0)

    print(elephant)

    nd = NodeObserver()
    nd.update(1, 2)
    nd.update(2, 4)
    nd.update(3, 6)
    # nd.draw()
