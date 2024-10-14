"""
Skeleton for COMP3506/7505 A2, S2, 2024
The University of Queensland
Joel Mackenzie and Vladimir Morozov

NOTE: This file will not be used for marking and is here to provide you with
a simple way of testing your data structures. You may edit this file by adding
your own test functionality.
"""

import argparse
import curses
import random

# Import helper libraries
import sys
import time

# Import our pathfinding algorithms and other data types we need
from algorithms.pathfinding import bfs_traversal, dijkstra_traversal, dfs_traversal
from structures.graph import Graph, LatticeGraph
from structures.dynamic_array import DynamicArray

# Configuration: The time (in seconds) to sleep between moves in the viz
ADVANCE = 0.01  # 10ms


class MazeDraw:
    """
    This class handles drawing of mazes. It is best that you leave it alone
    or you may break it.
    """

    def __init__(self, graph: LatticeGraph, origin: int, goal: int) -> None:
        """
        Need to prepare the graph for painting. This involves examining
        the graph to see where the walls are, and etc.
        """
        self._graph = graph
        self._origin_id = origin
        self._goal_id = goal
        self._paint_matrix = None
        self._screen = None
        self._id_to_coord = dict()
        self._rows, self._cols = graph.get_dimensions()

        # OK, let's build a 2d matrix for painting stuff.
        paint_grid = [["%"] * (self._cols) for _ in range(self._rows)]

        # Now we annotate the grid by mapping each node to the grid.
        # By definition, if our input is correct, adjacent nodes will be
        # connected, so we need not evaluate the edges, we can manage them
        # implicitly.
        for node in graph._nodes:
            data = node.get_id()
            self._id_to_coord[data] = node.get_coordinates()
            x, y = node.get_coordinates()
            # Paint the origin as an 'O' character
            if node.get_id() == self._origin_id:
                paint_grid[x][y] = "O"
            # Paint the goal as a 'G' character
            elif node.get_id() == self._goal_id:
                paint_grid[x][y] = "G"
            # Otherwise, we have a path, so leave it clear
            else:
                paint_grid[x][y] = " "

        self._paint_matrix = paint_grid

        # Initialize Curses for the painting
        stdscr = curses.initscr()
        screen_rows, screen_cols = stdscr.getmaxyx()
        if screen_rows < self._rows or screen_cols < self._cols:
            print(
                f"Your console window is too small to display the maze. \
                 Please, resize it to at least {self._rows} rows and {self._cols} columns."
            )
            self.bail_out()

        curses.start_color()
        curses.use_default_colors()
        curses.noecho()
        curses.curs_set(0)
        screen = curses.initscr()
        screen.nodelay(1)
        screen.keypad(1)
        screen.clear()
        self._screen = screen

        # Paint the maze now in its default state (before pathfinding)
        self.init_screen()

    def init_screen(self) -> None:
        """
        Paint the maze state before any paths are consumed
        """
        curses.init_pair(1, curses.COLOR_BLACK, curses.COLOR_WHITE)
        curses.init_pair(2, curses.COLOR_RED, curses.COLOR_BLUE)

        # Walk the cells and paint accordingly
        for i in range(self._rows):
            for j in range(self._cols):
                # Wall cell
                if self._paint_matrix[i][j] == "%":
                    self._screen.addstr(i, j, " ", curses.color_pair(1))
                # Goal cell
                elif self._paint_matrix[i][j] == "G":
                    self._screen.addstr(i, j, "G", curses.color_pair(2))
                # Starting cell
                elif self._paint_matrix[i][j] == "O":
                    self._screen.addstr(i, j, "O", curses.color_pair(2) | curses.A_REVERSE)
                # Valid Path
                else:
                    self._screen.addstr(i, j, " ", curses.color_pair(1) | curses.A_REVERSE)
        # Update the screen
        self._screen.refresh()

    def bail_out(self) -> None:
        """
        The user wants to quit. Let's do it...
        """
        curses.endwin()
        sys.exit(0)

    def draw_visited(self, visited: DynamicArray) -> None:
        """
        Given the visited nodes in order, paint the graph to show how
        they were visited.
        """
        curses.init_pair(3, curses.COLOR_GREEN, curses.COLOR_YELLOW)
        for i in range(visited.get_size()):
            node_id = visited[i]
            (x, y) = self._id_to_coord[node_id]
            if node_id == self._origin_id:
                self._screen.addstr(x, y, "O", curses.color_pair(3))
            elif node_id == self._goal_id:
                self._screen.addstr(x, y, "G", curses.color_pair(3))
            else:
                self._screen.addstr(x, y, "*", curses.color_pair(3))
            self._screen.refresh()
            event = self._screen.getch()
            if event == ord("q"):
                self.bail_out()
            time.sleep(ADVANCE)

    def draw_path(self, path: DynamicArray) -> None:
        """
        Paint the path from the origin to the goal using a different
        colour than the visited sequence.
        """
        curses.init_pair(4, curses.COLOR_MAGENTA, curses.COLOR_YELLOW)
        for i in range(path.get_size()):
            node_id = path[i]
            (x, y) = self._id_to_coord[node_id]
            if node_id == self._origin_id:
                self._screen.addstr(x, y, "O", curses.color_pair(4))
            elif node_id == self._goal_id:
                self._screen.addstr(x, y, "G", curses.color_pair(4))
            else:
                self._screen.addstr(x, y, "$", curses.color_pair(4))
            self._screen.refresh()
            event = self._screen.getch()
            if event == ord("q"):
                self.bail_out()
            time.sleep(ADVANCE)

    def run_viz(self, path: DynamicArray, visited: DynamicArray) -> None:
        """
        Now, given the visited/path, we can run our animation.
        """
        maze.init_screen()
        maze.draw_visited(visited)
        maze.draw_path(path)
        state = 0
        time.sleep(0.5)

        # Infinitely loop until the user presses 'q' to quit
        while state == 0:
            time.sleep(ADVANCE)
            event = maze._screen.getch()
            if event == ord("q"):
                state = 1
        maze._screen.clear()
        maze._screen.keypad(0)
        maze._screen.nodelay(0)
        curses.echo()
        curses.endwin()


# The actual program we're running here
if __name__ == "__main__":
    # Get and parse the command line arguments
    parser = argparse.ArgumentParser(description="COMP3506/7505 Assignment Two: Visual Pathfinding")

    parser.add_argument("--graph", type=str, required=True, help="Path to input graph file")
    parser.add_argument("--bfs", action="store_true", help="Run breadth-first search")
    parser.add_argument("--dfs", action="store_true", help="Run depth-first search")
    parser.add_argument("--dijkstra", action="store_true", help="Run Dijkstra")
    parser.add_argument(
        "--viz",
        action="store_true",
        help="Visualize the algorithm? Requires a LatticeGraph (a 2D graph). Press 'q' to quit the viz at any time. You may need to run `reset` on your terminal after if things go wrong.",
    )
    parser.add_argument("--seed", type=int, required=True, help="Seed the PRNG")

    args = parser.parse_args()

    # No arguments passed
    if len(sys.argv) == 1:
        parser.print_help()
        sys.exit(-1)

    # Seed the PRNG: This will be used to generate two random nodes in the
    # graph to represent the origin/goal nodes
    random.seed(args.seed)

    # Check that we're not trying to do more than one algorithm at a time...
    exclusion = sum([args.dfs, args.bfs, args.dijkstra])
    if exclusion != 1:
        print(
            "Error: Program expects one type of traversal. Please \
        try again with one of {--dfs, --bfs, --dijkstra} only."
        )
        sys.exit(-1)

    # Visualize the output
    if args.viz:
        # Double check we have a lattice graph!
        my_graph = LatticeGraph()
        my_graph.from_file(args.graph)
        origin = my_graph.generate_random_node_id()
        goal = my_graph.generate_random_node_id()
        maze = MazeDraw(my_graph, origin, goal)

        path, visited = None, None
        if args.bfs:
            path, visited = bfs_traversal(my_graph, origin, goal)
        elif args.dfs:
            path, visited = dfs_traversal(my_graph, origin, goal)
        elif args.dijkstra:
            path, visited = dijkstra_traversal(my_graph, origin, goal)

        # Run the viz!
        maze.run_viz(path, visited)

    # No viz desired; just output the path and visited
    # You may wish to add your own tests and etc.
    else:
        my_graph = None
        # Absolutely terrible
        try:
            my_graph = LatticeGraph()
            my_graph.from_file(args.graph)

        except Exception:
            my_graph = None
            try:
                my_graph = Graph()
                my_graph.from_file(args.graph)
            except Exception:
                my_graph = None
                pass

        # Bail out if we couldn't read the graph
        if my_graph is None:
            print("Could not read graph. Exiting...")
            sys.exit(-1)

        # Create start/end points
        origin = my_graph.generate_random_node_id()
        goal = my_graph.generate_random_node_id()

        path, visited = None, None

        # Now check/run the selected algorithm
        if args.bfs:
            path, visited = bfs_traversal(my_graph, origin, goal)
        elif args.dfs:
            path, visited = dfs_traversal(my_graph, origin, goal)
        elif args.dijkstra:
            path, visited = dijkstra_traversal(my_graph, origin, goal)

        print("===Traversal Complete===")
        print("Origin: ", str(origin))
        print("Goal: ", str(goal))
        print("Path: ", str(path))
        print("Visited: ", str(visited))
