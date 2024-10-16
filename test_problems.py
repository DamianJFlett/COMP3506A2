"""
Skeleton for COMP3506/7505 A1, S2, 2024
The University of Queensland
Joel Mackenzie and Vladimir Morozov

NOTE: This file is not used for assessment. It is just a driver program for
you to write your own test cases and execute them against your data structures.
"""

# Import helper libraries
import random
import sys
import time
import argparse

# Import our structures
from structures.entry import Entry, Compound, Offer
from structures.dynamic_array import DynamicArray
from structures.linked_list import DoublyLinkedList
from structures.bit_vector import BitVector
from structures.graph import Graph, LatticeGraph
from structures.map import Map
from structures.pqueue import PriorityQueue
from structures.bloom_filter import BloomFilter
from structures.util import Hashable
import random
import matplotlib.pyplot as plt

from algorithms.problems import maybe_maybe_maybe, dora, chain_reaction, labyrinth

def test_maybe():
    """
    A simple set of tests for the 3xmaybe problem.
    This is not marked and is just here for you to test your code.
    """
    print ("=== Maybe Maybe Maybe ===")
    # 0. Set some params; you can tweak these later.
    K = 17 # 17-mers
    DB_SIZE = 100000 # 100k DB entries
    Q_SIZE = 1000 # 1000 queries

    # 1. Generate a 'database' with some k-mers
    kmer_db = ["".join(random.choice("ACGT") for _ in range(K)) for i in range(DB_SIZE)]

    # 2. Generate a set of query k-mers. We could generate these randomly, but
    # here we might like to sample from the db to ensure the k-mers we're
    # looking for actually exist; we can test "negative" queries later...
    query_sample = random.sample(kmer_db, Q_SIZE)

    # Now you need to issue the queries. The testing is up to you from here,
    # because there are many ways to solve this problem. However, there are
    # some definite hints on how to solve this in the spec.
    output = maybe_maybe_maybe(kmer_db, query_sample)



def test_dora(graph: Graph):
    """
    A simple set of tests for the Dora problem.
    This is not marked and is just here for you to test your code.
    """
    print ("=== Dora ===")

    print ("Generating a random label for each vertex in G.")
    graph.generate_labels()
    # You may prefer to fix the starting vertex instead of picking a random one
    start = graph.generate_random_node_id()

    # You can now run Dora from start across graph.
    # You will also need to set up a sequence to encode. The sequence should
    # be drawn from the symbols in the reachable component of G from the
    # given start node. Look at Figure 8 in the spec.
    sequence = ""

    codeword, codebook = dora(graph, start, sequence)


def test_chain_reaction():
    """
    A simple set of tests for the Chain Reaction problem.
    This is not marked and is just here for you to test your code.
    """
    print ("=== Chain Reaction ===")

    # Set up some params
    # x dim is 100
    MIN_X = 0
    MAX_X = 100
    # y dim is 100
    MIN_Y = 0
    MAX_Y = 100
    # minimum radius is 1, max is 25
    MIN_R = 1
    MAX_R = 10
    # maximum compound count
    COMPOUNDS = 10

    compounds = []
    locations = set() # ensure we do not duplicate x/y coords
    for cid in range(COMPOUNDS):
        x = random.randint(MIN_X, MAX_X)
        y = random.randint(MIN_Y, MAX_Y)
        r = random.randint(MIN_R, MAX_R)
        xy_key = str(x) + "_" + str(y)
        if xy_key not in locations:
            compounds.append(Compound(x, y, r, cid))
            locations.add(xy_key)
    print ("Generated", len(compounds), "compounds.")
    for compound in compounds:
       print(str(compound))




    # You can now run and test your algorithm
    trigger_compound  = chain_reaction(compounds)
    print("trigger compound is", trigger_compound)
    plt.axis("equal")
    ax = plt.gca()
    ax.set_xlim([MIN_X - MAX_R, MAX_X + MAX_R])
    ax.set_ylim([MIN_Y - MAX_R, MAX_Y + MAX_R])

    for compound in compounds:
        x, y = compound.get_coordinates()
        rand_color = [random.uniform(0.01, 1) for _ in range(3)]
        plt.plot(x, y, 'o', color=rand_color)
        circle = plt.Circle((x, y), radius=compound.get_radius(), color=rand_color, alpha=0.2)
        plt.gca().add_artist(circle)
        ax.annotate(str(compound.get_compound_id()), (x,y))
    plt.show()

def test_labyrinth():
    """
    A simple set of tests for the Labyrinth problem.
    This is not marked and is just here for you to test your code.
    """
    print ("=== Labyrinth ===")

    # Set up some params - you should mess with these
    # nodes, n = |V|
    MIN_N = 2
    MAX_N = 10
    # edges, m = |E|
    MIN_M = 1
    MAX_M = 10
    # Diameter
    MIN_K = 0
    MAX_K = 3
    # Cost
    MIN_C = 1
    MAX_C = 10
    # How many?
    OFFERS = 10

    offers = []
    for oid in range(OFFERS):
        n = random.randint(MIN_N, MAX_N)
        m = random.randint(MIN_M, MAX_M)
        k = random.randint(MIN_K, MAX_K)
        c = random.randint(MIN_C, MAX_C)
        offers.append(Offer(n, m, k, c, oid))

    print ("Generated", len(offers), "offers.")
    for offer in offers:
       print(str(offer))
    # You can now run and test your algorithm
    best_offer, cost = labyrinth(offers)
    print(best_offer, cost, "best")


# The actual program we're running here
if __name__ == "__main__":
    # Get and parse the command line arguments
    parser = argparse.ArgumentParser(description="COMP3506/7505 Assignment Two: Testing Problems")

    parser.add_argument("--maybe", action="store_true", help="Test your Maybex3 solution.")
    parser.add_argument("--dora", type=str, help="Test your Dora solution.")
    parser.add_argument("--chain", action="store_true", help="Test your Chain Reaction solution.")
    parser.add_argument("--labyrinth", action="store_true", help="Test your Labyrinth solution.")
    parser.add_argument("--seed", type=int, default='42', help="Seed the PRNG.")
    args = parser.parse_args()

    # No arguments passed
    if len(sys.argv) == 1:
        parser.print_help()
        sys.exit(-1)

    # Seed the PRNG in case you are using randomness
    random.seed(args.seed)

    # Now check/run the selected algorithm
    if args.maybe:
        test_maybe()

    if args.dora:
        in_graph = Graph()
        in_graph.from_file(args.dora)
        test_dora(in_graph)

    if args.chain:
        test_chain_reaction()

    if args.labyrinth:
        test_labyrinth()

