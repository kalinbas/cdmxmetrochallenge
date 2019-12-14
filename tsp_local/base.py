from abc import ABCMeta, abstractmethod

class TSP():
    """
    Class to hold a TSP, sub-class will implement different improvement
    heuristics.
    """
    __metaclass__ = ABCMeta

    edges = {}  # Global cost matrix
    ratio = 10.  # Global ratio
    routes = {}  # Global routes costs

    def __init__(self, nodes, fast=False):
        """
        Initialise a TSP instance based on a scenario.

        Parameters:

            - nodes: nodes in the scenario
        """
        self.nodes = nodes
        self.fast = fast

        self.initial_path = nodes
        self.initial_cost = self.pathCost(nodes)
        # Do not save the initial path as it is not optimised
        self.heuristic_path = self.initial_path
        self.heuristic_cost = self.initial_cost

    def save(self, path, cost):
        """
        Save the heuristic cost and path.

        Parameters:

            - path: path

            - cost: cost of the path
        """
        self.heuristic_path = path
        self.heuristic_cost = cost

        self.routes[str(sorted(path))] = {"path": path, "cost": cost}

    def update(self, solution):
        """
        Update the heuristic solution with the master solution.

        Parameters:

            - solution: current master solution

        Updating the path should always be done on the initial path.

        >>> from tsp_local.test import TSPTest, matrix
        >>> TSP.setEdges(matrix)
        >>> l = list(range(len(matrix)))
        >>> t = TSPTest(l)
        >>> t.update(l[2:])
        >>> set(t.heuristic_path) == set([2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12])
        True
        >>> t.update(l[:2])
        >>> set(t.heuristic_path) == set([0, 1])
        True
        >>> t.update(l[2:7])
        >>> set(t.heuristic_path) == set([2, 3, 4, 5, 6])
        True
        """
        self.heuristic_path = [i for i in self.initial_path if i in solution]
        self.heuristic_cost = self.pathCost(self.heuristic_path)

    def __str__(self):
        out = "Route with {} nodes ({}):\n".format(
            len(self.heuristic_path), self.heuristic_cost)

        if self.heuristic_cost > 0:
            out += " -> ".join(map(str, self.heuristic_path))
            out += " -> {}".format(self.heuristic_path[0])
        else:
            out += "No current route."

        return out

    @staticmethod
    def dist(i, j):
        return TSP.edges[i][j]

    @staticmethod
    def pathCost(path):
        # Close the loop
        cost = TSP.dist(path[-1], path[0])

        for i in range(1, len(path)):
            cost += TSP.dist(path[i - 1], path[i])

        return cost

    @staticmethod
    def setRatio(ratio):
        TSP.ratio = ratio

    @staticmethod
    def setEdges(edges):
        TSP.edges = edges

    def optimise(self):
        """
        Check if the current route already exists before optimising.

        >>> from tsp_local.test import TSPTest, matrix
        >>> l = list(range(4))
        >>> TSP.setEdges(matrix)
        >>> t = TSPTest(l)
        >>> t.routes[str(sorted(l))] = {"path": l, "cost": 16}
        >>> t.heuristic_path = l
        >>> t.optimise()
        ([0, 1, 2, 3], 16)
        """
        route = str(sorted(self.heuristic_path))

        if route in self.routes:
            saved = TSP.routes[route]
            self.heuristic_path = saved["path"]
            self.heuristic_cost = saved["cost"]
        else:
            self._optimise()

        return self.heuristic_path, self.heuristic_cost

    @abstractmethod
    def _optimise(self):
        """
        Use an optimisation heuristic on the current TSP.
        """
        pass


if __name__ == "__main__":
    import doctest
    doctest.testmod()
