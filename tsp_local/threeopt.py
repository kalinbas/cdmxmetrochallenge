from tsp_local.base import TSP

# Start with an obvious exchange
start = [0, 3, 2, 4, 5, 1]
# Hexagon where direct neighbours are at distance 1, others 3
hexagon = [[0, 1, 3, 3, 3, 1],
           [1, 0, 1, 3, 3, 3],
           [3, 1, 0, 1, 3, 3],
           [3, 3, 1, 0, 1, 3],
           [3, 3, 3, 1, 0, 1],
           [1, 3, 3, 3, 1, 0]]  # yapf: disable


def exchange(path, execute, a, c, e):
    """
    Reconnects the path given three edges to swap.

    >>> TSP.setEdges(hexagon)
    >>> exchange(start, 0, 0, 2, 4)
    ([0, 5, 4, 2, 3, 1], 2)
    >>> exchange(start, 1, 0, 2, 4)
    ([0, 3, 2, 5, 4, 1], 0)
    >>> exchange(start, 2, 0, 2, 4)
    ([0, 2, 3, 4, 5, 1], 2)
    >>> exchange(start, 3, 0, 2, 4)
    ([0, 4, 5, 2, 3, 1], 0)
    >>> exchange(start, 4, 0, 2, 4)
    ([0, 4, 5, 3, 2, 1], 2)
    >>> exchange(start, 5, 0, 2, 4)
    ([0, 5, 4, 3, 2, 1], 6)
    >>> exchange(start, 6, 0, 2, 4)
    ([0, 2, 3, 5, 4, 1], 0)
    """
    b, d, f = a + 1, c + 1, e + 1

    p_a, p_b, p_c, p_d, p_e, p_f = [path[i] for i in (a, b, c, d, e, f)]

    base = TSP.dist(p_a, p_b) + TSP.dist(p_c, p_d) + TSP.dist(p_e, p_f)

    if execute == 0:
        # 2-opt (a, e) [d, c] (b, f)
        sol = path[:a + 1] + path[e:d - 1:-1] + path[c:b - 1:-1] + path[f:]
        gain = TSP.dist(p_a, p_e) + TSP.dist(p_c, p_d) + TSP.dist(p_b, p_f)
    elif execute == 1:
        # 2-opt [a, b] (c, e) (d, f)
        sol = path[:a + 1] + path[b:c + 1] + path[e:d - 1:-1] + path[f:]
        gain = TSP.dist(p_a, p_b) + TSP.dist(p_c, p_e) + TSP.dist(p_d, p_f)
    elif execute == 2:
        # 2-opt (a, c) (b, d) [e, f]
        sol = path[:a + 1] + path[c:b - 1:-1] + path[d:e + 1] + path[f:]
        gain = TSP.dist(p_a, p_c) + TSP.dist(p_b, p_d) + TSP.dist(p_e, p_f)
    elif execute == 3:
        # 3-opt (a, d) (e, c) (b, f)
        sol = path[:a + 1] + path[d:e + 1] + path[c:b - 1:-1] + path[f:]
        gain = TSP.dist(p_a, p_d) + TSP.dist(p_e, p_c) + TSP.dist(p_b, p_f)
    elif execute == 4:
        # 3-opt (a, d) (e, b) (c, f)
        sol = path[:a + 1] + path[d:e + 1] + path[b:c + 1] + path[f:]
        gain = TSP.dist(p_a, p_d) + TSP.dist(p_e, p_b) + TSP.dist(p_c, p_f)
    elif execute == 5:
        # 3-opt (a, e) (d, b) (c, f)
        sol = path[:a + 1] + path[e:d - 1:-1] + path[b:c + 1] + path[f:]
        gain = TSP.dist(p_a, p_e) + TSP.dist(p_d, p_b) + TSP.dist(p_c, p_f)
    elif execute == 6:
        # 3-opt (a, c) (b, e) (d, f)
        sol = path[:a + 1] + path[c:b - 1:-1] + path[e:d - 1:-1] + path[f:]
        gain = TSP.dist(p_a, p_c) + TSP.dist(p_b, p_e) + TSP.dist(p_d, p_f)

    return sol, base - gain


class ThreeOpt(TSP):
    """
    Implement the 3-opt for the TSP.

    Try with an hexagon.
    >>> TSP.setEdges(hexagon)
    >>> t = ThreeOpt(range(6))
    >>> t.heuristic_path = start
    >>> t.heuristic_cost = t.pathCost(start) # = 12 = 3 * 1 + 3 * 3
    >>> t._optimise()
    >>> t.heuristic_cost
    6
    """

    def _optimise(self):
        """
        U.S. test.

        >>> from tsp_local.test import matrix
        >>> TSP.setEdges(matrix)
        >>> l = list(range(len(matrix)))
        >>> t = ThreeOpt(l)

        Force initial solution.
        >>> t.heuristic_path = l
        >>> t.heuristic_cost = t.pathCost(l) # 18703
        >>> t._optimise()
        >>> t.heuristic_cost < t.pathCost(l)
        True
        """
        bestPath = self.heuristic_path
        bestCost = self.pathCost(self.heuristic_path)
        bestChange = 1
        size = len(self.heuristic_path)

        while bestChange > 0:
            saved, bestChange = self._improve(bestPath, size)

            if bestChange > 0:
                a, c, e, which = saved
                bestPath, change = exchange(bestPath, which, a, c, e)
                bestCost -= change

        self.save(bestPath, bestCost)

    def _improve(self, bestPath, size):
        """
        Breakable improvement loop, find an improving move and return to the
        main loop to execute it, selects whether we look for the first
        improving move or the best.
        """
        saved = None
        bestChange = 0

        # Choose 3 unique edges defined by their first node
        for a in range(size - 5):
            for c in range(a + 2, size - 3):
                for e in range(c + 2, size - 1):
                    change = 0
                    # Now we have seven (sic) permutations to check
                    for i in range(7):
                        # TODO improve this...
                        path, change = exchange(bestPath, i, a, c, e)

                        if change > bestChange:
                            saved = a, c, e, i
                            bestChange = change

                            # Cut short if fast
                            if self.fast:
                                return saved, bestChange

        return saved, bestChange


if __name__ == "__main__":
    import doctest
    doctest.testmod()
