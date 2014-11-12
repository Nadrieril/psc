#!usr/bin/python3.4
# -*-coding:utf-8 -*

import pygraphviz as pgv


class Network:
    """le RC"""

    def __init__(self):
        self.network = []

    def addNode(self, n):
        self.network.append(n)

    def __str__(self):
        s = ""
        for n in self.network:
            s = s+n.__str__()+"\n"
        return(s)

    def seek(self, string):
        res = None
        for n in self.network:
            if(n.name == string):
                res = n
        return(res)

    def to_graph(self):
        res = pgv.AGraph(directed=True)
        for n1 in self.network:
            res.add_node(n1.__str__(), shape='box', fontsize=(n1.a)*40/100+10)
        for n1 in self.network:
            for d, l in n1.linksOut.items():
                if(l.label):
                    res.add_edge(n1.__str__(), d.__str__(),
                                 label=l.label, weight=l.p)
                else:
                    res.add_edge(n1.__str__(), d.__str__(), weight=l.p)
        return(res)
