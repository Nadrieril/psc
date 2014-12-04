from workers import Worker, WriteConceptWorker, ComputeWorker

ACTIVATE_URGENCY = 100
ACTIVATION_ENABLING_CONCEPT_INSTANTIATION = 80

class ActivateWorker(Worker):
    """
    Worker which activates a node in the conceptnetwork
    """

    def __init__(self, target_node, activation_to_add):
        """
        It is urgent to activate nodes.
        Thus, worker's urgency is set to 100 (maximum)
        """
        super(ActivateWorker, self).__init__(ACTIVATE_URGENCY)
        self.target_node = target_node
        self.activation_to_add = activation_to_add


    def run(self, context):
        """
        The Activate worker generates new Compute workers for every linked node
        It pushes a writeConcept worker if the node is activated enough
        """
        self.target_node.activation += self.activation_to_add
        if self.target_node.activation > ACTIVATION_ENABLING_CONCEPT_INSTANTIATION:
            context.workers.pushRandom(WriteConceptWorker(self.target_node))
        for n in self.target_node.linksOut.keys():
            context.workers.pushRandom(ComputeWorker(n))


    def __str__(self):
        return "Activation of concept " + self.target_node.name + \
            " by " + self.activation_to_add
