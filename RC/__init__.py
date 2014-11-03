#!usr/bin/python3.4
# -*-coding:utf-8 -*

import os
import matplotlib.pyplot as plt
from numpy import *
from node import *
from total import *
from task import *
from random import *
import networkx as nx

import pygraphviz as pgv

#initialisation du graphe, et du RC à partir du fichier
A=pgv.AGraph("RC.dot")
net1=Network()

for i in A.nodes():
    liste=i.__str__().split("_")
    net1.addNode(Node(liste[0], int(liste[1]), (int(i.attr['fontsize'])-10)*100/40))

for i in A.edges():
    l1=i[0].__str__().split("_")
    name1=l1[0]
    l2=i[1].__str__().split("_")
    name2=l2[0]
    if(i.attr['label'] ):
        net1.seek(name1).addLink(Link(int(i.attr['weight']), net1.seek(i.attr['label'])),  net1.seek(name2))
    else:
        net1.seek(name1).addLink(Link(int(i.attr['weight'])),  net1.seek(name2))

A.layout()
A.draw("initial.png")
#lancement des tâches et des observateurs

o=NodeObserver()
net1.seek("captain").addObserver(o)

Task.push(Read(net1.seek("WayneRooney"), net1.seek("celebrate"), net1.seek("appointment")))
Task.push(Read(net1.seek("appointment"), net1.seek("as"), net1.seek("captain")))
Task.push(Read(net1.seek("fans"), net1.seek("turnsbsback"), net1.seek("team")))



def work():
    while (len(Task.tasks))<>0  and (Task.time<30)  : #tant que ce n'est pas vide
        #print(Task.time)
        Task.pop()

work()

o.draw()

#tracé final du graphe
G=net1.to_graph()
G.layout()
G.draw("final.png")
G.write("final.dot")

