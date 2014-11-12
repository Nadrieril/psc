#!usr/bin/python3.4
# -*-coding:utf-8 -*



#from enum import Enum

#class Grammatic(Enum):
#    subject=0
#    object=1

from node import *
from conceptnetwork import *
from worker import *

class Workspace:
    """
    Most important part of the architecture.
    The workspace has to contain all information that is retrieved from the text.
    """
    

class WorkspaceNode:
    
    def __init__(self, father, links={}):
        self.father=father#father node, from the RC 
        self.name=self.father.name
        self.importance=father.ic#the node's importance can evolve by itself
        self.links=links

    def __str__(self):
        return(self.name)

    
    
class RealNode(WorkspaceNode):
    """
    Node in the workspace. They can be created, deleted.
    """
    
    def __init__(self, role='subject',  **kwds):
        self.satisfaction=0
        self.role=role#subject default for me
        super(RealNode, self).__init__(**kwds)



class PhantomNode:
    """Node created by activation of a concept which is not in the text"""
    """it is not a concept instantiation, just a mirror"""
    
    def __init__(self, **kwds):
        super(PhantomNode, self).__init__(**kwds)

    

    
    
if __name__=="__main__":
    toto=RealNode(father=Node("toto", 4), role="object", links={})
    print(toto)
