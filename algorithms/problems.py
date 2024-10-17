"""
Skeleton for COMP3506/7505 A2, S2, 2024
The University of Queensland
Joel Mackenzie and Vladimir Morozov

 Each problem will be assessed on three sets of tests:

1. "It works":
       Basic inputs and outputs, including the ones peovided as examples, with generous time and memory restrictions.
       Large inputs will not be tested here.
       The most straightforward approach will likely fit into these restrictions.

2. "Exhaustive":
       Extensive testing on a wide range of inputs and outputs with tight time and memory restrictions.
       These tests won't accept brute force solutions, you'll have to apply some algorithms and optimisations.

 3. "Welcome to COMP3506":
       Extensive testing with the tightest possible time and memory restrictions
       leaving no room for redundant operations.
       Every possible corner case will be assessed here as well.

There will be hidden tests in each category that will be published only after the assignment deadline.

You may wish to import your data structures to help you with some of the
problems. Or maybe not. We did it for you just in case.
"""
from structures.entry import Entry, Compound, Offer
from structures.dynamic_array import DynamicArray
from structures.linked_list import DoublyLinkedList, DLLNode
from structures.bit_vector import BitVector
from structures.graph import Graph
from structures.map import Map
from structures.pqueue import PriorityQueue
from structures.bloom_filter import BloomFilter
from math import sqrt


def maybe_maybe_maybe(database: list[str], query: list[str]) -> list[str]:
    """
    Task 3.1: Maybe Maybe Maybe

    @database@ is an array of k-mers in our database.
    @query@ is an array of k-mers we want to search for.

    Return a list of query k-mers that are *likely* to appear in the database.

    Limitations:
        "It works":
            @database@ contains up to 1000 elements;
            @query@ contains up to 1000 elements.

        "Exhaustive":
            @database@ contains up to 100'000 elements;
            @query@ contains up to 100'000 elements.

        "Welcome to COMP3506":
            @database@ contains up to 1'000'000 elements;
            @query@ contains up to 500'000 elements.

    Each test will run over three false positive rates. These rates are:
        fp_rate = 10%
        fp_rate = 5%
        fp_rate = 1%.

    You must pass each test in the given time limit and be under the given
    fp_rate to get the associated mark for that test.
    """
    answer = []
    bf = BloomFilter(len(database)*2)
    for kmer in database:
        bf.insert(kmer)
    for kmer in query:
        if bf.contains(kmer):
            answer.append(kmer)
    return answer


def dora(graph: Graph, start: int, symbol_sequence: str,
         ) -> tuple[BitVector, list[Entry]]:
    """
    Task 3.2: Dora and the Chin Bicken

    @graph@ is the input graph G; G might be disconnected; each node contains
    a single symbol in the node's data field.
    @start@ is the integer identifier of the start vertex.
    @symbol_sequence@ is the input sequence of symbols, L, with length n.
    All symbols are guaranteed to be found in G. 

    Return a BitVector encoding symbol_sequence via a minimum redundancy code.
    The BitVector should be read from index 0 upwards (so, the first symbol is
    encoded from index 0). You also need to return your codebook as a
    Python list of unique Entries. The Entry key should correspond to the
    symbol, and the value should be a string. More information below.

    Limitations:
        "It works":
            @graph@ has up to 1000 vertices and up to 1000 edges.
            the alphabet consists of up to 26 characters.
            @symbol_sequence@ has up to 1000 characters.

        "Exhaustive":
            @graph@ has up to 100'000 vertices and up to 100'000 edges.
            the alphabet consists of up to 1000 characters.
            @symbol_sequence@ has up to 100'000 characters.

        "Welcome to COMP3506":
            @graph@ has up to 1'000'000 vertices and up to 1'000'000 edges.
            the alphabet consists of up to 300'000 characters.
            @symbol_sequence@ has up to 1'000'000 characters.

    """
    coded_sequence = BitVector()
    """
    list of Entry objects, each entry has key=symbol, value=str. The str
    value is just an ASCII representation of the bits used to encode the
    given key. For example: x = Entry("c", "1101")
    """
    codebook = []

    # DO THE THING
    visited_order = DynamicArray()
    # Stores the path from the origin to the goal
    pred = Map()
    seen = Map()  # glorified set of keys
    freqs = Map()
    # ALGO GOES HERE
    # I LOVE COPYING MY CODE INSTEAD OF ABSTRACTING I DO IT EVERY DAY
    queue = DoublyLinkedList()
    queue.insert_to_back(Entry(start, graph.get_node(start).get_data()))
    pred[start] = "Root"
    while queue.get_size():
        temp = queue.remove_from_front()
        removed = temp.get_key()
        data = temp.get_value()
        if not seen.find(removed):
            if not freqs[data]:
                visited_order.append(data)
                freqs[data] = 0
            freqs[data] += 1
            seen[removed] = "junk"
        for node in graph.get_neighbours(removed):
            neighbour = node.get_id()
            if not pred.find(neighbour):
                pred[neighbour] = removed
                queue.insert_to_back(Entry(neighbour, node.get_data()))
    PQ = PriorityQueue()
    i = 0
    for i in range(visited_order.get_size()):
        x = visited_order[i]
        PQ.insert(freqs[x], DLLNode(x))
    while PQ.get_size() > 1:
        f1 = PQ.get_min_priority()
        t1 = PQ.remove_min()
        f2 = PQ.get_min_priority()
        t2 = PQ.remove_min()
        t = DLLNode(f1+f2)
        t.set_prev(t1)
        t.set_next(t2)
        PQ.insert(f1+f2, t) 
    f = PQ.get_min_priority()
    T = PQ.remove_min()

    #  Traverse T
    codes = Map()
    stack = DoublyLinkedList()
    seen = DynamicArray()
    stack.insert_to_back(Entry(T, ""))
    while stack.get_size() > 0:
        temp = stack.remove_from_back()
        cur = temp.get_key()
        code = temp.get_value()
        if (not cur.get_next()) and (not cur.get_prev()):
            codes[cur.get_data()] = code
            seen.append(cur.get_data())
        else:
            if cur.get_next():
                stack.insert_to_back(Entry(cur.get_next(), code + "1"))
            if cur.get_prev():
                stack.insert_to_back(Entry(cur.get_prev(), code + "0"))
    i = 0
    for i in range(visited_order.get_size()):
        codebook.append(Entry(seen[i], codes[seen[i]]))
    for char in symbol_sequence:
        for bit in codes[char]:
            coded_sequence.append(int(bit))

    return (coded_sequence, codebook)


def chain_reaction(compounds: list[Compound]) -> int:
    """
    Task 3.3: Chain Reaction

    @compounds@ is a list of Compound types, see structures/entry.py for the
    definition of a Compound. In short, a Compound has an integer x and y
    coordinate, a floating point radius, and a unique integer representing
    the compound identifier.

    Return the compound identifier of the compound that will yield the
    maximal number of compounds in the chain reaction if set off. If there
    are ties, return the one with the smallest identifier.

    Limitations:
        "It works":
            @compounds@ has up to 100 elements

        "Exhaustive":
            @compounds@ has up to 1000 elements

        "Welcome to COMP3506":
            @compounds@ has up to 10'000 elements

    """
    # the problem is that ids needn't be in orer
    maximal_compound = -1
    current_max = -1
    # DO THE THING
    reacted_with = Map() # store ids directly reacted with 
    for compound1 in compounds:
        for compound2 in compounds:
            if not reacted_with.find(compound1.get_compound_id()):
                reacted_with[compound1.get_compound_id()] = DynamicArray()
            if _in_rad(compound1, compound2):
                reacted_with[compound1.get_compound_id()].append(
                    compound2.get_compound_id())
    # ALGO GOES HERE
    queue = PriorityQueue()
    for i in range(len(compounds) ):
        queue = PriorityQueue() # redoing fucking bfs code copying my beloved
        pred = BitVector()
        seen = BitVector()  # glorified set of keys
        pred.allocate(len(compounds))
        seen.allocate(len(compounds))
        num_reac = 0
        queue.insert_fifo(i)
        pred[i] = 1
        while not queue.is_empty():
            removed = queue.remove_min()
            if not seen[removed]:
                num_reac += 1
                seen[removed] = 1
            for j in range(reacted_with[removed].get_size()):
                node = reacted_with[removed][j]
                if not pred[node]:
                    pred[node] = 1
                    queue.insert_fifo(node)
        if num_reac > current_max:
            current_max = num_reac
            maximal_compound = i
    return maximal_compound


def _in_rad(c1: Compound, c2: Compound):
    if sqrt((c1.get_coordinates()[0]-c2.get_coordinates()[0])**2+(c1.get_coordinates()[1]-c2.get_coordinates()[1])**2) <= c1.get_radius():
        return True
    else:
        return False


def labyrinth(offers: list[Offer]) -> tuple[int, int]:
    """
    Task 3.4: Labyrinth

    @offers@ is a list of Offer types, see structures/entry.py for the
    definition of an Offer. In short, an Offer stores n (number of nodes),
    m (number of edges), and k (diameter) of the given Labyrinth. Each
    Offer also has an associated cost, and a unique offer identifier.
    
    Return the offer identifier and the associated cost for the cheapest
    labyrinth that can be constructed from the list of offers. If there
    are ties, return the one with the smallest identifier. 
    You are guaranteed that all offer ids are distinct.

    Limitations:
        "It works":
            @offers@ contains up to 1000 items.
            0 <= n <= 1000
            0 <= m <= 1000
            0 <= k <= 1000

        "Exhaustive":
            @offers@ contains up to 100'000 items.
            0 <= n <= 10^6
            0 <= m <= 10^6
            0 <= k <= 10^6

        "Welcome to COMP3506":
            @offers@ contains up to 5'000'000 items.
            0 <= n <= 10^42
            0 <= m <= 10^42
            0 <= k <= 10^42

    """
    best_offer_id = -1
    best_offer_cost = float('inf')

    for offer in offers:    
        if is_valid(offer) and offer.get_cost() < best_offer_cost:
            best_offer_id = offer.get_offer_id()
            best_offer_cost = offer.get_cost()

    return (best_offer_id, best_offer_cost)


def is_valid(offer: Offer) -> bool:
    # "is this a graph" checks - if these are somehow superceneded later
    #  can get rid of considering a mapping n, m -> k, 
    #  starting from a tree m=n-1, fixing
    #  n and increasing m, k = n-1, k =n-2, ... k=2 where its
    # fixed until k=1 at a complete graph 
    n = offer.get_n()
    m = offer.get_m()
    k = offer.get_k()
    if m > n*(n-1) // 2:
        return False
    if m < n-1:
        return False
    if m == n*(n-1) // 2 and k < 1:
        return False
    if m == n-1 and k < m:
        return False
    if n-1 < m and k < successive_halves(n,m):
        return False
    return True


def successive_halves(n, m):
    difference = m - n + 1
    m >>= difference
    return max(m, 2)
