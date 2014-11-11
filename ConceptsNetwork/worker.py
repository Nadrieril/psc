#!usr/bin/python3.4
# -*-coding:utf-8 -*

from collections import deque
from random import shuffle


class Worker:
    """The workers act on several objects : they activate nodes, create some...
	The main class Worker has subclasses for every type of worker
	It also contains the global static list of workers, used by the program
    """


    workers = deque()#global static queue of workers
    time = 0#each action increases time

    @staticmethod
    def pop():
        Worker.workers.popleft().launch()

    @staticmethod
    def push(t):
        Worker.workers.append(t)

    @staticmethod
    def pushRandom(t):
	"""
	Push a new worker into the queue, but randomly
	(it has to depend on the type and importance of the worker)
	"""
        Worker.push(t)
        shuffle(Worker.workers)

    def launch(self):
        """
	launch the worker, increase the time
	"""
        self.time += 1


class Activate(Worker):
    """Activate a node (increase node's activation)"""


    def __init__(self, node, newact):
        self.node = node
        self.newact = newact

    def launch(self):
	"""
	The Activate workers generates new Compute workers for every linked node
	"""
        Worker.time += 1
        self.node.activation += self.newact
        for n in self.node.linksOut.keys():
            Worker.pushRandom(Compute(n))



class Compute(Worker):
    """compute node activation : creates new "Compute" workers"""

    def __init__(self, node):
        self.node = node

    def launch(self):
        Worker.time += 1
        self.node.compute_activation()
        if(self.node.has_observer):#if the node is observed
            self.node.observer.update(Worker.time, self.node.a)
        for n in self.node.linksOut.keys():
            Worker.pushRandom(Compute(n))


class Write(Worker):
    """Write into the workspace"""


class ReadTitle(Worker):
    """Read some important information"""
