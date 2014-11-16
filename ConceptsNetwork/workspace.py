#!usr/bin/python3.4
# -*-coding:utf-8 -*



#from enum import Enum

#class Grammatic(Enum):
#    subject=0
#    object=1

import pygraphviz as pgv
from node import *
from conceptnetwork import *
from worker import *

"""
Most important part of the architecture.
The workspace has to contain all information that is retrieved from the text.
    
Main class Workspace has static lists of nodes.
To access them we use methods like :
add_phantom_node
add_real_node
search_phantom_node
search_real_node

Which are more reliable.
"""
    
__all__=['RealNode','PhantomNode','set_conceptnetwork', 'add_phantom_node',
'add_real_node', 'search_real_node', 'search_phantom_node', 'save_workspace_graph']    

real_nodes=[]
phantom_nodes=[]
conceptnetwork=None
    

def set_conceptnetwork(CN):
    conceptnetwork=CN
    

def add_phantom_node(phantom_node):
    phantom_nodes.append(phantom_node)
    

def add_real_node(real_node):
    real_nodes.append(real_node)


def search_real_node(node_name):
    """
    Seek among the real nodes, for a node named 'node_name'
    """
    res = None
    for node in real_nodes:
        if(node.name == node_name):
            res = node
    return(res)
  

def search_phantom_node(node_name):
    """
    Seek among the phantom nodes, for a node named 'node_name'
    """
    res = None
    for node in phantom_nodes:
        if(node.name == node_name):
            res = node
    return(res)    


def save_workspace_graph(file_name):
    graph=pgv.AGraph(directed=True, overlap=False)
    for node in real_nodes:
        graph.add_node(node.__str__(), shape='box', fontsize=node.importance)
        for other_node in node.real_links.keys():
            graph.add_edge(node, other_node)
        for other_node in node.phantom_links.keys():
            graph.add_edge(node, other_node)
    for node in phantom_nodes:
        graph.add_node(node.__str__(), fontsize=node.importance)
        for other_node in node.real_links.keys():
            graph.add_edge(node, other_node)
        for other_node in node.phantom_links.keys():
            graph.add_edge(node, other_node)
    graph.layout()
    graph.draw(file_name)
    

class WorkspaceNode:
    """
    Superclass for every type of node in the workspace.
    
    Each node has links to other nodes.
    workspacenode.real_links : real links, which may appear in the final summary
    workspacenode.phantom_links : they will not appear, but may be used in the computation
    """
    
    
    def __init__(self, father=None,name=None,importance=0,real_links={}, phantom_links={}):
        self.father=father#father node, from the conceptnetwork
        if(name):
            self.name=name
        elif(father):
            self.name=self.father.name
        else:
            self.name="No_name"
        
        if(father):
            self.importance=min(100,father.ic/10*father.activation)
            #the node's importance can evolve by itself
        self.real_links=real_links#links to real nodes
        self.phantom_links=phantom_links#links to phantom_nodes
        self.satisfaction=0

    def add_satisfaction(self, sat):
        self.satisfaction=min(100, self.satisfaction+sat)


    def __str__(self):
        return(self.name)

    
    def add_real_link(self, workspacenode, importance=0, label=None):
        self.real_links.update({workspacenode : (importance, label)})


    def add_phantom_link(self, workspacenode, importance=0, label=None):
        self.phantom_links.update({workspacenode : (importance, label)})
    
    
class RealNode(WorkspaceNode):
    """
    Node in the workspace. They can be created, deleted.
    """
    
    def __init__(self, role='subject',  **kwds):
        self.role=role#default = subject
        WorkspaceNode.__init__(self, **kwds)



class PhantomNode(WorkspaceNode):
    """Node created by activation of a concept which is not in the text
    
    It is not a concept instantiation, just a mirror
    """
    
    def __init__(self, **kwds):
        WorkspaceNode.__init__(self, **kwds)

    

    
    
if __name__=="__main__":
    toto=RealNode(father=Node("toto", 4), role="object", real_links={})
    add_real_node(toto)
    print(real_nodes)
    print(toto)
    print(search_real_node("toto"))
