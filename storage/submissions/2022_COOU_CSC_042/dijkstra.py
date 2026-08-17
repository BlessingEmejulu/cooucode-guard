import heapq

def dijkstra_shortest_path(graph, start_vertex):
    distances = {vertex: float('infinity') for vertex in graph}
    distances[start_vertex] = 0
    pq = [(0, start_vertex)]
    visited = set()

    while pq:
        current_distance, current_vertex = heapq.heappop(pq)

        if current_vertex in visited:
            continue
        visited.add(current_vertex)

        for neighbor, weight in graph[current_vertex].items():
            distance = current_distance + weight
            if distance < distances[neighbor]:
                distances[neighbor] = distance
                heapq.heappush(pq, (distance, neighbor))

    return distances

def find_all_paths(graph, start, end, path=[]):
    path = path + [start]
    if start == end:
        return [path]
    if start not in graph:
        return []
    paths = []
    for node in graph[start]:
        if node not in path:
            newpaths = find_all_paths(graph, node, end, path)
            for p in newpaths:
                paths.append(p)
    return paths
