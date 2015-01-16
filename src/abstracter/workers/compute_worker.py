try:
    from workers.workers_settings import *
    from workers import *
except ImportError:
    from abstracter.workers.workers_settings import *
    from abstracter.workers import *

class ComputeWorker(Worker):
    """
    Workers which compute nodes' activation.
    """

    def __init__(self, target_id):
        """
        :param target_id: id of the node to activate (a node in the conceptnetwork)
        :type target_id: str
        """
        super(ComputeWorker, self).__init__(COMPUTE_URGENCY)
        self.target_id = target_id

    def run(self, context):
        """
        Computes node's activation.
        Then pushes new compute workers for each neighbour node in the workspace.
        """
        context.network.compute_activation(self.target_id)
        for n in context.network.successors(self.target_id):
            context.workersManager.push(ComputeWorker(n))
        return(COMPUTE_DELTA_TIME)

    def __str__(self):
        return "Calculating act of concept " + self.target_id
