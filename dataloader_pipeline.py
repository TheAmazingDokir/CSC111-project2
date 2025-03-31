from class_graph import Webgraph, _Website
import csv

def load_graph(vertices_file: str, edges_file: str, website_stats_file: str, load_with_stats_only: bool = False, n_vertices: int = 10000) -> Webgraph:
    """
    Load a web graph from the given files.

    Arguments:
        - vertices_file: The path to the file containing the vertices information.
        - edges_file: The path to the file containing the edges information.
        - website_stats_file: The path to the file containing the website statistics.
        - load_with_stats_only: A boolean indicating whether to load only websites that have.
        - n_vertices: The maximum number of vertices to load.
    """
    # Load vertices (websites)
    id_domain_mapping = {}

    with open(vertices_file, "r") as file:
        for line in file:
            site_id, domain = line.split()
            id_domain_mapping[int(site_id)] = domain

    domain_id_mapping = {domain: site_id for site_id, domain in id_domain_mapping.items()}

    # Load statistics for each website
    website_stats = {}

    with open(website_stats_file, "r") as file:
        csv_reader = csv.reader(file)
        next(csv_reader)  # Skip the header row

        for row in csv_reader:
            stats_entry = {}
            stats_entry["alexa_rank"] = int(row[0])
            stats_entry["domain_name"] = row[1]
            stats_entry["daily_min"] = float(row[2])
            stats_entry["daily_pageviews"] = float(row[3])
            stats_entry["traffic_ratio"] = float(row[4])
            stats_entry["site_links"] = int(row[5])
            stats_entry["tranco_rank"] = int(row[6])

            if stats_entry["domain_name"] in domain_id_mapping:
                # Only add stats if the domain exists in the vertex mapping
                website_id = domain_id_mapping[stats_entry["domain_name"]]
                website_stats[website_id] = stats_entry

    # Create a new Webgraph object
    graph = Webgraph()
    vertex_ids = set(id_domain_mapping.keys())
    count_websites = 0

    for site_id in vertex_ids:
        domain = id_domain_mapping[site_id]

        if site_id in website_stats and count_websites < n_vertices:
            stats = website_stats[site_id]
            graph.add_vertex(domain, stats)
            count_websites += 1
        else:
            if load_with_stats_only or count_websites >= n_vertices:
                del id_domain_mapping[site_id]
            else:
                graph.add_vertex(domain)
                count_websites += 1

    # Load edges (links between websites)
    with open(edges_file, "r") as file:
        for line in file:
            src_id, dst_id = map(int, line.split())
            if src_id in id_domain_mapping and dst_id in id_domain_mapping:
                # Only add edges if both vertices exist
                src_domain = id_domain_mapping[src_id]
                dst_domain = id_domain_mapping[dst_id]
                graph.add_edge(src_domain, dst_domain)

    return graph
