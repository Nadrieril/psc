#!usr/bin/python3.4
# -*-coding:utf-8 -*

from random import random
from node import Node
from workspace import *

"""
Main class worker, some functions, and 
workers which act only on the conceptnetwork
"""


__all__=['pop','push','Worker','Activate', 'Compute',  'activate_messages', 'deactivate_messages', 'increase_time']

workers = []#global static queue of workers
time = 0
print_messages=False

ACTIVATION_ENABLING_CONCEPT_INSTANTIATION=80
ACTIVATE_URGENCY=100
COMPUTE_URGENCY=50

def increase_time():
    global time
    time=time+1
    

def pop():
    global workers
    workers.pop(0).launch()

def push(t):
    global workers
    workers.append(t)

def pushRandom(t):
    """
    Push a new worker into the queue, but randomly
    (it has to depend on the urgency of the worker)
    """
    i=0
    while(i<len(workers) and workers[i].urgency>t.urgency):
        i+=1
    i+=int((random()-0.5)*len(workers)/15)
    workers.insert(i, t)
    

def print_workers():
    for w in workers:
        print(w)


def activate_messages():
    global print_messages
    print_messages=True

def deactivate_messages():
    global print_messages
    print_messages=False


class WorkerException(Exception):
    pass

class Worker:
    """The workers act on several objects : they activate nodes, create some...
    The main class Worker has subclasses for every type of worker.
    """

    def launch(self):
        """
        launch the worker, increase the time
        """
        increase_time()
        if(print_messages):
            print(self.log_message())
        


    def __init__(self, urgency=0):
        self.urgency=urgency

 
    def __str__(self):
        return("Worker, urgency : "+self.urgency.__str__())

    def log_message(self):
        """
        Default message when launching"""
        return(self.__str__())


class Activate(Worker):
    """Worker which activates a node (increase node's activation)
    
    Acts only on the conceptnetwork.
    """

    def __init__(self, target_node, activation_to_add):
        """
        It is urgent to activate nodes. Thus, worker's urgency is set to 100 (maximum)
        """
        Worker.__init__(self, ACTIVATE_URGENCY)
        self.target_node = target_node
        self.activation_to_add = activation_to_add


    def launch(self):
        """
        The Activate worker generates new Compute workers for every linked node
        It pushes a writeConcept worker if the node is activated enough
        """
        Worker.launch(self)
        self.target_node.activation += self.activation_to_add
        if(self.target_node.activation>ACTIVATION_ENABLING_CONCEPT_INSTANTIATION):
            pushRandom(WriteConcept(target_node))
        for n in self.target_node.linksOut.keys():
            pushRandom(Compute(n))


    def __str__(self):
        return("Activation of concept "+self.target_node.name+" by "+self.activation_to_add.__str__())


class Compute(Worker):
    """
    Workers which compute nodes' activation.
    
    Acts only on the conceptnetwork.
    """

    def __init__(self, target_node):
        """
        It is important to compute node's activation, but there are things more important to do.
        Thus, the worker's importance is set to 50
        """
        Worker.__init__(self, COMPUTE_URGENCY)
        self.target_node = target_node

    def launch(self):
        """
        Computes node's activation.
        Then pushes new compute workers for each neighbour node in the workspace.
        Also, send a signal to the node's observer if there is one.
        """
        Worker.launch(self)
        self.target_node.compute_activation()
        if(self.target_node.has_observer):#if the node is observed
            self.target_node.observer.update(time, self.target_node.activation)
        for n in self.target_node.linksOut.keys():
            pushRandom(Compute(n))

    def __str__(self):
        return("Calculation of concept "+self.target_node.name+"\'s activation")



if __name__=="__main__":
    activate_messages()
    toto=Activate(Node("toto", 4), 50)
    push(toto)
    toto.launch()
    toto2=RealNode(father=Node("toto", 4))
