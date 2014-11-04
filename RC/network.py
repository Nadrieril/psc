#!usr/bin/python3.4
# -*-coding:utf-8 -*

from collections import deque

import pygraphviz as pgv
from node import *

class Network:
    """le RC"""
    
    def __init__(self, graph):
        self.network=[]
        if(graph):#si on a passé un graphe en argument
            for i in graph.nodes():
                liste=i.__str__().split("_")
                self.addNode(Node(liste[0], int(liste[1]), (int(i.attr['fontsize'])-10)*100/40))

            for i in graph.edges():
                l1=i[0].__str__().split("_")
                name1=l1[0]
                l2=i[1].__str__().split("_")
                name2=l2[0]
                if(i.attr['label'] ):
                    self.seek(name1).addLink(Link(int(i.attr['weight']), self.seek(i.attr['label'])),  self.seek(name2))
                else:
                    self.seek(name1).addLink(Link(int(i.attr['weight'])),  self.seek(name2))
        
    def addNode(self, n):
        self.network.append(n)

    def __str__(self):
        s=""
        for n in self.network:
            s=s+n.__str__()+"\n"
        return(s)

    def seek(self, string):
        res=None
        for n in self.network:
            if(n.name==string):
                res=n
        return(res)
        
    def to_graph(self):
        res=pgv.AGraph(directed=True, overlap=False)
        for n1 in self.network:
            res.add_node(n1.__str__(), shape='box', fontsize=(n1.a)*40/100+10)
        for n1 in self.network:
            for d,l  in n1.linksOut.iteritems():
                if(l.label):
                    res.add_edge(n1.__str__(), d.__str__(), label=l.label, weight=l.p)
                else:
                    res.add_edge(n1.__str__(), d.__str__(), weight=l.p)
        return(res)
