import networkx as nx
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import tkinter as tk
from tkinter import ttk
import class_graph as cg

import networkx as nx
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import tkinter as tk
from tkinter import ttk
import class_graph as cg

import plotly.graph_objects as go
import networkx as nx
from dataloader_pipeline import *
import stats

def launch_web_graph(webgraph: cg.Webgraph, n_vertices: int) -> None:
    """Launch the render of the updated webgraph in the browser.
    """
    G = webgraph.to_networkx(n_vertices)

    # Node positions and stats
    pos = nx.spring_layout(G)
    # node_stats = {n: (n + 1) * 50 for n in G.nodes()}  # Sample daily_min values

    # Extract edge coordinates
    edge_x, edge_y = [], []
    for edge in G.edges():
        x0, y0 = pos[edge[0]]
        x1, y1 = pos[edge[1]]
        edge_x.extend([x0, x1, None])
        edge_y.extend([y0, y1, None])

    # Label function
    vertex_dict = {v.domain_name: v for v in webgraph.get_vertices()}

    name = lambda v: (f"Website: {v.domain_name}<br>"+
                    f"Avg Daily Min: {v.stats['daily_min']} ({stats.percentify(v.stats['daily_min'], stats.calc_global_daily_min, G)}% global)<br>"+
                    f"Daily Unique Pageviews: {v.stats['daily_pageviews']} ({stats.percentify(v.stats['daily_pageviews'], stats.calc_global_daily_pageviews, G)}% global)<br>"+
                    f"Avg Min Per Page: {v.stats['min_per_page']} ({stats.percentify(v.stats['min_per_page'], stats.calc_global_min_per_page, G)}% global)<br>"+
                    f"Search Traffic Impact: {v.stats['search_traffic']}% ({stats.percentify(v.stats['search_traffic'], stats.calc_global_search_traffic, G)}% global)<br>"+
                    f"Total Sites Linking-in: {v.stats['site_links']} ({stats.percentify(v.stats['site_links'], stats.calc_global_site_links, G)}% global)<br>"+
                    f"Links Traffic Impact: {v.stats['links_traffic']}% ({stats.percentify(v.stats['links_traffic'], stats.calc_global_links_traffic, G)}% global)<br>"+
                    f"Engagement Rating: {v.stats['engagement_rating']} ({stats.percentify(v.stats['engagement_rating'], stats.calc_global_engagement_rating, G)}% global)<br>"+
                    f"Predicted Rank: {v.stats['predicted_rank']}")
    # Extract node coordinates and tooltips
    node_x, node_y, tooltips = [], [], []
    for node in G.nodes():
        x, y = pos[node]
        node_x.append(x)
        node_y.append(y)
        tooltips.append(name(vertex_dict[node]))

    # Create edge trace
    edge_trace = go.Scatter(x=edge_x, y=edge_y, mode="lines", line=dict(width=1, color="gray"))

    # Create node trace with hover tooltips
    node_trace = go.Scatter(
        x=node_x, y=node_y, mode="markers",
        marker=dict(size=10, color="blue"),
        text=tooltips, hoverinfo="text"
    )

    # Create figure
    fig = go.Figure(data=[edge_trace, node_trace])
    fig.update_layout(title="Graph with Node Tooltips", showlegend=False, hovermode="closest")

    fig.show()
