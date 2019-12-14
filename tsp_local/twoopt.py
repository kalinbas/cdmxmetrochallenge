from tsp_local.base import TSP

# Cross circuit with obvious 2-opt
# A   B    A - B
# | X | -> |   |
# D   C    D - C
cross = [[0, 2, 3, 2], [2, 0, 2, 3], [3, 2, 0, 2], [2, 3, 2, 0]]
start = [0, 2, 1, 3]


def swap(path, i, j):
    """
    Swap two elements in a list and reverse what was in between.

    >>> swap([1, 2, 3, 4, 5], 1, 2)
    [1, 3, 2, 4, 5]
    >>> swap([1, 2, 3, 4, 5], 0, 3)
    [4, 3, 2, 1, 5]
    >>> swap([0, 1, 2, 3, 4, 5, 6, 7, 8, 9], 0, 1)
    [1, 0, 2, 3, 4, 5, 6, 7, 8, 9]
    >>> swap([0, 1, 2, 3, 4, 5, 6, 7, 8, 9], 2, 6)
    [0, 1, 6, 5, 4, 3, 2, 7, 8, 9]
    >>> swap(start, 0, 2)
    [1, 2, 0, 3]
    """

    return path[:i] + list(reversed(path[i:j + 1])) + path[j + 1:]


class TwoOpt(TSP):
    """
    Implement the 2-opt operator for the TSP.

    Cross optimisation
    >>> TSP.setEdges(cross)
    >>> t = TwoOpt(range(4))
    >>> t.heuristic_path = start
    >>> t.heuristic_cost = 10
    >>> t._optimise()
    >>> t.heuristic_cost
    8
    """

    def _optimise(self):
        """
        U.S. test.

        >>> from tsp_local.test import matrix
        >>> TSP.setEdges(matrix)
        >>> l = list(range(len(matrix)))
        >>> t = TwoOpt(l)

        Force initial solution.
        >>> t.heuristic_path = l
        >>> t.heuristic_cost = t.pathCost(l) # 18703
        >>> t._optimise()
        >>> t.heuristic_cost < t.pathCost(l)
        True
        """
        bestChange = -1
        bestPath = self.heuristic_path
        size = len(bestPath)

        while bestChange < 0:
            saved, bestChange = self._improve(bestPath, size)

            if bestChange < 0:
                i, j = saved  # `i` is the last element in place
                bestPath = swap(bestPath, i + 1, j)

        self.save(bestPath, self.pathCost(bestPath))

    def _improve(self, bestPath, size):
        bestChange = 0
        saved = None

        for n in range(size - 3):
            for m in range(n + 2, size - 1):
                i = bestPath[n]
                j = bestPath[m]
                k = bestPath[n + 1]
                l = bestPath[m + 1]

                # Replacement arcs are:
                #  * i -> k => i -> j
                #  * j -> l => k -> l
                change = self.dist(i, j) + self.dist(k, l)
                change -= self.dist(i, k) + self.dist(j, l)

                if change < bestChange:
                    bestChange = change
                    saved = (n, m)

                    # If fast, we return the first improving move
                    if self.fast:
                        return saved, bestChange
                    # Otherwise, we explore all possible moves

        return saved, bestChange


if __name__ == "__main__":
    import doctest
    doctest.testmod()
