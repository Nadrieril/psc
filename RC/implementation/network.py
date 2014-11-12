#!usr/bin/python3.4
# -*-coding:utf-8 -*

import pygraphviz as pgv
from node import Node, Link


class Network:
    """le RC"""

    def __init__(self, graph):
        self.network = []
        self.graph = pgv.AGraph(directed=True, overlap=False)
        if(graph):  # si on a passé un graphe en argument
            for i in graph.nodes():
                liste = i.__str__().split("_")
                self.addNode(Node(liste[0], int(liste[1]),
                                  (int(i.attr['fontsize'])-10)*100/40))

            for i in graph.edges():
                l1 = i[0].__str__().split("_")
                name1 = l1[0]
                l2 = i[1].__str__().split("_")
                name2 = l2[0]

                lnk = Link(int(i.attr['weight']), self.seek(i.attr['label'])
                           if 'label' in i.attr else None)
                self.addLink(self.seek(name1), self.seek(name2), lnk)

        for n1 in self.network:
            self.graph.get_node(n1.__str__()).attr['fontsize'] = 35
        self.graph.layout()

    def addNode(self, n):
        self.network.append(n)
        self.graph.add_node(n.__str__(), shape='box')

    def addLink(self, n1, n2, lnk):
        n1.addLink(lnk, n2)
        if(lnk.label):
            self.graph.add_edge(n1.__str__(), n2.__str__(),
                                label=lnk.label, weight=lnk.p)
        else:
            self.graph.add_edge(n1.__str__(), n2.__str__(), weight=lnk.p)

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
        for n1 in self.network:
            self.graph.get_node(n1.__str__()).attr['fontsize'] = (
                (n1.a)*40/100+10)
            # if len(n1.linksOut)+len(n1.linksIn) = =0:
            #     self.graph.get_node(n1.__str__()).attr['style'] = "invis"
            # else:
            #     self.graph.get_node(n1.__str__()).attr['style'] = ""
        for n1 in self.network:
            for d, l in n1.linksOut.items():
                if(l.label):
                    self.graph.get_edge(
                        n1.__str__(), d.__str__()).attr['weight'] = l.p
                else:
                    self.graph.get_edge(
                        n1.__str__(), d.__str__()).attr['weight'] = l.p
        return self.graph
