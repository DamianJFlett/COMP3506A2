"""
Skeleton for COMP3506/7505 A2, S2, 2024
The University of Queensland
Joel Mackenzie and Vladimir Morozov

You may wish to import your data structures to help you with some of the
problems. Or maybe not. We did it for you just in case.
"""
from structures.entry import Entry
from structures.dynamic_array import DynamicArray
from structures.graph import Graph, LatticeGraph
from structures.map import Map
from structures.pqueue import PriorityQueue
from structures.bloom_filter import BloomFilter
from structures.util import Hashable


def bfs_traversal(
    graph: Graph | LatticeGraph, origin: int, goal: int
    ) -> tuple[DynamicArray, DynamicArray]:
    """
    Task 2.1: Breadth First Search

    @param: graph
      The general graph or lattice graph to process
    @param: origin
      The ID of the node from which to start traversal
    @param: goal
      The ID of the target node

    @returns: tuple[DynamicArray, DynamicArray]
      1. The ordered path between the origin and the goal in node IDs
      (or an empty DynamicArray if no path exists);
      2. The IDs of all nodes in the order they were visited.
    """
    # Stores the keys of the nodes in the order they were visited
    visited_order = DynamicArray()
    # Stores the path from the origin to the goal
    path = DynamicArray()
    pred = Map()
    seen = Map()  # glorified set of keys
    # ALGO GOES HERE
    queue = PriorityQueue()
    queue.insert_fifo(origin)
    pred[origin] = "Root"
    while not queue.is_empty():
        removed = queue.remove_min()
        if not seen.find(removed):
            visited_order.append(removed)
            seen[removed] = "junk"
        if removed == goal:
            cur = goal
            while pred[cur] != "Root":
                path.prepend(cur)
                cur = pred[cur]
            path.prepend(origin)
            break
        for node in graph.get_neighbours(removed):
            neighbour = node.get_id()
            if not pred.find(neighbour):
                pred[neighbour] = removed
                queue.insert_fifo(neighbour)
    
    # Return the path and the visited nodes list
    return (path, visited_order)


def dijkstra_traversal(graph: Graph, origin: int) -> DynamicArray:
    """
    Task 2.2: Dijkstra Traversal

    @param: graph
      The *weighted* graph to process (POSW graphs)
    @param: origin
      The ID of the node from which to start traversal.

    @returns: DynamicArray containing Entry types.
      The Entry key is a node identifier, Entry value is the cost of the
      shortest path to this node from the origin.

    NOTE: Dijkstra does not work (by default) on LatticeGraph types.
    This is because there is no inherent weight on an edge of these
    graphs. It should of course work where edge weights are uniform.
    """
def dijkstra_traversal(graph: Graph, origin: int) -> DynamicArray:
    """
    Task 2.2: Dijkstra Traversal

    @param: graph
      The *weighted* graph to process (POSW graphs)
    @param: origin
      The ID of the node from which to start traversal.

    @returns: DynamicArray containing Entry types.
      The Entry key is a node identifier, Entry value is the cost of the
      shortest path to this node from the origin.

    NOTE: Dijkstra does not work (by default) on LatticeGraph types.
    This is because there is no inherent weight on an edge of these
    graphs. It should of course work where edge weights are uniform.
    """

    #  I'm sure like 50% of this is redundant but it passes the tests and i'm not spending another second of my life on this
    queue = PriorityQueue()
    valid_locations = DynamicArray()  # This holds your answers
    distances = _inf_map(graph, origin)
    seen = Map()
    distances[origin] = 0
    queue.insert(0, origin)
    seen[origin] = 1
    while not queue.is_empty():
        removed_weight = queue.get_min_priority()
        removed = queue.remove_min()
        if not seen.find(removed):
            valid_locations.append(Entry(removed, distances[removed]))
        seen[removed] = "junk"
        for node, weight in graph.get_neighbours(removed):
            node_id = node.get_id()
            if not seen.find(node_id):
                new_dist = weight + removed_weight
                if new_dist < distances[node_id]:
                    distances[node_id] = new_dist
                    queue.insert(new_dist, node_id)
    # Return the DynamicArray containing Entry types
    return valid_locations

def _inf_map(graph, origin):
    """
    Horror code copying to iterate through and get all the nodes, outputting a map where all of them are mapped to inf
    """
    # Stores the keys of the nodes in the order they were visited
    # Stores the path from the origin to the goal
    pred = Map()
    seen = Map()  # glorified set of keys
    inf_map = Map()
    # ALGO GOES HERE
    queue = PriorityQueue()
    queue.insert_fifo(origin)
    pred[origin] = "Root"
    while not queue.is_empty():
        removed = queue.remove_min()
        if not seen.find(removed):
            inf_map[removed] = float("inf")
            seen[removed] = "junk"
        for node, weight in graph.get_neighbours(removed):
            neighbour = node.get_id()
            if not pred.find(neighbour):
                pred[neighbour] = removed
                queue.insert_fifo(neighbour)
    
    # Return the path and the visited nodes list
    return inf_map 

def dfs_traversal(
    graph: Graph | LatticeGraph, origin: int, goal: int
    ) -> tuple[DynamicArray, DynamicArray]: 
    """
    Task 2.3: Depth First Search **** COMP7505 ONLY ****
    COMP3506 students can do this for funsies.

    @param: graph
      The general graph or lattice graph to process
    @param: origin
      The ID of the node from which to start traversal
    @param: goal
      The ID of the target node

    @returns: tuple[DynamicArray, DynamicArray]
      1. The ordered path between the origin and the goal in node IDs
      (or an empty DynamicArray if no path exists);
      2. The IDs of all nodes in the order they were visited.
    
    """
    # Stores the keys of the nodes in the order they were visited
    visited_order = DynamicArray()
    # Stores the path from the origin to the goal
    path = DynamicArray()

    # ALGO GOES HERE

    # Return the path and the visited nodes list
    return (path, visited_order)



