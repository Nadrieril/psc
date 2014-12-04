from workers import Worker

COMPUTE_URGENCY = 50

class ComputeWorker(Worker):
    """
    Workers which compute nodes' activation.
    """

    def __init__(self, target_node):
        """
        It is important to compute node's activation, but there are things more important to do.
        Thus, the worker's importance is set to 50
        """
        super(ComputeWorker, self).__init__(COMPUTE_URGENCY)
        self.target_node = target_node

    def run(self, context):
        """
        Computes node's activation.
        Then pushes new compute workers for each neighbour node in the workspace.
        Also, send a signal to the node's observer if there is one.
        """
        self.target_node.compute_activation()
        if(self.target_node.has_observer):
            self.target_node.observer.update(context.manager.time, self.target_node.activation)
        for n in self.target_node.linksOut.keys():
            context.manager.pushRandom(ComputeWorker(n))

    def __str__(self):
        return "Calculation of concept " + self.target_node.name + \
            "\'s activation"
