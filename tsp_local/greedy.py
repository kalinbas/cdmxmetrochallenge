from tsp_local.base import TSP

class Greedy(TSP):
    """
    Implement the greedy heuristic for the TSP.
    """

    def _optimise(self):
        """
        Cheapest relink.

        >>> from tsp_local.test import matrix
        >>> TSP.setEdges(matrix)
        >>> l = list(range(len(matrix)))
        >>> t = Greedy(l)

        Force initial solution.
        >>> t.heuristic_path = l
        >>> t.heuristic_cost = t.pathCost(l)
        >>> t._optimise()
        >>> t.heuristic_cost < t.pathCost(l)
        True
        >>> t.heuristic_cost == t.pathCost(t.heuristic_path)
        True

        """
        if len(self.heuristic_path) == 0:
            return

        nodes = set(self.heuristic_path)
        i = nodes.pop()
        path = [i]
        cost = 0

        while len(nodes) > 0:
            best = float('inf')

            for j in nodes:
                dist = self.dist(i, j)

                if dist < best:
                    best = dist
                    node = j

            path.append(node)
            cost += best
            i = node
            nodes.remove(node)

        self.save(path, cost + self.dist(path[-1], path[0])) # Relink


if __name__ == "__main__":
    import doctest
    doctest.testmod()
