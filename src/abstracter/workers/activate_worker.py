try:
    from workers_settings import *
    from compute_worker import ComputeWorker
except ImportError:
    from abstracter.workers.workers_settings import *
    from abstracter.workers.compute_worker import *

class ActivateWorker(Worker):
    """
    Worker which activates a node in the conceptnetwork
    """

    def __init__(self, target_id, activation_to_add):
        """
        """
        super(ActivateWorker, self).__init__(ACTIVATE_URGENCY)
        self.target_id = target_id
        self.activation_to_add = activation_to_add


    def run(self, context):
        """
        The Activate worker generates new Compute workers for every linked node
        It pushes a writeConcept worker if the node is activated enough
        """
        context.network[self.target_id]['a'] += self.activation_to_add
        if context.network[self.target_id]['a'] > ACTIVATION_ENABLING_CONCEPT_INSTANTIATION:
            pass
            #context.workers.push(WriteConceptWorker(self.target_id))
        for n in context.network.successors(self.target_id):
            context.workersManager.push(ComputeWorker(n))
        return ACTIVATE_DELTA_TIME


    def __str__(self):
        return "Activation of concept " + self.target_id + \
            " by " + self.activation_to_add.__str__()
