import matplotlib.pyplot as plt
import class_graph as cg

import networkx as nx

import plotly.graph_objects as go
from dataloader_pipeline import *
import stats
import math
import random

# Create a graph with edges

VERTICES_FILE = "data/vertices.txt"
EDGES_FILE = "data/edges.txt"
WEBSITE_STATS_FILE = "data/website_stats.csv"

def visualize_graph_with_stats(webgraph: Webgraph, stats_dict, size_by_tranco_rank=False):
    """
    Visualize the graph with tooltips for selected statistics and optional vertex sizing by inverted tranco_rank.

    :param webgraph: Webgraph object
    :param stats_dict: Dictionary of statistics
    :param size_by_tranco_rank: Boolean flag to size vertices by inverted tranco_rank
    """
    g = webgraph.to_networkx(10000)
    pos = nx.kamada_kawai_layout(g)

    # Extract edge coordinates
    edge_x, edge_y = [], []
    for edge in g.edges():
        x0, y0 = pos[edge[0]]
        x1, y1 = pos[edge[1]]
        edge_x.extend([x0, x1, None])
        edge_y.extend([y0, y1, None])

    # Extract node coordinates, tooltips, and sizes
    node_x, node_y, tooltips, sizes = [], [], [], []
    for node in g.nodes():
        x, y = pos[node]
        node_x.append(x)
        node_y.append(y)

        tooltip = f"{node}<br>"
        if node in stats_dict:
            for stat_name, value in stats_dict[node].items():
                tooltip += f"{stat_name}: {value}<br>"
        tooltips.append(tooltip)

        if size_by_tranco_rank:
            rank = g.nodes[node]['stats'].get('tranco_rank', 1)
            size = math.log(100 / rank + 1) * 16 + 10  # Normalize using logs
        else:
            size = 10
        sizes.append(size)

    # Create edge trace
    edge_trace = go.Scatter(x=edge_x, y=edge_y, mode="lines", line=dict(width=1, color="gray"))

    # Create node trace with hover tooltips and sizes
    node_trace = go.Scatter(
        x=node_x, y=node_y, mode="markers",
        marker=dict(size=sizes, color="blue"),
        text=tooltips, hoverinfo="text"
    )

    # Create figure
    fig = go.Figure(data=[edge_trace, node_trace])
    fig.update_layout(title="Webgraph statistics visualization",
                      showlegend=False,
                      hovermode="closest",
                      xaxis=dict(showgrid=False, zeroline=False, showticklabels=False),
                      yaxis=dict(showgrid=False, zeroline=False, showticklabels=False),
                      )

    fig.show()


def visualize_communities(webgraph: Webgraph, stats_dict) -> None:
    """
    Visualize the WebGraph using the Louvain community detection method.
    Each community is colored differently, ranging from red for small communities to blue for large communities.
    Additionally, only 50% of the edges are displayed, for better performance.
    """
    # Build the undirected graph from WebGraph
    g = webgraph.to_networkx()

    # Compute the communities using the Louvain method
    communities = nx.community.louvain_communities(g)
    # Create a partition dictionary mapping node -> community label
    partition = {node: i for i, community in enumerate(communities) for node in community}

    # Count the size of each community and calculate average stats
    community_sizes = {}
    community_stats = {stat: {} for stat in stats_dict[next(iter(stats_dict))].keys()}
    for node, comm in partition.items():
        if comm not in community_sizes:
            community_sizes[comm] = 0
            for stat in community_stats.keys():
                community_stats[stat][comm] = 0
        community_sizes[comm] += 1
        for stat, values in stats_dict[node].items():
            community_stats[stat][comm] += values

    community_avg_stats = {stat: {k: v / community_sizes[k] for k, v in comm_stats.items()}
                           for stat, comm_stats in community_stats.items()}

    # Ensure there are multiple communities
    if len(community_sizes) < 2:
        raise ValueError("The graph must have at least two communities.")

    # Generate a color map ranging from red to blue
    cmap = plt.get_cmap('plasma')
    norm = plt.Normalize(vmin=min(community_sizes.values()), vmax=max(community_sizes.values()))
    community_colors = {comm: cmap(norm(size)) for comm, size in community_sizes.items()}

    # Prepare node colors based on community
    node_colors = [f"rgb({int(255 * community_colors[partition[node]][0])},"
                       f"{int(255 * community_colors[partition[node]][1])},"
                       f"{int(255 * community_colors[partition[node]][2])})"
                   for node in g.nodes()]

    # Generate positions using circular layout.
    pos = nx.kamada_kawai_layout(g)

    # Randomly select 50% of the edges to display
    all_edges = list(g.edges())
    random.shuffle(all_edges)
    edges_to_display = all_edges[:len(all_edges) // 2]

    # Build edge traces.
    edge_x, edge_y = [], []
    for src, dest in edges_to_display:
        x0, y0 = pos[src]
        x1, y1 = pos[dest]
        edge_x.extend([x0, x1, None])
        edge_y.extend([y0, y1, None])
    edge_trace = go.Scatter(
        x=edge_x, y=edge_y,
        line=dict(width=0.5, color='gray'),
        hoverinfo='none',
        mode='lines'
    )

    # Build node traces.
    node_x, node_y, node_text = [], [], []
    for node in g.nodes():
        x, y = pos[node]
        node_x.append(x)
        node_y.append(y)
        tooltip = f"{node}<br>Community: {partition[node]}<br>"
        for stat, comm_stats in community_avg_stats.items():
            tooltip += f"{stat}: {comm_stats[partition[node]]:.2f}<br>"
        node_text.append(tooltip)

    node_trace = go.Scatter(
        x=node_x, y=node_y,
        mode='markers',
        hoverinfo='text',
        text=node_text,
        marker=dict(
            showscale=True,
            colorscale='plasma',
            colorbar=dict(
                title='Community Size',
                titleside='right'
            ),
            color=[community_sizes[partition[node]] for node in g.nodes()],
            size=10,
            line_width=0.5
        )
    )

    # Create the figure.
    fig = go.Figure(data=[edge_trace, node_trace],
                    layout=go.Layout(
                        title='Statistics inside communities of the webgraph varing by size',
                        showlegend=False,
                        hovermode='closest',
                        xaxis=dict(showgrid=False, zeroline=False, showticklabels=False),
                        yaxis=dict(showgrid=False, zeroline=False, showticklabels=False)
                    ))
    fig.update_layout({'showlegend': False, 'width': 900, 'height': 900})
    fig.show()

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


if __name__ == "__main__":
    webgraph_ex = load_graph(VERTICES_FILE, EDGES_FILE, WEBSITE_STATS_FILE, True, 100)
    stats_dict_ex = {}
    visualize_graph_with_stats(webgraph_ex, stats_dict_ex, True)
