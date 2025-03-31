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

    # Extract node coordinates and tooltips
    node_x, node_y, tooltips = [], [], []
    for node in G.nodes():
        x, y = pos[node]
        node_x.append(x)
        node_y.append(y)
        # tooltips.append(f"Node {node}<br>daily_min: {node_stats[node]}")

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
