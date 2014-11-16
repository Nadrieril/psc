#!usr/bin/python3.4
# -*-coding:utf-8 -*

from random import random
from node import Node
from workspace import *
from worker import *

"""
Workers which act directly on the workspace
"""

__all__=['BuildLink', 'ReadAndWrite', 'WriteConcept']

READANDWRITE_URGENCY=90
CONCEPT_ACTIVATION_WHILE_READING_FIRST_TIME=40
CONCEPT_ACTIVATION_WHILE_READING_OTHER_TIME=40
WRITECONCEPT_URGENCY=80
CONCEPT_DEACTIVATION_WHILE_WRITING_DOWN=50
BUILDLINK_URGENCY=80


def read_and_write(word,  grammatical_role):
    nodefather=conceptnetwork.seek(self.word)
    realnode=search_real_node(self.word)
    phantomnode=search_phantom_node(self.word)
    
    
    if(nodefather and not(realnode) and not(phantomnode)):
        pushRandom(Activate(nodefather, CONCEPT_ACTIVATION_WHILE_READING_FIRST_TIME))
        temp=RealNode(role=grammatical_role,father=nodefather)
        add_real_node(temp)
        pushRandom(BuildLink(temp))
        
    elif(nodefather and not(realnode) and phantomnode):
        temp=RealNode(role=grammatical_role,father=nodefather)
        add_real_node(temp)
        temp.phantom_links=phantomnode.phantom_links
        temp.real_links=phantomnode.real_links
        temp.satisfaction=nodefather.activation
        pushRandom(Activate(nodefather, CONCEPT_ACTIVATION_WHILE_READING_OTHER_TIME))
        pushRandom(BuildLink(temp))
    
    elif(nodefather and realnode and not(phantomnode)):
        temp=realnode
        pushRandom(Activate(nodefather, CONCEPT_ACTIVATION_WHILE_READING_OTHER_TIME))
        pushRandom(BuildLink(realnode))
        
    elif(not(nodefather) and realnode):
        temp=realnode
        pushRandom(BuildLink(realnode))
        
    elif( not(nodefather) and not(realnode)):
        temp=RealNode(role=grammatical_role,father=None)
        add_real_node(temp)
        pushRandom(BuildLink(temp))
    else:
        raise(WorkerException)
        
    return(temp)
    


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
        
        Worker.__init__(self, READANDWRITE_URGENCY)
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
        phantomnode=search_phantom_node(self.word)
        
        if(nodefather and not(realnode) and not(phantomnode)):
            pushRandom(Activate(nodefather, CONCEPT_ACTIVATION_WHILE_READING_FIRST_TIME))
            temp=RealNode(role=self.grammatical_role,father=nodefather)
            add_real_node(temp)
            pushRandom(BuildLink(temp))
            
        elif(nodefather and not(realnode) and phantomnode):
            temp=RealNode(role=self.grammatical_role,father=nodefather)
            add_real_node(temp)
            temp.phantom_links=phantomnode.phantom_links
            temp.real_links=phantomnode.real_links
            temp.satisfaction=nodefather.activation
            pushRandom(Activate(nodefather, CONCEPT_ACTIVATION_WHILE_READING_OTHER_TIME))
            pushRandom(BuildLink(temp))
        
        elif(nodefather and realnode and not(phantomnode)):
            pushRandom(Activate(nodefather, CONCEPT_ACTIVATION_WHILE_READING_OTHER_TIME))
            pushRandom(BuildLink(realnode))
            
        elif(not(nodefather) and realnode):
            pushRandom(BuildLink(realnode))
            
        elif( not(nodefather) and not(realnode)):
            temp=RealNode(role=self.grammatical_role,father=None)
            add_real_node(temp)
            pushRandom(BuildLink(temp))
        else:
            raise(WorkerException)


    def __str__(self):
        return("Writing down new workspacenode "+word)

class WriteLink(Worker):
    
    """
    Writes down a link between two nodes. If the nodes don't exist, the link is not written.
    """
    
    def __init__(self, target_1, target_2, label=None):
        Worker.__init__(self, 80)
        self.target_1=target_1
        self.target_2=target_2
        self.label=label   


    def launch(self):
        Worker.launch(self)
        node1=search_real_node(target_1)
        node2=search_real_node(target_2)
        if(label):
            node3=search_real_node(label)
        else:
            node3=None
        if(node1 and node2):
            node1.add_real_link(workspacenode=node2, importance=0, label=node3)


    def __str__(self):
        return("Creating and building a link between "+self.target_1.__str__()+
        " and "+self.target_2.__str__())

class ReadAndWriteLink(Worker):
    
    def __init__(self, target_1, target_2, label=None):
        Worker.__init__(self, 80)
        self.target_1=target_1
        self.target_2=target_2
        self.label=label
    
    
    def launch(self):
        Worker.launch(self)
        node1=read_and_write(word=target_1[0], grammatical_role=target_1[1])
        node2=read_and_write(word=target_2[0], grammatical_role=target_2[1])
        if(label):
            node3=read_and_write(word=label[0], grammatical_role=label[1])
        else:
            node3=None
            
        node1.add_real_link(workspacenode=node2, importance=0, label=node3)


    def __str__(self):
        return("Creating and building a link between "+self.target_1.__str__()+
        " and "+self.target_2.__str__())


class WriteConcept(Worker):
    """Write a concept of the conceptnetwork into the workspace.
    
    Acts on the workspace, and the conceptnetwork.
    """
    
    def __init__(self, target_node):
        """
        Target_node is an activated node of the conceptnetwork. 
        The worker attempts to create an instance of this node.
        
        It is very important to write down new information.
        """
        Worker.__init__(self, WRITECONCEPT_URGENCY)
        self.target_node = target_node
    
#todo : search for links and related nodes after phantomnode creation
#todo : search if the node already exists !!!
#then see if it has to create another concept instantation !!
    def launch(self):
        """
        Deactivates the node and creates a phantom node.
        """
        Worker.launch(self)
        phantomnode=search_phantom_node(self.target_node.name)
        realnode=search_real_node(self.target_node.name)
        
        if(not(phantomnode) and not(realnode)):
            add_phantom_node(PhantomNode(father=target_node))
            self.target_node.activation=max(self.target_node.activation-CONCEPT_DEACTIVATION_WHILE_WRITING_DOWN, 0)
        elif(realnode):
            push(BuildLink(realnode))
        elif(phantomnode):
            push(BuildLink(phantomnode))

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

class BuildLinkSubject(Worker):
    
    """Builds links for a subject : links action -> object
    """

class BuildLinkObject(Worker):
    
    """Builds links for an object..."""

class ReadTitle(Worker):
    """Read some important information
    """
