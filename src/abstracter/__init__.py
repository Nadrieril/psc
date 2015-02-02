try:
    from concepts_network import *
    from workers.activate_worker import *
except ImportError:
    from abstracter.concepts_network import *
    from abstracter.workers.activate_worker import *



class Context:
    
    
    def __init__(self,network=None):
        self.workersManager=WorkersManager()
        self.network=(network if network else Network())

    def test(self):
        self.network=ConceptNetwork()
        self.network.add_node(id="babar",ic=2,a=0)
        self.network.add_edge(fromId="toto",toId="babar",w=20,r="nothing in common")
        self.network.add_edge(fromId="toto",toId="elephant",w=100,r="useless")
        print(self.network["toto"])
        self.workersManager.push(ActivateWorker("toto",60))
        self.run(10)
        print(self.network["babar"]["a"])

    def activate(self,node,activation):
        self.workersManager.push(ActivateWorker(node,activation))

    def print_activated_nodes(self):
        for n,d in self.network.nodes():
            if d['a'] > 0:
                print(n+" : "+d['a'].__str__())

    def run(self,max_time):
        while self.workersManager.time<max_time and not self.workersManager.isEmpty():
            print(self.workersManager)
            #self.print_activated_nodes()
            self.workersManager.runWorker(self)
        print(self.workersManager)

if __name__=="__main__":
	c=Context()
	c.test()




