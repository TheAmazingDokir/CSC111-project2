from class_graph import Webgraph
from dataloader_pipeline import load_graph
import stats
import plotly.graph_objects as go
import networkx as nx
import math
import plotly.express as px

# File paths
VERTICES_FILE = "data/vertices.txt"
EDGES_FILE = "data/edges.txt"
WEBSITE_STATS_FILE = "data/website_stats.csv"

# Load the data
webgraph = load_graph(VERTICES_FILE, EDGES_FILE, WEBSITE_STATS_FILE, load_with_stats_only=True)

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
#
#   DUMMY TEST BELOW
#
# for v in webgraph.get_vertices():
#     normalized_degree = math.erf(len(webgraph.get_website_neighbours()))

name = lambda v: (f"Website: {v.domain_name}<br>"+
                    f"Avg daily min: {v.stats['daily_min']}<br>"+
                    f"Daily pageviews per visitor: {v.stats['daily_pageviews']}<br>"+
                    f"Min per page: {v.stats['min_per_page']}<br>"+
                    f"Search traffic: {v.stats['search_traffic']}<br>"+
                    f"Total sites linking in: {v.stats['site_links']}<br>"+
                    f"Links traffic: {v.stats['links_traffic']}<br>"+
                    f"Engagement rating: {v.stats['engagement_rating']}<br>"+
                    f"Predicted rank: {v.stats['predicted_rank']}")

x = [len(v.links_in) for v in webgraph.get_vertices()]
y = [v.stats["engagement_rating"] for v in webgraph.get_vertices()]
fig = px.scatter(x=x ,y=y, hover_name=[name(v) for v in webgraph.get_vertices()], trendline= "ols")
fig.update_layout(xaxis_title="Number of Incoming Links", yaxis_title="Engagement Rating")
fig.show()

x = [len(v.links_in) for v in webgraph.get_vertices()]
print(len(x))
y = [v.stats["links_traffic"] for v in webgraph.get_vertices()]

fig = px.scatter(x=x, y=y, hover_name=[name(v) for v in webgraph.get_vertices()], trendline= "ols")
fig.update_layout(xaxis_title="Number of Incoming Links", yaxis_title="Links Traffic")
fig.show()

# x = [len(v.links_out) for v in webgraph.get_vertices()]
# y = [v.stats["search_traffic"] for v in webgraph.get_vertices()]
# fig = px.scatter(x=x, y=y, hover_name=[v.domain_name for v in webgraph.get_vertices()], trendline= "ols")
# fig.show()
# NO CORRELATION






G = webgraph.to_networkx(300)

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


if __name__ == '__main__':
    # import python_ta
    # python_ta.check_all(config={
    #     'extra-imports': [],  # the names (strs) of imported modules
    #     'allowed-io': [],  # the names (strs) of functions that call print/open/input
    #     'max-line-length': 120
    # })
    
    pass
