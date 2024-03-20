import json
from pyvis.network import Network
net = Network(bgcolor="#222222", font_color="white")

N = 300
C = 100

linetemplate = [-1]*C
lines = {
    "NS": linetemplate.copy(),
    "EW": linetemplate.copy(),
    "NE": linetemplate.copy(),
    "DT": linetemplate.copy(),
    "CC": linetemplate.copy(),
}

adjlist = [[] for i in range(N)]
visited = [False]*N

def bfs(s, e):
    queue = []
    prev = [None]*N
    queue.append(s)
    visited[s] = True

    while len(queue) > 0:
        node = queue.pop(0)
        for nextNode in adjlist[node]:
            if not visited[nextNode]:
                prev[nextNode] = node
                visited[nextNode] = True
                queue.append(nextNode)
        
        currentNode = e
    path = []
    while currentNode != None:
        path.append(currentNode)
        currentNode = prev[currentNode]

    path.reverse()
    return path

with open("formatted.json", "r") as file:
    mrts = json.load(file)

for mrt in mrts.keys():
    value = mrts[mrt]
    net.add_node(value[0], label=mrt)
    for station in value[1]:
        line = station[0:2]
        index = int(station[2:4])
        lines[line][index] = value[0]

for line in lines.keys():
    lines[line] = list(set(lines[line]))
    lines[line].remove(-1)
    stationNo = {}
    for i in lines[line]:
        c = [v[1] for k, v in mrts.items() if v[0] == i]
        c = c[0]
        for st in c:
            if line in st:
                c = st[2:4]
        stationNo[i] = int(c)
    lines[line] = sorted(lines[line], key=lambda st: stationNo[st])

for line in lines.keys():
    stations = lines[line]
    for station in stations:
        stationIndex = stations.index(station)
        after = stationIndex+1
        before = stationIndex-1
        if after <= len(stations)-1:
            nodeAfter = stations[after]
            adjlist[station].append(nodeAfter)
            net.add_edge(station, nodeAfter)
        if before >= 1:
            nodeBefore = stations[before]
            adjlist[station].append(nodeBefore)
            net.add_edge(station, nodeBefore)


path = bfs(20, 45)

for i in path:
    c = [k for k, v in mrts.items() if v[0] == i]
    c = c[0]
    print(c)

net.show("network.html", notebook=False)