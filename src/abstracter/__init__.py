try:
    from concepts_network import *
    from workers.activate_worker import *
except ImportError:
    pass



class Context:
    
    
    def __init__(self):
        self.workersManager=WorkersManager()
        self.network=Network()

    def test(self):
        self.network=Network()
        self.network.add_node(id="babar",ic=2,activation=0)
        self.network.add_edge(fromId="toto",toId="babar",weight=20,r="nothing in common")
        self.network.add_edge(fromId="toto",toId="elephant",weight=100,r="useless")
        self.workersManager.push(ActivateWorker("toto",60))
        self.run(10)
        print(self.network["babar"]["a"])

    def run(self,max_time):
        while self.workersManager.time<max_time and not self.workersManager.isEmpty():
            print(self.workersManager)
            self.workersManager.runWorker(self)
        print(self.workersManager)

if __name__=="__main__":
	c=Context()
	c.test()




