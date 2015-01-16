from abstracter import Context
from abstracter.concepts_network import *

n=ConceptNetwork()
n.load_from_JSON_stream(nodes_files=["wayne_nodes.jsons"],edges_files=["wayne_edges.jsons"])

c=Context(n)
c.activate("ball_sport",60)
c.run(5)

def print_activated_nodes(network):
	for n,d in network.nodes():
		if d['a'] > 0:
			print(n+" : "+d['a'].__str__())

print_activated_nodes(n)