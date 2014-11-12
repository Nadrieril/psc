#!usr/bin/python3.4
# -*-coding:utf-8 -*

from collections import deque
from random import shuffle


class Worker:
    """The workers act on several objects : they activate nodes, create some...
	The main class Worker has subclasses for every type of worker
	It also contains the global static list of workers, used by the programme
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
	(it has to depend on the type and urgency of the worker)
	"""
        Worker.push(t)
        shuffle(Worker.workers)

    def launch(self):
        """
	launch the worker, increase the time
	"""
        Worker.time += 1

    def __init__(self, urgency=0):
        self.urgency=urgency


class Activate(Worker):
    """Activate a node (increase node's activation)"""
    """It is urgent to activate nodes. Thus, worker's urgency is set to 100 (maximum)"""



    def __init__(self, target_node, activation_to_add, **kwds):
        self.target_node = node
        self.activation_to_add = activation_to_add
        super().__init__(100)

    def launch(self):
	"""
	The Activate workers generates new Compute workers for every linked node
	"""
        self.target_node.activation += self.activation_to_add
        for n in self.target_node.linksOut.keys():
            Worker.pushRandom(Compute(n))
        super().launch()



class Compute(Worker):
    """compute node activation : creates new "Compute" workers"""

    def __init__(self, target_node):
        self.target_node = target_node
        super().__init__(50)

    def launch(self):
        self.target_node.compute_activation()
        if(self.target_node.has_observer):#if the node is observed
            self.target_node.observer.update(Worker.time, self.target_node.activation)
        for n in self.target_node.linksOut.keys():
            Worker.pushRandom(Compute(n))
        super().launch()


class Write(Worker):
    """Write into the workspace"""


class ReadTitle(Worker):
    """Read some important information"""
