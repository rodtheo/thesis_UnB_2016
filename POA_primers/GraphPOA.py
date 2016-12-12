
class Node(object):
    def __init__(self, name):
        self.name = str(name)
    def getName(self):
        return self.name
    def __str__(self):
        return self.name
    def __repr__(self):
        return self.name
    def __eq__(self, other):
        return self.name == other.name
    def __ne__(self, other):
        return not self.__eq__(other)
    def __hash__(self):
        # Override the default hash method
        # Think: Why would we want to do this?
        return self.name.__hash__()

class Edge(object):
    def __init__(self, src, dest):
        self.src = src
        self.dest = dest
    def getSource(self):
        return self.src
    def getDestination(self):
        return self.dest
    def __str__(self):
        return '{0}->{1}'.format(self.src, self.dest)

class Digraph(object):
    """
    A directed graph
    """
    def __init__(self):
        # A Python Set is basically a list that doesn't allow duplicates.
        # Entries into a set must be hashable (where have we seen this before?)
        # Because it is backed by a hashtable, lookups are O(1) as opposed to the O(n) of a list (nifty!)
        # See http://docs.python.org/2/library/stdtypes.html#set-types-set-frozenset
        self.seq = {}
        self.nodes = set([])
        self.edges = {}
        self.idx = {}
    def addNode(self, node, label, index):
        self.label = str(label)
        self.index = index
        if node in self.nodes:
            # Even though self.nodes is a Set, we want to do this to make sure we
            # don't add a duplicate entry for the same node in the self.edges list.
            raise ValueError('Duplicate node')
        else:
            self.idx[node] = self.index
            self.seq[node] = self.label
            self.nodes.add(node)
            self.edges[node] = []
    def addEdge(self, edge):
        src = edge.getSource()
        dest = edge.getDestination()
        if not(src in self.nodes and dest in self.nodes):
            raise ValueError('Node not in graph')
        self.edges[src].append(dest)
    def getLabelNode(self,node):
        return self.seq[node]
    def childrenOf(self, node):
        return self.edges[node]
    def hasNode(self, node):
        return node in self.nodes
    def __str__(self):
        res = ''
        for k in self.edges:
            for d in self.edges[str(k)]:
                res = '{0}{1}->{2}\n'.format(res, k, d)
        return res[:-1]

class WeightedEdge(Edge):
    def __init__(self, src, dest, weight1):
        Edge.__init__(self, src, dest)
        self.total_score = float(weight1)
    
    def getTotalScore(self):
        return self.total_score
    
    def __str__(self):
        return  Edge.__str__(self) + " (" + str(self.total_score) + ")"
    def __repr__(self):
        return '{0}'.format(self.total_score)

class WeightedDigraph(Digraph):
    def __init__(self):
        Digraph.__init__(self)
        self.edges = {}

    def addEdge(self,edge):
        src = edge.getSource()
        dest = edge.getDestination()
        weights = (edge.getTotalScore(),0)
        if not (src in self.nodes and dest in self.nodes):
            raise ValueError("Node not in graph")
        self.edges[src].append([dest,weights])

    def childrenOf(self, node):
        return [child for child,_ in self.edges[node]]
    
    def __str__(self):
        res = ''
        for k in self.edges:
            for out in self.edges[Node(k)]:
                dest = out[0]
                d = out[1][0]
                res = '{0}{1}->{2} ({3})\n'.format(res, k, dest, int(d))
        return res[:-1]

