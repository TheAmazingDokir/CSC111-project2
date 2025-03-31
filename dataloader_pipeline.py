"""
CSC111 Project 2: Final Submission

Module Description
==================
This module contains functions for loading web graph data from multiple file sources into a
graph structure. It processes:
1. Vertex mappings from ID to domain names
2. Website statistics from CSV files
3. Directed edge connections between websites
4. Optional filtering for statistics-complete websites
5. Size-limited graph loading capabilities

The module serves as the data ingestion component of the web analysis system, coordinating
multiple data sources into a unified graph representation.

Copyright and Usage Information
==============================
This file is part of the CSC111 Project 2 submission and Copyright (c) 2025 of Kyrylo Degtiarenko,
Samuel Joseph Iacobazzi, Arkhyp Boryshkevych, and John DiMatteo. All rights reserved.
Usage by CSC111 teaching team permitted.
"""

import csv
from class_graph import Webgraph

WEBSITES_TO_EXCLUDE = ["xhamster3.com"]

def load_graph(vertices_file: str, edges_file: str, website_stats_file: str, load_with_stats_only: bool = False,
               n_vertices: int = 10000) -> Webgraph:
    """
    Load a web graph from the given files.

    Arguments:
        - vertices_file: The path to the file containing the vertices information.
        - edges_file: The path to the file containing the edges information.
        - website_stats_file: The path to the file containing the website statistics.
        - load_with_stats_only: A boolean indicating whether to load only websites that have statistics.
        - n_vertices: The maximum number of vertices to load.
    """
    id_domain_mapping, domain_id_mapping = load_vertex_mappings(vertices_file)
    website_stats = load_website_stats(website_stats_file, domain_id_mapping)
    graph = Webgraph()
    add_vertices_to_graph(graph, id_domain_mapping, website_stats, load_with_stats_only, n_vertices)
    load_edges(graph, edges_file, id_domain_mapping)
    return graph


def load_vertex_mappings(vertices_file: str) -> tuple[dict[int, str], dict[str, int]]:
    """
    Load the vertex mappings from a file, returning two dictionaries: one mapping site IDs to domains,
    and another mapping domains to site IDs.
    """
    id_domain_mapping = {}
    with open(vertices_file, "r") as file:
        for line in file:
            site_id, domain = line.split()
            id_domain_mapping[int(site_id)] = domain
    domain_id_mapping = {web_domain: web_id for web_id, web_domain in id_domain_mapping.items()}
    return id_domain_mapping, domain_id_mapping


def load_website_stats(website_stats_file: str, domain_id_mapping: dict[str, int]) -> dict[int, dict]:
    """
    Load website statistics from a CSV file, returning a dictionary mapping site IDs to their statistics.
    Only includes statistics for domains present in the provided domain_id_mapping.
    """
    website_stats = {}
    with open(website_stats_file, "r") as file:
        csv_reader = csv.reader(file)
        next(csv_reader)  # Skip the header row

        for row in csv_reader:
            stats_entry = {
                "alexa_rank": int(row[0]),
                "domain_name": row[1],
                "daily_min": float(row[2]),
                "daily_pageviews": float(row[3]),
                "traffic_ratio": float(row[4]),
                "site_links": int(row[5]),
                "tranco_rank": int(row[6])
            }
            domain = stats_entry["domain_name"]
            if domain in domain_id_mapping:
                website_id = domain_id_mapping[domain]
                website_stats[website_id] = stats_entry
    return website_stats


def add_vertices_to_graph(graph: Webgraph, id_domain_mapping: dict[int, str], website_stats: dict[int, dict],
                          load_with_stats_only: bool, n_vertices: int) -> None:
    """
    Add vertices to the graph from the provided mappings and statistics, modifying id_domain_mapping in place
    by removing sites that are excluded due to load_with_stats_only or exceeding n_vertices.
    """
    vertex_ids = set(id_domain_mapping.keys())
    count_websites = 0

    for site_id in vertex_ids:
        domain = id_domain_mapping[site_id]
        if domain in WEBSITES_TO_EXCLUDE:
            del id_domain_mapping[site_id]
            continue

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


def load_edges(graph: Webgraph, edges_file: str, id_domain_mapping: dict[int, str]) -> None:
    """
    Load edges into the graph from the provided edges file, only adding edges where both endpoints exist
    in the id_domain_mapping.
    """
    with open(edges_file, "r") as file:
        for line in file:
            src_id, dst_id = map(int, line.split())
            if src_id in id_domain_mapping and dst_id in id_domain_mapping:
                src_domain = id_domain_mapping[src_id]
                dst_domain = id_domain_mapping[dst_id]
                if src_domain in WEBSITES_TO_EXCLUDE or dst_domain in WEBSITES_TO_EXCLUDE:
                    continue
                graph.add_edge(src_domain, dst_domain)


if __name__ == '__main__':
    # import doctest
    # doctest.testmod()

    import python_ta
    python_ta.check_all(config={
        'extra-imports': ['csv', 'class_graph'],
        'allowed-io': ['load_vertex_mappings', 'load_website_stats', 'load_edges'],
        'max-line-length': 120
    })
