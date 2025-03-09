import pandas as pd
import os

# Function to load the cluster assignments from a file
def load_cluster_assignments(cluster_file):
    cluster_assignments = pd.read_csv(cluster_file, sep='\t', header=None, names=["Node", "Cluster"])
    return cluster_assignments

# Function to load the network file (edge list)
def load_network(network_file):
    network = pd.read_csv(network_file, sep='\t', header=None, names=["Node1", "Node2"])
    return network

# Function to count the number of cut edges
def count_cut_edges(network, cluster_assignments):
    # Merge the cluster assignments with the network edges on the nodes
    merged_network = pd.merge(network, cluster_assignments, left_on='Node1', right_on='Node', how='left')
    merged_network = pd.merge(merged_network, cluster_assignments, left_on='Node2', right_on='Node', how='left', suffixes=('_1', '_2'))

    # Count the edges where the two nodes belong to different clusters
    cut_edges = merged_network[merged_network["Cluster_1"] != merged_network["Cluster_2"]]
    
    return len(cut_edges)

# Function to process each network and its clustering results
def process_networks_and_clusters(network_files, cluster_dir):
    results = []
    
    for network_file in network_files:
        network_name = network_file.split('.')[0]  # Get the base name of the network
        
        # Load the network
        network_path = os.path.join("/projects/illinois/eng/shared/shared/CS598GCK-SP25/assig2_networks/", network_file)
        network = load_network(network_path)
        
        # Loop through the three clustering files for each network
        for resolution in ["CPM_0.01", "CPM_0.001", "Modularity_"]:
            cluster_file = os.path.join(cluster_dir, f"{network_name}_{resolution}.tsv")
            
            # Load the cluster assignments
            cluster_assignments = load_cluster_assignments(cluster_file)
            
            # Count the removed edges
            num_removed_edges = count_cut_edges(network, cluster_assignments)
            
            # Store the result (network name, clustering type, number of removed edges)
            results.append((network_name, resolution, num_removed_edges))
            
            print(f"Network: {network_name}, Clustering: {resolution}, Removed Edges: {num_removed_edges}")
    
    return results

# Main function
def main():
    # List of network files (adjusted to 5 networks)
    network_files = [
        "cen_cleaned.tsv", "cit_hepph_cleaned.tsv", "cit_patents_cleaned.tsv",
        "wiki_topcats_cleaned.tsv", "wiki_talk_cleaned.tsv"  # Add your fifth network here
    ]
    
    # Directory containing the clustering files
    cluster_dir = "/u/tledfo2/scratch/assig_2/clustering_outputs"
    
    # Process the networks and their clustering results
    results = process_networks_and_clusters(network_files, cluster_dir)
    
    # Output the results to a file
    result_df = pd.DataFrame(results, columns=["Network", "Clustering", "Removed Edges"])
    result_df.to_csv("removed_edges_report.csv", index=False)
    print("Results saved to 'removed_edges_report.csv'")

# Run the script
if __name__ == "__main__":
    main()
