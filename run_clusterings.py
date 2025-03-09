import igraph as ig
import leidenalg as la
import os
import time
import pandas as pd

# Function to read the network from a TSV file and create the graph
def load_network(file_path):
    # Read the edge list from a TSV file
    graph = ig.Graph.Read_Ncol(file_path, directed=False)
    return graph

# Function to apply Leiden algorithm (CPM with given resolution or Modularity)
def apply_leiden_algorithm(graph, model, resolution=None):
    if model == "CPM":
        # Apply CPM with a specific resolution
        partition = la.find_partition(graph, la.CPMVertexPartition, resolution_parameter=resolution)
    elif model == "Modularity":
        # Apply Modularity optimization
        partition = la.find_partition(graph, la.ModularityVertexPartition)
    else:
        raise ValueError("Model should be either 'CPM' or 'Modularity'")
    return partition

# Function to output the clusters to a file
def output_clusters(partition, output_file):
    # Write the node membership (which node belongs to which cluster) to a file
    with open(output_file, 'w') as f:
        for node, cluster_id in enumerate(partition.membership):
            f.write(f"{node}\t{cluster_id}\n")
    print(f"Cluster membership saved to: {output_file}")

# Function to log run time for each clustering
def log_run_time(report_file, network_name, model, resolution, run_time):
    with open(report_file, 'a') as report:
        report.write(f"{network_name}\t{model}\t{resolution}\t{run_time:.4f} seconds\n")

# Main function to run the clustering algorithm
def main():
    # Path to your network files (TSV format)
    network_dir = "/projects/illinois/eng/shared/shared/CS598GCK-SP25/assig2_networks/"
    
    # Define the output report file for run times
    report_file = "./re_run.txt"
    
    # Open the report file and add headers
    with open(report_file, 'w') as report:
        report.write("Network\tModel\tResolution\tRunTime(s)\n")

    # List of network files in the directory
    network_files = [f for f in os.listdir(network_dir) if f.endswith('.tsv')]
    
    # Define the output files for each model and resolution
    output_files = {
        "CPM_0.01": "clustering_CPM_0.01.tsv",
        "CPM_0.001": "clustering_CPM_0.001.tsv",
        "Modularity": "clustering_modularity.tsv"
    }

    # Iterate over each network file
    for network_file in network_files:
        network_name = network_file.split('.')[0]  # Extract the base name of the network file
        
        # Load the network
        network_file_path = os.path.join(network_dir, network_file)
        print(f"Loading network from: {network_file_path}")
        graph = load_network(network_file_path)

        # Run the Leiden algorithm for each model (CPM with different resolutions and Modularity)
        models = [("CPM", 0.01), ("CPM", 0.001), ("Modularity", None)]

        for model, resolution in models:
            print(f"Running Leiden algorithm with {model} (resolution: {resolution})...")
            
            # Start the timer
            start_time = time.time()
            
            # Apply Leiden algorithm
            partition = apply_leiden_algorithm(graph, model, resolution)
            
            # Generate the output file path
            output_file = f"./clustering_outputs_2/{network_name}_{model}_{resolution if resolution else ''}.tsv"
            output_clusters(partition, output_file)
            
            # Stop the timer
            end_time = time.time()
            run_time = end_time - start_time
            
            # Log the run time to the report file
            log_run_time(report_file, network_name, model, resolution, run_time)

    print("Clustering completed successfully!")

# Run the script
if __name__ == "__main__":
    main()
