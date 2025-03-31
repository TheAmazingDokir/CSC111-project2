"""
CSC111 Project 2: Final Submission

Module Description
==================
This module contains functions for the graph's control panel, allowing the user to input a website
URL and add it to the graph. Links to and from the input site are scraped, added to the dataset,
and the page is refreshed.

Copyright and Usage Information
==============================
This file is part of the CSC111 Project 2 submission and Copyright (c) 2025 of Kyrylo Degtiarenko,
Samuel Joseph Iacobazzi, Arkhyp Boryshkevych, and John DiMatteo. All rights reserved.
Usage by CSC111 teaching team permitted.
"""
import tkinter as tk
from tkinter import ttk
import matplotlibimport visual

import requests as re
from bs4 import BeautifulSoup as bs
import class_graph as cg

matplotlib.use('TkAgg')


def launch_control_panel(g3: cg.Webgraph, nvertices: int) -> None:
    """Launch control panel for the webgraph with buttons and inputs.
    """
    window = tk.Tk()
    window.wm_title("Graph Control Window")

    #
    #   Button and text array for adding new websites
    #
    button_quit = ttk.Button(master=window, text="Quit", padding=10, command=window.quit)
    button_quit.pack(side=tk.RIGHT)

    text_add_website = tk.Text(master=window, width=50, height=1, padx=10, pady=10)
    text_add_website.insert("1.0", "Insert URL here...")
    text_add_website.pack()

    button_add_site = ttk.Button(master=window, text="Add Website", padding=10,
                                 command=lambda: _refresh(g3, text_add_website.get("1.0", tk.END)))
    button_add_site.pack(side=tk.RIGHT)

    window.update()
    window.mainloop()


def _refresh(g1: cg.Webgraph, url: str) -> None:
    """Add the url's website into the graph and refresh the page"""
    print(_search_data_for_links(g, url))
    visual.launch_web_graph(g, 1000)
    

def _search_data_for_links(g: cg.Webgraph, URL: str) -> tuple[list[str], list[str]]:
    """Search other websites for links towards the input website, 
    and scrape input website for links to websites in the graph.
    Return as a tuple in respective order.
    """
    connected_websites = []
    for domain in [website.domain_name for website in g2.get_vertices()]:
        if url in _scrape_website(domain):
            connected_websites.append(domain)
    return connected_websites


def _scrape_website(url1: str) -> list[str]:
    """Scrape the input website for hyperlinks to other sites. Return a list of urls from the input website.
    """
    page = bs(re.get(url1).content, "html.parser")
    domain_names = []
    for a in page.find_all("a", href=True):
        link = str(a["href"])
        if link[0:4] != "http":
            continue

        pos1 = link.find("//")
        if pos1 == -1:
            break
        pos2 = link.find("/", pos1 + 2)
        if pos2 == -1:
            break

        if link[pos1 + 2: pos1 + 5] == "www":
            domain_names.append(link[pos1 + 5: pos2])
        else:
            domain_names.append(link[pos1 + 2: pos2])

    return domain_names


g = cg.Webgraph()

    launch_control_panel(g)

    # g.add_vertex("maps.google.ca")

    # print(scrape_website(g, "https://google.com"))

g.add_vertex(item="google.com")
g.add_vertex(item="maps.google.com")
g.add_vertex(item="maps.google.ca")

    # u = g.get_vertices[0]
    # sum = 0

    # for v in g._vertices:
    #     if v == u: continue
    
    #     path = g.directed_connected(v, u)
    
    #     if path is not None:
    #         sum += sum([(stats.calc_engagement_rating(g._vertices[path[i]])*
    #                      ))])


if __name__ == '__main__':
    # import doctest
    # doctest.testmod()

    import python_ta

    python_ta.check_all(config={
        'extra-imports': ['csv', 'class_graph', 'matplotlib', 'tkinter', 'requests', 'bs4'],
        'allowed-io': ['_refresh', 'load_vertex_mappings', 'load_website_stats', 'load_edges'],
        'max-line-length': 120
    })
