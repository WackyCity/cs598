import networkit as nk
import numpy as np

# 1. Network Analysis (Loading the Network and Calculating Basic Stats)

def load_network(network_file):
    """Load the network from a TSV edge list file and calculate basic stats."""
    G = nk.Graph()
    with open(network_file, 'r') as f:
        for line in f:
            # Assuming the file is tab-separated and contains edges like: source_node \t target_node
            source, target = map(int, line.strip().split('\t'))
            
            # Ensure both nodes are added to the graph before adding the edge
            # If the node doesn't exist, add it.
            while source >= G.numberOfNodes():
                G.addNode()
            while target >= G.numberOfNodes():
                G.addNode()
                
            # Add the edge between the nodes
            G.addEdge(source, target)

    num_nodes = G.numberOfNodes()
    num_edges = G.numberOfEdges()
    return G, num_nodes, num_edges

# Load the network and calculate basic statistics
network_file = "/projects/illinois/eng/shared/shared/CS598GCK-SP25/assig2_networks/wiki_topcats_cleaned.tsv"  # Path to your network file
G, num_nodes, num_edges = load_network(network_file)

# Print network statistics
print(f"Number of nodes: {num_nodes}")
print(f"Number of edges: {num_edges}")

# 2. Cluster Analysis (Calculating Cluster Metrics)

def load_cluster_file(cluster_file):
    """Load cluster membership file into a list of clusters."""
    clusters = []
    with open(cluster_file, 'r') as file:
        for line in file:
            # Split by tab and take the second value (cluster ID)
            parts = line.strip().split('\t')
            if len(parts) == 2:
                node_id, cluster_id = parts
                clusters.append(int(cluster_id))
            else:
                # Handle cases where the line might not have exactly 2 parts
                print(f"Skipping invalid line: {line.strip()}")
    return clusters

def calculate_cluster_metrics(clusters, total_nodes):
    """Calculate various cluster metrics."""
    # Count cluster sizes
    cluster_sizes = {}
    for cluster in clusters:
        if cluster not in cluster_sizes:
            cluster_sizes[cluster] = 0
        cluster_sizes[cluster] += 1
    
    # Count singletons and non-singletons
    singletons = [size for size in cluster_sizes.values() if size == 1]
    non_singletons = [size for size in cluster_sizes.values() if size > 1]
    
    num_singletons = len(singletons)
    num_non_singletons = len(non_singletons)
    
    # Calculate percentages
    percent_singletons = (num_singletons / len(cluster_sizes)) * 100
    percent_non_singletons = (num_non_singletons / len(cluster_sizes)) * 100
    
    # Cluster size distribution (non-singleton)
    non_singleton_sizes = sorted(non_singletons)
    
    # Calculate statistics (min, quartiles, median, max)
    min_size = np.min(non_singleton_sizes)
    q1 = np.percentile(non_singleton_sizes, 25)
    median = np.median(non_singleton_sizes)
    q3 = np.percentile(non_singleton_sizes, 75)
    max_size = np.max(non_singleton_sizes)
    
    # Node coverage (percentage of nodes in non-singletons)
    node_coverage = (sum(non_singletons) / total_nodes) * 100
    
    return {
        "num_singletons": num_singletons,
        "percent_singletons": percent_singletons,
        "num_non_singletons": num_non_singletons,
        "percent_non_singletons": percent_non_singletons,
        "min_size": min_size,
        "q1": q1,
        "median": median,
        "q3": q3,
        "max_size": max_size,
        "node_coverage": node_coverage,
    }

def analyze_clusters(cluster_files, num_nodes):
    """Analyze multiple cluster files and output metrics."""
    for cluster_file in cluster_files:
        clusters = load_cluster_file(cluster_file)
        metrics = calculate_cluster_metrics(clusters, num_nodes)
        
        print(f"Metrics for {cluster_file}:")
        print(f"  Number of singletons: {metrics['num_singletons']}")
        print(f"  Percentage of singletons: {metrics['percent_singletons']:.2f}%")
        print(f"  Number of non-singletons: {metrics['num_non_singletons']}")
        print(f"  Percentage of non-singletons: {metrics['percent_non_singletons']:.2f}%")
        print(f"  Non-singleton cluster size distribution (min, Q1, median, Q3, max):")
        print(f"    Min size: {metrics['min_size']}")
        print(f"    Q1: {metrics['q1']}")
        print(f"    Median: {metrics['median']}")
        print(f"    Q3: {metrics['q3']}")
        print(f"    Max size: {metrics['max_size']}")
        print(f"  Node coverage: {metrics['node_coverage']:.2f}%\n")

# 3. Cluster files to analyze
cluster_files = [
    "clustering_outputs/wiki_topcats_cleaned_CPM_0.01.tsv",
    "clustering_outputs/wiki_topcats_cleaned_CPM_0.001.tsv",
    "clustering_outputs/wiki_topcats_cleaned_Modularity_.tsv"
]

# Now analyze clusters after network statistics are loaded
analyze_clusters(cluster_files, num_nodes)
