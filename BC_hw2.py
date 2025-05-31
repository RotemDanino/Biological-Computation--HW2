from itertools import combinations
import networkx as nx
from networkx.algorithms.isomorphism import DiGraphMatcher
import time
import multiprocessing
from multiprocessing import Process

def connected_sub_graphs(n):
    graphs = []
    nx_graphs = []
    if n==1:
        g = set()
        g.add((1, 1))
        graphs.append(g)
        convert_to_txt(n, graphs)
        return

    #create the biggest graph- with all directed edges:
    complete_graph = set()
    for i in range(1, n+1):
        for j in range(1, n+1):
            if i != j:
                complete_graph.add((i, j))
    #the complete graph is always part of the connected graphs:
    graphs.append(complete_graph)
    G = nx.DiGraph()
    G.add_edges_from(complete_graph)
    nx_graphs.append(G)

    #all other graphs are subgraphs of the complete graph,
    #so we can obtain them by removing one or more edges.

    #outer loop is iterating on how many edeges to remove.
    #in order for the graph to be connected, we cant remove more then (n-1)^2 edges.
    max_edges = (n-1)*(n-1)
    complete_graph_size = n*(n-1)
    for k in range(1,max_edges+1):
        #now we need to loop over all the options to remove k edges:
        for g in combinations(complete_graph, complete_graph_size-k):
            g = set(g)
            #make sure the graph is connected as an undirected graph:
            g_nx = nx.DiGraph()
            g_nx.add_nodes_from(range(1, n+1))
            g_nx.add_edges_from(g)
            g_nx_undirected = g_nx.to_undirected()
            if not nx.is_connected(g_nx_undirected):
                continue
            #make sure that this type of control is not already in the graphs:
            #the same type of control on different nodes will be isomorphic graphs
            nx_graphs_size = len(nx_graphs)
            flag = 0
            for l in range(nx_graphs_size):
                matcher = DiGraphMatcher(nx_graphs[l], g_nx)
                iso = matcher.is_isomorphic()
                if iso ==True:
                    flag = 1
                    break
            if flag == 0:
                graphs.append(g)
                nx_graphs.append(g_nx)

    #save the output into a tetual file in the given format:
    convert_to_txt(n, graphs)
    return

def convert_to_txt(n, graphs):
    filename = f"Q1_output_{n}.txt"
    with open(filename, 'w') as f:
        f.write(f"n={n}\n")
        f.write(f"count={len(graphs)}\n")
        for idx, graph in enumerate(graphs, start=1):
            f.write(f"#{idx}\n")
            for edge in graph:
                f.write(f"{edge[0]} {edge[1]}\n")

    return

def run_connected(n, return_dict):
    try:
        connected_sub_graphs(n)
        return_dict["success"] = True
    except Exception as e:
        return_dict["success"] = False
        return_dict["error"] = str(e)

def Q1_c_d(X):
    log_filename = "Q1_cd_output.txt"
    total_seconds = X * 3600
    start_time = time.time()
    next_log_time = start_time + 3600  # first log after one hour
    n = 1
    last_completed_n = 0

    with open(log_filename, 'w') as log_file:
        while True:
            current_time = time.time()

            # Check total time
            if current_time - start_time >= total_seconds:
                print("Reached total time limit.")
                break

            print(f"Trying n={n}...")

            manager = multiprocessing.Manager()
            return_dict = manager.dict()
            p = Process(target=run_connected, args=(n, return_dict))

            t0 = time.time()
            p.start()

            while p.is_alive():
                p.join(timeout=1)
                if time.time() - start_time >= total_seconds:
                    print(f"Time limit reached during computation of n={n}. Terminating...")
                    p.terminate()
                    p.join()
                    break

            if return_dict.get("success"):
                elapsed = time.time() - t0
                print(f"n={n} completed in {elapsed:.2f} seconds")
                last_completed_n = n
                n += 1
            else:
                print(f"Failed or terminated at n={n}")
                break

            # Write log every hour
            if time.time() >= next_log_time:
                hours_passed = int((next_log_time - start_time) // 3600)
                log_file.write(f"After {hours_passed} hour(s): max completed n = {last_completed_n}\n")
                log_file.flush()
                print(f"[Log] Hour {hours_passed}: last completed n = {last_completed_n}")
                next_log_time += 3600

        # Final log
        final_hours_passed = int((time.time() - start_time) // 3600)
        log_file.write(f"After {final_hours_passed} hour(s): max completed n = {last_completed_n}\n")
        print(f"[Log] Final: Hour {final_hours_passed}: last completed n = {last_completed_n}")

def extract_graph(filename):
    with open(filename, 'r') as file:
        lines = file.readlines()

    graphs = []
    current_graph = set()
    nodes = set()
    has_multiple_graphs = any(line.startswith("#") for line in lines)

    for line in lines:
        line = line.strip()
        if not line or line.startswith("n=") or line.startswith("count="):
            continue
        elif line.startswith("#"):
            if current_graph:
                graphs.append(current_graph)
                current_graph = set()
        else:
            parts = line.split()
            if len(parts) == 2:
                a, b = int(parts[0]), int(parts[1])
                edge = (a, b)
                current_graph.add(edge)
                nodes.add(a)
                nodes.add(b)

    if current_graph:
        graphs.append(current_graph)

    n = len(nodes)

    if not has_multiple_graphs:
        return list(graphs[0]), n  # for Q2 input
    else:
        return graphs, n  # for Q1 output

def count_motifs(input_file):
    graph, n = extract_graph(input_file)
    input_graph_size = len(graph)

    # Create all directed sub-graphs (size n) of the given graph
    max_edges = input_graph_size - (n - 1)
    sub_graphs = []
    for k in range(max_edges + 1):
        for g in combinations(graph, input_graph_size - k):
            g = set(g)
            g_nx = nx.DiGraph()
            g_nx.add_nodes_from(range(1, n + 1))
            g_nx.add_edges_from(g)
            g_nx_undirected = g_nx.to_undirected()
            if nx.is_connected(g_nx_undirected):
                sub_graphs.append(g)

    # Read all motifs from Q1_output:
    motifs_file = f"Q1_output_{n}.txt"
    motifs, n = extract_graph(motifs_file)

    # Create networkx graphs for each subgraph
    sub_graphs_nx = []
    for g in sub_graphs:
        g_nx = nx.DiGraph()
        g_nx.add_nodes_from(range(1, n + 1))
        g_nx.add_edges_from(g)
        sub_graphs_nx.append(g_nx)

    # Prepare output file
    output_file = f"Q2_output_{n}.txt"
    with open(output_file, 'w') as out_file:
        # Count how many instances appear of each motif:
        for j in range(len(motifs)):
            instances = []
            motif_nx = nx.DiGraph()
            motif_nx.add_nodes_from(range(1, n + 1))
            motif_nx.add_edges_from(list(motifs[j]))

            i = 0
            while i < len(sub_graphs_nx):
                matcher = DiGraphMatcher(sub_graphs_nx[i], motif_nx)
                if matcher.is_isomorphic():
                    instances.append(sub_graphs[i])
                    del sub_graphs[i]
                    del sub_graphs_nx[i]
                    # do not increment i, since lists shrunk
                else:
                    i += 1

            # Write motif header and count
            out_file.write(f"#{j + 1}\n")
            out_file.write(f"count = {len(instances)}\n")

            # Write instances of motif j
            for instance in instances:
                line = ", ".join(f"{a} {b}" for (a, b) in instance)
                out_file.write(line + "\n")
    return

def Q1_a_b():
    connected_sub_graphs(1)
    connected_sub_graphs(2)
    connected_sub_graphs(3)
    connected_sub_graphs(4)

def Q2(input_file):
    count_motifs(input_file)

def main():
    Q1_a_b()
    Q2('Q2_input.txt')
    # Q1_c_d(8)


if __name__=='__main__':
    main()


