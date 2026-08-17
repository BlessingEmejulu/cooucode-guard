"""
Module: Graph Traversal and Shortest Path Utilities
Author: Student Solution
Date: 2026-08-17
"""

import heapq
from typing import Dict, List, Tuple, Any

def dijkstra_shortest_path(graph: Dict[str, Dict[str, float]], start_node: str) -> Dict[str, float]:
    """
    Computes the shortest paths from a single starting vertex to all other vertices.
    
    Parameters:
        graph (Dict[str, Dict[str, float]]): Weighted adjacency dictionary.
        start_node (str): The initial source vertex.
        
    Returns:
        Dict[str, float]: Dictionary mapping each vertex to its minimum distance.
        
    Time Complexity: O((V + E) log V)
    Space Complexity: O(V)
    """
    # Step 1: Initialize distances with infinity
    distances: Dict[str, float] = {vertex: float('inf') for vertex in graph}
    distances[start_node] = 0.0
    
    # Step 2: Initialize min-heap priority queue
    priority_queue: List[Tuple[float, str]] = [(0.0, start_node)]
    visited_vertices = set()
    
    # Step 3: Loop through the priority queue until empty
    while priority_queue:
        current_distance, current_vertex = heapq.heappop(priority_queue)
        
        # Check if vertex was already evaluated
        if current_vertex in visited_vertices:
            continue
        visited_vertices.add(current_vertex)
        
        # Step 4: Iterate over adjacent neighbor edges
        for neighbor, weight in graph.get(current_vertex, {}).items():
            calculated_distance = current_distance + weight
            
            # Step 5: Relax the edge if a shorter path is discovered
            if calculated_distance < distances[neighbor]:
                distances[neighbor] = calculated_distance
                heapq.heappush(priority_queue, (calculated_distance, neighbor))
                
    # Return the final computed shortest distances
    return distances

# Example usage driver code
if __name__ == "__main__":
    sample_network = {
        'A': {'B': 4, 'C': 2},
        'B': {'A': 4, 'C': 1, 'D': 5},
        'C': {'A': 2, 'B': 1, 'D': 8},
        'D': {'B': 5, 'C': 8}
    }
    result = dijkstra_shortest_path(sample_network, 'A')
    print("Computed shortest paths:", result)
