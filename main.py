"""
CSC111 Project 2: Final Submission

Module Description
==================
This is the main execution module for the website engagement analysis system. It handles:
1. Loading graph data from multiple sources (vertices, edges, and website statistics files)
2. Calculating global engagement metrics across all websites in the graph
3. Updating individual website vertices with key performance indicators
4. Generating interactive visualizations of the web graph structure using Plotly

The module serves as the entry point for the analysis pipeline, coordinating data loading, 
statistical calculations, and visualization components.

Copyright and Usage Information
==============================
This file is part of the CSC111 Project 2 submission. All rights reserved.
"""
from class_graph import Webgraph
from dataloader_pipeline import load_graph
import stats
import plotly.graph_objects as go
import networkx as nx
import math
import plotly.express as px
import visual
import tkinter_control_window as tkw
import scatter_plot_gen as spg




# File paths
VERTICES_FILE = "data/vertices.txt"
EDGES_FILE = "data/edges.txt"
WEBSITE_STATS_FILE = "data/website_stats.csv"

# Load the data
webgraph = load_graph(VERTICES_FILE, EDGES_FILE, WEBSITE_STATS_FILE, load_with_stats_only=True)

# # Cull google.*
# for v in webgraph.get_vertices():
#     if v.domain_name.startswith("google"):
#         webgraph.remove_vertex(v.domain_name)
        

# Calculate and update webgraph's global stats
webgraph.global_stats["global_daily_min"] = stats.calc_global_daily_min(webgraph)
webgraph.global_stats["global_daily_pageviews"] = stats.calc_global_daily_pageviews(webgraph)
webgraph.global_stats["global_min_per_page"] = stats.calc_global_min_per_page(webgraph)
webgraph.global_stats["global_search_traffic"] = stats.calc_global_search_traffic(webgraph)
webgraph.global_stats["global_site_links"] = stats.calc_global_site_links(webgraph)
webgraph.global_stats["global_links_traffic"] = stats.calc_global_links_traffic(webgraph)
webgraph.global_stats["global_engagement_rating"] = stats.calc_global_engagement_rating(webgraph)

# Update vertices with individual stats
stats.loader(webgraph, stats.calc_min_per_page)
stats.loader(webgraph, stats.calc_search_traffic)
stats.loader(webgraph, stats.calc_links_traffic)
stats.loader(webgraph, stats.calc_engagement_rating)
stats.loader(webgraph, stats.predict_rank)

# RENDER AND DISPLAY GRAPH

spg.render_scatter(webgraph)

# sorted_vertex_list = sorted(webgraph.get_vertices(), key=lambda v: v.stats["engagement_rating"], reverse=False)
# for v in sorted_vertex_list:
#     print(v.domain_name, v.stats["engagement_rating"])
    


# visual.launch_web_graph(webgraph, 10000)

# tkw.launch_control_panel(webgraph, 10000)



if __name__ == '__main__':
    import python_ta
    python_ta.check_all(config={
        'extra-imports': ["class_graph", "dataloader_pipeline", "stats", "plotly.graph_objects", "networkx", "math", "plotly.express", "visual", "tkinter_control_window", "tkinter", "matplotlib", "matplotlib.pyplot", "matplotlib.backends.backend_tkagg"],  # the names (strs) of imported modules
        'allowed-io': [],  # the names (strs) of functions that call print/open/input
        'max-line-length': 120
    })
    
    pass
