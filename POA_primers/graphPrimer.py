import string
# This imports everything from `graph.py` as if it was defined in this file!
from GraphPOA import *
from POA import *
import sys
import yaml

def load_poa(poaFilename):
    print "Parsing POA alignment from {0} to weighted digraph structure:".format(poaFilename)
    poa_g = WeightedDigraph()
    i=0
    idx = 0
    print "Adding node.."
    for po in POAReader(poaFilename):
        label = po.getName()
        Aindex = po.getAindex()
        fromNodes = po.getfromNodes()
        w = po.gettoNodes()
        print "..",i,"WITH NUCLEOTIDE",label,"LEN",str(idx)
        node = Node(i)
        try:
            poa_g.addNode(node,label,idx)
        except:
            print "WARNING: NODE",i,"ALREADY ADD WITH NUCLEOTIDE",label
            pass
        if '0' in w:
            idx+=1
        i+=1
    print "Conecting edges.."
    n=0
    for poa in POAReader(poaFilename):
        label = poa.getName()
        Aindex = poa.getAindex()
        fromNodes = poa.getfromNodes()
        w = poa.gettoNodes()
        if fromNodes == []: # if the node hasn't any parental
            pass
        elif Aindex != []: # if node is part of a ring (SNP in this graph position)
            for x in Aindex:
                node1=Node(x)
                poa_g.addEdge(WeightedEdge(Node(fromNodes[0]),node1,len(w)))
                # G.add_node(x,label = str(po.getName()))
                # G.add_edge(fromNodes[0], x, weight = len(w))
        else: # if the node is alone, i.e, the seq doesnt have polymorphisms in this position
            node1=Node(n)
            for parental in fromNodes:
                print "NODE",parental,"TO",n
                parentalNode = Node(parental)
                poa_g.addEdge(WeightedEdge(Node(parental), Node(n), len(w)))
                # G.add_edge(parental,i,weight = len(w))
        n+=1
    print "LENGTH OF GRAPH IS",len(poa_g.nodes)
    print "Graph construction finished."
    return poa_g

#
# State the optimization problem as a function to minimize
# and what the constraints are
#

def bruteForceSearch(digraph, start, end, minTotalDist, maxDistOutdoors, N):
    """
    Finds the best segment path from a pairwise alignment that contains at least N mismatches using Brute-force algorithm.
    The best segment would be the one that contains less mismatches. To performe the walk through the graph and compute the
    best segment we consider as score the number of matches in each position of a sequence.

    The total distance travelled on the path must not exceed maxTotalDist, and
    the distance spent outdoor on this path must not exceed maxDistOutdoors.

    Parameters: 
        digraph: instance of class Digraph or its subclass
        start, end: start & end building numbers (strings) - dont deal with mismatches in start position
        maxTotalDist : maximum total distance on a path (integer)
        maxDistOutdoors: maximum distance spent outdoors on a path (integer)

    Assumes:
        start and end are numbers for existing buildings in graph

    Returns:
        The best-path (longest path without mismatches) from start to end, represented by 
        a list of building numbers (in strings), [n_1, n_2, ..., n_k], 
        where there exists an edge from n_i to n_(i+1) in digraph, 
        for all 1 <= i < k.

        If there exists no path that satisfies maxTotalDist and
        maxDistOutdoors constraints, then raises a ValueError.
    """
    def dfs(graph, start_node, end_node, N, path=[], valid_paths=[], visited_nodes=[]):
        path = path + [start_node]
        visited_nodes.append(start_node)
        if start_node == end_node:
            valid_paths.append(path[1:])
            return valid_paths
        for edge in graph.edges[start_node]:
            node = edge[0]
            # print start_node,edge
            if edge[1][0] >= int(N) and len(graph.edges[start_node]) == 1:
                # print str(node), str(start_node)
                if node not in path and node not in visited_nodes: # avoid cycle
                    valid_paths = dfs(graph, node, end_node, N, path, valid_paths, visited_nodes)
            else:
                if path not in valid_paths:
                    valid_paths.append(path[1:])
                valid_paths = dfs(graph, node, end_node,N, [], valid_paths, visited_nodes)
        return valid_paths

    def lookup_edge(graph, source, destination):
        edges = graph.edges[source]
        for edge in edges:
            if edge[0] == destination:
                return edge
        raise ValueError('EPA')
    def start_node_single(graph, start_node):
        edges = graph.edges[start_node]
        last_edge = 0
        for edge in edges:
            if len(graph.edges[edge[0]]) != 1:
                if int(edge) > last_edge:
                    last_edge = int(edge)
                
            else:
                return [start_node]
        return [range(last_edge)]


    ## REALIZAR MUDANCAS PARA CONSIDERAR O CASO EM QUE A PRIMEIRA BASE FAZ PARTE DE UM ANEL. OU SEJA, NA QUAL ELA EH POLIMORFICA.
    ## DEVE-SE CONSIDERAR, NESTE CASO, TODOS OS NOS COMO PONTO INICIAL

    valid_paths = dfs(digraph, Node(start), Node(end), N)

    path_results = {}
    shortest_path = None
    longest_path_dist = minTotalDist + 1
    # print valid_paths
    for p in range(len(valid_paths)):
        path = valid_paths[p]
        total_dist = 0
        outdoor_dist = 0
        for i in range(len(path) - 1):
            edge = lookup_edge(digraph, path[i], path[i+1])
            total_dist += edge[1][0]
        if total_dist >= minTotalDist:
            if total_dist > longest_path_dist:
                shortest_path = p
                longest_path_dist = total_dist
            path_results[p] = (total_dist)
    if shortest_path is None:
        raise ValueError('longest is none')
    else:
        seqfinal = ''
        clear_path = []
        include_region = []
        for e in valid_paths[shortest_path]:
            include_region.append(int(str(e)))
            seqfinal = seqfinal + digraph.seq[e]
            clear_path.append((str(e),path_results[shortest_path]))
        return (clear_path,seqfinal,[min(include_region),max(include_region)])


def primerForwardGenomicPos(position,point,lengthExtend):
    return int(point) - (lengthExtend - int(position))

def primerReverseGenomicPos(position,point,lengthExtend):
    return int(point) - (lengthExtend - int(position))

def _pass_parse(POAReaderObj):
    for po in POAReaderObj:
        pass
    return True

if __name__ == '__main__':
#     Test cases
    lengthExtend = int(sys.argv[4])
    final_primers = {}
    filenameforward = sys.argv[1]
    poaforward = load_poa(filenameforward)
    headerpoaforward = POAReader(filenameforward)
    if _pass_parse(headerpoaforward):
        samplesforward = headerpoaforward.get_samples()
        pointforward = headerpoaforward.get_point()
    # print samplesforward,pointforward
    # print isinstance(poa, Digraph)
    # print isinstance(poa, WeightedDigraph)
    # print 'nodes', poa.nodes
    # print 'edges', poa.edges[Node(93)]
    brutePathforward,sequenceforward,idxRangeforward = bruteForceSearch(poaforward, '4', str(len(poaforward.edges)-1), 1, 1, len(samplesforward))
    # print brutePathforward
    # print sequenceforward
    # print idxRangeforward
    pseudobegin = poaforward.idx[Node(idxRangeforward[0])]
    pseudoend = poaforward.idx[Node(idxRangeforward[1])]
    print pseudobegin, pseudoend

    filenamereverse = sys.argv[2]
    poareverse = load_poa(filenamereverse)
    headerpoareverse = POAReader(filenamereverse)
    if _pass_parse(headerpoareverse):
        samplesreverse = headerpoareverse.get_samples()
        pointreverse = headerpoareverse.get_point()
    # print samplesreverse,pointreverse
    # print isinstance(poa, Digraph)
    # print isinstance(poa, WeightedDigraph)
    # print 'nodes', poa.nodes
    # print 'edges', poa.edges[Node(93)]
    brutePathreverse,sequencereverse,idxRangereverse = bruteForceSearch(poareverse, '4', str(len(poareverse.edges)-1), 1, 1, len(samplesreverse))
    # print brutePathreverse
    # print sequencereverse
    # print idxRangereverse
    pseudobegin = poareverse.idx[Node(idxRangereverse[0])]
    pseudoend = poareverse.idx[Node(idxRangereverse[1])]
    print pseudobegin, pseudoend
    final_primers['forward']={'begingraph':pseudobegin,'begin':primerForwardGenomicPos(pseudobegin, pointforward, lengthExtend),'endgraph':pseudoend,'end':primerForwardGenomicPos(pseudoend, pointforward,lengthExtend), 'samples':samplesforward, 'extendingbp':str(lengthExtend)}
    final_primers['reverse']={'begingraph':pseudobegin,'begin':primerReverseGenomicPos(pseudobegin, pointreverse,lengthExtend),'endgraph':pseudoend,'end':primerReverseGenomicPos(pseudoend, pointreverse,lengthExtend), 'samples':samplesreverse, 'extendingbp':str(lengthExtend)}
    print "FORWARD PRIMER PERMITED POSITIONS",primerForwardGenomicPos(pseudobegin, pointforward,lengthExtend),primerForwardGenomicPos(pseudoend, pointforward,lengthExtend),"EXTENDING -", str(lengthExtend),"bp FROM INITIAL POSITION"
    print "reverse PRIMER PERMITED POSITIONS",primerReverseGenomicPos(pseudobegin, pointreverse,lengthExtend),primerReverseGenomicPos(pseudoend, pointreverse,lengthExtend),"EXTENDING +",str(lengthExtend),"bp FROM INITIAL PRIMER POSITION"
    print "Dumping YAML.."
    print yaml.dump(final_primers)
    with open(sys.argv[3],'w') as outfile:
        outfile.write(yaml.dump(final_primers,default_flow_style = True))
