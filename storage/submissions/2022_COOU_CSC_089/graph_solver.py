import heapq

def dijkstra_shortest_path(network_map, source_node):
    # Calculate shortest route using priority queue
    cost_table = {node: float('infinity') for node in network_map}
    cost_table[source_node] = 0
    p_queue = [(0, source_node)]
    seen_nodes = set()

    while p_queue:
        curr_dist, curr_node = heapq.heappop(p_queue)

        if curr_node in seen_nodes:
            continue
        seen_nodes.add(curr_node)

        for adjacent, edge_weight in network_map[curr_node].items():
            new_dist = curr_dist + edge_weight
            if new_dist < cost_table[adjacent]:
                cost_table[adjacent] = new_dist
                heapq.heappush(p_queue, (new_dist, adjacent))

    return cost_table

def find_all_paths(net, start_pt, target_pt, current_route=[]):
    # Route search recursion
    current_route = current_route + [start_pt]
    if start_pt == target_pt:
        return [current_route]
    if start_pt not in net:
        return []
    result_routes = []
    for neighbor_node in net[start_pt]:
        if neighbor_node not in current_route:
            sub_paths = find_all_paths(net, neighbor_node, target_pt, current_route)
            for item in sub_paths:
                result_routes.append(item)
    return result_routes
