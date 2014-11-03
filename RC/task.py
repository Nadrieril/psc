#!usr/bin/python3.4
# -*-coding:utf-8 -*

from collections import deque

class Task:
    """superclasse pour les actions à déposer dans la file d'attente. Les tâches agissent sur des noeuds déjà déterminés."""
    """Les tâches n'ont accès qu'à des noeuds et qu'à la file générale"""
    
    tasks=deque()#objet de type deque (file d'attente)
    time=0


    @staticmethod
    def pop():
        Task.tasks.popleft().launch()

    @staticmethod
    def push(t):
        Task.tasks.append(t)
    
    @staticmethod
    def pushRandom(t):
        Task.push(t)#à changer pour introduire des tâches à une position aléatoire (il faut surtout avoir le choix)

    def launch(self):
        """effectue l'action (sans la retirer de la file où elle se situe)"""
        time+=1


class Read(Task):
    """action consistant à lire une instruction (sous forme de triplet : sujet, action, objet)"""
    
    def __init__(self,node1, action, node2):
        self.node1=node1
        self.action=action
        self.node2=node2
    
    def launch(self):
        Task.time+=1
        self.node1.a+=20
        self.node2.a+=20
        self.action.a+=10
        #action un peu bizarre de l'ordre du test
        for n in self.node1.linksOut.keys() :
            Task.pushRandom(Compute(n))
        #doit ensuite créer des objets dans le W, etc

class Compute(Task):
    """action consistant à calculer l'activation d'un noeud"""
    
    def __init__(self, node):
        self.node=node
    
    def launch(self):
        Task.time+=1
        self.node.computeActivation()
        if(self.node.isObserved):
            self.node.observer.update(Task.time, self.node.a)
        for n in self.node.linksOut.keys() :
            Task.pushRandom(Compute(n))


class Write(Task):
    """action consistant à écrire un mot dans le W"""
    
    
class ReadTitle(Task):
    """action consistant à lire une info importante"""
