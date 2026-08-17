def solve_graph_reachability(adj_matrix):
    n = len(adj_matrix)
    reach = [row[:] for row in adj_matrix]
    
    for k in range(n):
        for i in range(n):
            for j in range(n):
                reach[i][j] = reach[i][j] or (reach[i][k] and reach[k][j])
                
    return reach

def print_matrix(mat):
    for r in mat:
        print(" ".join(str(int(x)) for x in r))
