#!usr/bin/python3.4
# -*-coding:utf-8 -*

from random import random
from node import Node
from workspace import *
from worker import *

"""
Workers which act directly on the workspace
"""

class ReadAndWrite(Worker):
    """
    Read a word/concept from the text (already parsed with grammatics)
    and creates a node in the workspace
    
    Acts on the workspace, and the conceptnetwork
    """

    def __init__(self, word, grammatical_role):
        """
        Here, the grammatical_role is seen as a synthesis of how the concept is used :
        is it a subject ? An object ?
        It will be saved into the workspacenode created.
        
        It is very important to read new information.
        Thus, worker's importance is set to 90.
        """
        
        Worker.__init__(self, 90)
        self.word=word
        self.grammatical_role=grammatical_role
   
  
#todo : use grammatical role !!!
    def launch(self):
        """
        if the word is not recognized as a concept
        we should see it differently : it may be the name of someone, etc.
        
        If the word is recognized, we activate the corresponding concept after writing down the new workspace node.
        """
        Worker.launch(self)
        nodefather=conceptnetwork.seek(self.word)
        realnode=search_real_node(self.word)

        if(realnode):
            pushRandom(Activate(nodefather, 40))
            
        else:
            phantomnode=search_phantom_node(self.word)
            if(phantomnode):
                temp=RealNode(role=self.grammatical_role,father=nodefather)
                add_real_node(temp)
                temp.phantom_links=phantomnode.phantom_links
                temp.real_links=phantomnode.real_links
                temp.satisfaction=nodefather.activation
                pushRandom(Activate(nodefather, 30))
                
            else: 
                if(not(nodefather)):
                    add_real_node(RealNode(role=self.grammatical_role, 
                    father=None, name=self.word, importance=25))
                else:
                    add_real_node(RealNode(role=self.grammatical_role, 
                    father=nodefather))
                    pushRandom(Activate(nodefather,30))

    def __str__(self):
        return("Writing down new workspacenode "+word)

class WriteConcept(Worker):
    """Write a concept of the conceptnetwork into the workspace.
    
    Acts on the workspace, and the conceptnetwork.
    """
    
    def __init__(self, target_node):
        """
        Target_node is an activated node of the conceptnetwork. 
        The worker attempts to create an instance of this node.
        
        It is very important to write down new information.
        Thus, the worker's importance is set to 80.
        """
        Worker.__init__(self, 80)
        self.target_node = target_node
    
#todo : search for links and related nodes after phantomnode creation
#todo : search if the node already exists !!!
#then see if it has to create another concept instantation !!
    def launch(self):
        """
        Deactivates the node and creates a phantom node.
        """
        Worker.launch(self)
        self.target_node.activation=max(self.target_node.activation-50, 0)
        add_phantom_node(PhantomNode(father=target_node))

    def __str__(self):
        return("Writing down concept "+self.target_node.name)

class BuildLink(Worker):
    """
    Build new links in the workspace, being influenced by concepts activation.
    """
    
    def __init__(self, target_node):
        """
        Here, target_node is a node of the workspace itself (a RealNode to begin with)
        """
        Worker.__init__(self, min(100, target_node.importance))#importance between 0 and 100
        self.target_node=target_node
        
        
    def launch(self):
        Worker.launch(self)
        if(self.target_node.father):
            for node in self.target_node.linksOut.keys():
                if(node.activation>50):#TODO : search for already instantiated nodes
                
                    temp=search_real_node(target_node.name)
                    temp2=search_phantom_node(target_node.name)
                    if(temp):
                        target_node.add_real_link(workspacenode=temp, importance=node.activation)
                        target_node.add_satisfaction(10)
                    elif(temp2):
                        target_node.add_phantom_link(workspacenode=temp2, importance=node.activation)
                        target_node.add_satisfaction(10)
                    else:
                        target_node.add_satisfaction(5)
                        pushRandom(WriteConcept(node))
                        pushRandom(BuildLink(target_node))
                    
    def __str__(self):
        return("Searching links for node "+target_node.__str__())

class ReadTitle(Worker):
    """Read some important information
    """
