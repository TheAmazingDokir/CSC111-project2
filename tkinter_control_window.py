import networkx as nx
import matplotlib
matplotlib.use('TkAgg')
import tkinter as tk
from tkinter import ttk
import class_graph as cg
import stats
from visual import visualize_graph_with_stats, visualize_communities
from dataloader_pipeline import load_graph
import scatter_plot_gen as spg

import requests as re
from bs4 import BeautifulSoup as bs

VERTICES_FILE = "data/vertices.txt"
EDGES_FILE = "data/edges.txt"
WEBSITE_STATS_FILE = "data/website_stats.csv"


def launch_control_panel(g: cg.Webgraph) -> None:
    """Launch control panel for the webgraph with buttons and inputs."""
    window = tk.Tk()
    window.wm_title("Graph Control Window")

    # Checkboxes for statistics
    stats_vars = {
        'Min per Page': tk.BooleanVar(),
        'Search Traffic': tk.BooleanVar(),
        'Links Traffic': tk.BooleanVar(),
        'Engagement Rating': tk.BooleanVar(),
        'Predicted Rank': tk.BooleanVar(),
        'Degree': tk.BooleanVar(),
        'In Degree': tk.BooleanVar(),
        'Out Degree': tk.BooleanVar(),
        'Neighbours Avg Popularity': tk.BooleanVar(),
        'Neighbour Largest In Degree': tk.BooleanVar(),
        'Popularity per Degree': tk.BooleanVar(),
        'Popularity per Neighbours Avg Popularity': tk.BooleanVar(),
        'Popularity per Neighbour Largest In Degree': tk.BooleanVar(),
        'Harmonic Centrality': tk.BooleanVar(),
        'PageRank': tk.BooleanVar()
    }

    for stat, var in stats_vars.items():
        chk = ttk.Checkbutton(window, text=stat, variable=var)
        chk.pack(anchor=tk.W)
        
    # Button to render scatter plots
    button_scatter_plot = ttk.Button(master=window, text="Scatter Plot", padding=10,
                                     command=lambda: spg.render_scatter(g))
    button_scatter_plot.pack(side=tk.RIGHT)

    # Button and text array for adding new websites
    button_quit = ttk.Button(master=window, text="Quit", padding=10, command=window.quit)
    button_quit.pack(side=tk.RIGHT)

    # Button to plot the graph with separate communities
    button_plot_graph = ttk.Button(master=window, text="Plot Communities", padding=10,
                                   command=lambda: plot_selected_community_graph(g, stats_vars))
    button_plot_graph.pack(side=tk.RIGHT)

    # Button to plot the graph
    button_plot_graph = ttk.Button(master=window, text="Plot Graph", padding=10,
                                   command=lambda: plot_selected_graph(g, stats_vars))
    button_plot_graph.pack(side=tk.RIGHT)

    text_add_website = tk.Text(master=window, width=50, height=1, padx=10, pady=10)
    text_add_website.pack()

    text_add_website.insert("1.0", "Insert URL here...")

    # button_add_site = ttk.Button(master=window, text="Add Website", padding=10, command=_refresh(g, url))
    # button_add_site.pack(side=tk.RIGHT)

    window.update()
    window.mainloop()


def get_selected_stats(stats_vars: dict) -> list:
    """Return a list of selected statistics based on the checkboxes."""
    selected_stats = [stat for stat, var in stats_vars.items() if var.get()]
    return selected_stats


def calculate_selected_stats(webgraph: cg.Webgraph, selected_stats: list) -> dict:
    """Return a dictionary with each domain name and its calculated statistics for all selected stats."""
    stats_functions = {
        'Min per Page': lambda _, v: stats.calc_min_per_page(v),
        'Search Traffic': lambda _, v: stats.calc_search_traffic(v),
        'Links Traffic': lambda _, v: stats.calc_links_traffic(v),
        'Engagement Rating': lambda _, v: stats.calc_engagement_rating(v),
        'Predicted Rank': lambda g, v: stats.predict_rank(g, v.domain_name),
        'Degree': lambda _, v: stats.calc_degree(v),
        'In Degree': lambda _, v: stats.calc_in_degree(v),
        'Out Degree': lambda _, v: stats.calc_out_degree(v),
        'Neighbours Avg Popularity': lambda _, v: stats.calc_neighbours_avg_popularity(v),
        'Neighbour Largest In Degree': lambda _, v: stats.calc_neighbour_largest_in_degree(v),
        'Popularity per Degree': lambda _, v: stats.calc_popularity_per_degree(v),
        'Popularity per Neighbours Avg Popularity': lambda _, v: stats.calc_popularity_per_neighbours_avg_popularity(v),
        'Popularity per Neighbour Largest In Degree':
            lambda _, v: stats.calc_popularity_per_neighbour_largest_in_degree(v),
        'Harmonic Centrality': lambda g, v: round(stats.calc_harmonic_centrality(g)[v.domain_name], 2),
        'PageRank': lambda g, v: round(stats.calc_page_rank(g)[v.domain_name], 2)
    }

    calculated_stats = {}
    for vertex in webgraph.get_vertices():
        domain_name = vertex.domain_name
        calculated_stats[domain_name] = {}
        for stat in selected_stats:
            if stat in stats_functions:
                calculated_stats[domain_name][stat] = stats_functions[stat](webgraph, vertex)

    for vertex in webgraph.get_vertices():
        domain_name = vertex.domain_name
        if domain_name in calculated_stats:
            for stat in selected_stats:
                if stat in stats_functions:
                    calculated_stats[domain_name][stat] = stats_functions[stat](webgraph, vertex)

    return calculated_stats


def plot_selected_graph(g: cg.Webgraph, stats_vars: dict) -> None:
    """Calculate selected stats and plot the graph."""
    selected_stats = get_selected_stats(stats_vars)
    stats_dict = calculate_selected_stats(g, selected_stats)
    visualize_graph_with_stats(g, stats_dict, True)


def plot_selected_community_graph(g: cg.Webgraph, stats_vars: dict) -> None:
    """Calculate selected stats and plot the graph."""
    selected_stats = get_selected_stats(stats_vars)
    stats_dict = calculate_selected_stats(g, selected_stats)
    visualize_communities(g, stats_dict)


# def _refresh(g: cg.Webgraph, url: str) -> None:
#     """Add the url's website into the graph and refresh the page."""
#     pass


# def _scrape_website(url1: str) -> list[str]:
#     """Scrape the input website for hyperlinks.
#     Return a list of urls from the input website that are present in the input graph.
#     """
#     page = bs(re.get(url1).content, "html.parser")
#     domain_names = []
#     for a in page.find_all("a", href=True):
#         link = str(a["href"])
#         if link[0:4] != "http":
#             continue

#         pos1 = link.find("//")
#         if pos1 == -1:
#             break
#         pos2 = link.find("/", pos1 + 2)
#         if pos2 == -1: break

#         if link[pos1 + 2: pos1 + 5] == "www":
#             domain_names.append(link[pos1 + 5: pos2])
#         else:
#             domain_names.append(link[pos1 + 2: pos2])

#     domains_in_graph = [website.domain_name for website in g.get_vertices()]

#     valid_links = [name for name in domain_names if name in domains_in_graph]
#     return valid_links


if __name__ == '__main__':
    import python_ta
    python_ta.check_all(config={
        'extra-imports': ['networkx', 'matplotlib', 'tkinter', 'class_graph', 'stats', 'visual',
                          'dataloader_pipeline', 'requests', 'bs4', 'scatter_plot_gen'],
        'allowed-io': [],
        'max-line-length': 120
    })
    # webgraph_ex = load_graph(VERTICES_FILE, EDGES_FILE, WEBSITE_STATS_FILE, True, 200)
    # launch_control_panel(webgraph_ex)
