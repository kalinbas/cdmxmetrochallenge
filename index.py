# Data from https://datos.cdmx.gob.mx/explore/dataset/estaciones-metro/table/
# Best Python LKH implementation from https://arthur.maheo.net/implementing-lin-kernighan-in-python/
# Dijkstra implementation adapted from https://www.geeksforgeeks.org/python-program-for-dijkstras-shortest-path-algorithm-greedy-algo-7/

import pandas as pd 
import numpy as np
import geopy.distance
import graph

from tsp_local.base import TSP
from tsp_local.kopt import KOpt

# calculates estimated time to travel from stop 1 to 2
# if not same line add some time to change and wait for new train
def calculateEstimatedMins(s1, s2):

    averageSpeed = 35.0
    averageWalkSpeed = 5.0
    switchMins = 3.0

    ll1 = (float(s1["Lat"]), float(s1["Lng"]))
    ll2 = (float(s2["Lat"]), float(s2["Lng"]))
    sameLine = s1["LineID"] == s2["LineID"]
    distKm = geopy.distance.distance(ll1, ll2).km

    if sameLine:
        return (distKm / averageSpeed) * 60.0
    else:
        return (distKm / averageWalkSpeed) * 60.0 + switchMins


# read station info
data = pd.read_csv("metro_stations.csv") #ID,Name,Lat,Lng,LineID
station_count = data.shape[0]

# create graph for distance calculation
g = graph.Graph()

# adds vertices / edges with calculated cost (estimated time) - simple edges of same line
for index, stop in data.iterrows():
    if index < station_count - 1:
        nextStop = data.iloc[index + 1]
        if nextStop["LineID"] == stop["LineID"]:
            g.add_edge(index, index + 1, calculateEstimatedMins(stop, nextStop))

# adds vertices / edges with calculated cost (estimated time) -  edges to connect to other lines
for index, stop in data.iterrows():
    mask = data['Name'] == stop["Name"]
    if np.count_nonzero(mask) > 1:
        indices = np.where(mask)[0]
        for otherIndex in indices:
            if otherIndex < index:
                sameStop = data.iloc[otherIndex]
                g.add_edge(index, otherIndex, calculateEstimatedMins(stop, sameStop))

# calculate complete distance / path table
dist = np.zeros((station_count, station_count))
distPath = np.empty((station_count, station_count), dtype=object)
for v in g:
    distances, paths = g.dijkstra(v.get_id())
    for id, cost in distances.items():
        dist[v.get_id()][id] = cost
    for id, p in paths.items():
        distPath[v.get_id()][id] = p

# use TSP algorithm
TSP.setEdges(dist)
lk = KOpt(list(range(station_count)))
result, cost = lk.optimise()

total = 0

# print solution
for i, index in enumerate(result):
    currentName = data.iloc[index]["Name"] + ' ' + data.iloc[index]["LineID"]
    nextIndex = result[(i + 1) % len(result)]
    total += dist[index][nextIndex]

    print(currentName)

    for p in distPath[index][nextIndex]:
        if p != index and p != nextIndex:
            name = data.iloc[p]["Name"] + ' ' + data.iloc[p]["LineID"]
            print(">", name)

print(total)