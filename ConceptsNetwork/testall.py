# !usr/bin/python3.4
# -*-coding:utf-8 -*

import pygraphviz as pgv

from conceptnetwork import *
from node import *
import worker as w
from workspace import *

"""
This file is intended to be a test of the global architecture.

Entry of the test : the phrase :

Wayne Rooney celebrated his appointment as England captain.

parsed as something like :

[WayneRooney,subject],[celebrate,action],[his,other],[appointment,object],[as,other],
[England,object],[captain,object]

So a list of tuples. Read such a list implies reading every tuple in order.
"""


def work(time_max):
    """Function which makes the programme run
    """
    while len(w.workers) != 0 and w.time < me_maxt:
        w.pop()
        G = net1.to_graph()
        #G.layout()
        G.draw("CN/CNtime{0}.png".format(w.time))
        save_workspace_graph("W/Wtime{0}.png".format(w.time))

net1 = ConceptNetwork.load("RC.txt");
w.activate_messages()



w.push(Activate(net1.seek("WayneRooney"), 30))
w.push(Activate(net1.seek("celebrate"), 10))
w.push(Activate(net1.seek("appointment"), 20))
w.push(Activate(net1.seek("as"), 5))
w.push(Activate(net1.seek("captain"), 20))
w.push(Activate(net1.seek("english"), 10))
w.push(Activate(net1.seek("team"), 20))

work(30)

net1.save("RCfinal.txt")
