#!/usr/bin/python3.4
# -*-coding:utf-8 -*

from random import random

"""
Main worker class and manager
"""


class WorkerException(Exception):
    pass

class Worker:
    """
    The workers act on several objects : they activate nodes, create some...
    The main class Worker has subclasses for every type of worker.
    """

    def __init__(self, urgency=0):
        self.urgency = urgency

    def run(self, context):
        return 0

    def __str__(self):
        return("Worker, urgency : " + self.urgency)


class WorkersManager:
    def __init__(self):
        self.workers = []
        self.time = 0


    def pop(self):
        return self.workers.pop(0)

    def pushEnd(self, w):
        self.workers.append(w)

    def push(self, w):
        """
        Push a new worker into the queue, but randomly
        (it has to depend on the urgency of the worker)
        """
        i = 0
        while i < len(self.workers) and self.workers[i].urgency > w.urgency:
            i += 1
        i += int((random() - 0.5) * len(self.workers) / 15)
        self.workers.insert(i, w)

    def isEmpty(self):
        return self.workers==[]

    def runWorker(self, context, w=None):
        w = w or self.pop()
        delta_time = w.run(context)
        self.time += delta_time


    def __str__(self):
        res="WorkersManager : \nTime = "+self.time.__str__() \
        +"\n"+len(self.workers).__str__()+" workers :"
        for w in self.workers:
            res+="\n"+w.__str__()
        return res
