import networkx as nx

def returnsConceptIterator(f):
    def wrap(self, *args, **kwargs):
        ret = f(self, *args, **kwargs)
        for c in ret:
            yield Concept(self.network, c)
    return wrap

def returnsArcIterator(f):
    def wrap(self, *args, **kwargs):
        ret = f(self, *args, **kwargs)
        for (i, j, key, data) in ret:
            yield Arc(self.network, i, j, key, data)
    return wrap


class Network:
    def __init__(self):
        self.network = nx.MultiDiGraph()

    def get(self, id):
        return Concept(self.network, id)


class Concept:
    def __init__(self, network, id):
        self.network = network
        self.id = id

    def __getattr__(self, attr):
        return self.network.node[self.id][attr]

    def __setattr__(self, attr, value):
        self.network.node[self.id][attr] = value

    @returnsConceptIterator
    def successors(self):
        return self.network.successors_iter(self.id)

    @returnsConceptIterator
    def predecessors(self):
        return self.network.predecessors_iter(self.id)

    @returnsArcIterator
    def outArcs(self):
        return self.network.out_edges_iter(self.id, data=True, keys=True)

    @returnsArcIterator
    def inArcs(self):
        return self.network.in_edges_iter(self.id, data=True, keys=True)


class Arc:
    def __init__(self, network, fromId, toId, key=0, data=None):
        self.network = network
        self.fromId = fromId
        self.toId = toId
        self.key = key

    def __getattr__(self, attr):
        return self.network[self.fromId][self.toId][self.key][attr]

    def __setattr__(self, attr, value):
        self.network[self.fromId][self.toId][self.key][attr] = value

    def origin(self):
        return Concept(self.network, self.fromId)

    def destination(self):
        return Concept(self.network, self.toId)
