import numpy as np

class Vertex:
    def __init__(self, node):
        self.id = node
        self.adjacent = {}

    def set_neighbor(self, neighbor, cost=0):
        self.adjacent[neighbor] = cost

    def get_connections(self):
        return self.adjacent.keys()  

    def get_id(self):
        return self.id

    def get_weight(self, neighbor):
        return self.adjacent[neighbor]

class Graph:
    def __init__(self):
        self.vert_dict = {}

    def __iter__(self):
        return iter(self.vert_dict.values())

    def add_vertex(self, node):
        if not node in self.vert_dict:
            new_vertex = Vertex(node)
            self.vert_dict[node] = new_vertex

    def get_vertex(self, n):
        if n in self.vert_dict:
            return self.vert_dict[n]
        else:
            return None

    def add_edge(self, frm, to, cost = 0):
        if frm not in self.vert_dict:
            self.add_vertex(frm)
        if to not in self.vert_dict:
            self.add_vertex(to)

        self.vert_dict[frm].set_neighbor(self.vert_dict[to], cost)
        self.vert_dict[to].set_neighbor(self.vert_dict[frm], cost)

    def get_vertices(self):
        return self.vert_dict.keys()

    # get vertex with minimum distance
    def minDistance(self, dist, sptSet): 
  
        min = None
  
        # Search nearest vertex not yet in the shortest path set
        for v in self.vert_dict.values(): 
            if dist[v.get_id()] != None and (min == None or dist[v.get_id()] < min) and not sptSet[v.get_id()]: 
                min = dist[v.get_id()] 
                min_index = v.get_id()
  
        return self.vert_dict[min_index]

    # searches shortest paths from start node to all other nodes
    def dijkstra(self, start): 
  
        dist = { key: None for key in [*self.vert_dict] }
        path = { key: [] for key in [*self.vert_dict] }
        dist[start] = 0
        path[start] = []
        sptSet = { key: False for key in [*self.vert_dict] }
  
        # repeat until all shortest paths have been found
        while not np.all(list(sptSet.values())): 
  
            # closest node not yet finished
            u = self.minDistance(dist, sptSet) 
   
            sptSet[u.get_id()] = True
   
            for v in u.get_connections(): 
                cost = u.get_weight(v)
                if dist[v.get_id()] == None or dist[v.get_id()] > dist[u.get_id()] + cost: 
                    dist[v.get_id()] = dist[u.get_id()] + cost
                    path[v.get_id()] = path[u.get_id()] + [u.get_id()]

        return dist, path