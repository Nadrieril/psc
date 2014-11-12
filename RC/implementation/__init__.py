# !usr/bin/python3.4
# -*-coding:utf-8 -*

from network import Network, NodeObserver
from task import Task, Activate

import pygraphviz as pgv


# petite fonction importante
def work(nbetapes):
    while len(Task.tasks) != 0 and Task.time < nbetapes:
        # tant que ce n'est pas vide
        # print(Task.time)
        Task.pop()
        G = net1.to_graph()
        # G.layout()
        G.draw("figures/RCetape{0}.png".format(Task.time))


# initialisation du graphe, et du RC à partir du fichier
A = pgv.AGraph("RC.dot")
net1 = Network(A)


A.layout()
A.draw("initial.png")
net1.to_graph().draw("figures/RCetape0.png")
# lancement des tâches et des observateurs

o = NodeObserver()
net1.seek("captain").addObserver(o)

Task.push(Activate(net1.seek("WayneRooney"), 30))
Task.push(Activate(net1.seek("celebrate"), 10))
Task.push(Activate(net1.seek("appointment"), 20))
Task.push(Activate(net1.seek("as"), 5))
Task.push(Activate(net1.seek("captain"), 20))
Task.push(Activate(net1.seek("english"), 10))
Task.push(Activate(net1.seek("team"), 20))

work(30)

# tracé final du graphe
# G=net1.to_graph()
# G.layout()
# G.write("final.dot")

# o.draw()
