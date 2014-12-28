import networkx as nx
from networkx.readwrite import json_graph
from math import log
import matplotlib.pyplot as plt
import json
try:
    from abstracter.util.json_stream import *
except ImportError:
    pass



"""
The workspace is supposed to be smaller than the concept network.
It is also stored as a network object, using networkx.

Beginning : we use the class Network from concepts_network
"""


class Workspace:
    pass


