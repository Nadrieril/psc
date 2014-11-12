# !usr/bin/python3.4
# -*-coding:utf-8 -*


from conceptnetwork import *
from node import NodeObserver, Node
from worker import Worker, Activate

import pygraphviz as pgv


# small function to make the network run
def work(nbetapes):
    while len(Worker.workers) != 0 and Worker.time < nbetapes:
        # tant que ce n'est pas vide
        # print(Worker.time)
        Worker.pop()
        G = net1.to_graph()
        #G.layout()
        G.draw("figures/RCetape{0}.png".format(Worker.time))



net1 = ConceptNetwork.load("RC.txt");
net1.save("RCfinal.txt")
net1.to_graph().draw("figures/RCetape0.png")

# lancement des tâches et des observateurs
#o = NodeObserver()

#net1.seek("captain").addObserver(o)


Worker.push(Activate(net1.seek("WayneRooney"), 30))
Worker.push(Activate(net1.seek("celebrate"), 10))
Worker.push(Activate(net1.seek("appointment"), 20))
Worker.push(Activate(net1.seek("as"), 5))
Worker.push(Activate(net1.seek("captain"), 20))
Worker.push(Activate(net1.seek("english"), 10))
Worker.push(Activate(net1.seek("team"), 20))

work(30)

net1.save("RCfinal.txt")


# o.draw()
