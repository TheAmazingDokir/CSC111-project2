import networkx as nx
import matplotlib
matplotlib.use('TkAgg')
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg, NavigationToolbar2Tk
import tkinter as tk
from tkinter import ttk
import class_graph as cg
import stats

import requests as re
from bs4 import BeautifulSoup as bs

def launch_control_panel(g: cg.Webgraph) -> None:
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
    
    url = text_add_website.get("1.0", tk.END)
    
    button_add_site = ttk.Button(master=window, text="Add Website", padding=10, 
                                 command=lambda: _refresh(g, url))
    button_add_site.pack(side=tk.RIGHT)
    
    window.update()
    window.mainloop()
    
def _refresh(g: cg.Webgraph, url: str) -> None:
    """Add the url's website into the graph and refresh the page"""
    print(url)
    pass

def _search_graph(g: cg.Webgraph, URL: str) -> list[str]:
    """Search other websites for links towards the input website.
    """
    connected_websites = list()
    for url in [website.domain_name for website in g.get_vertices()]:
        if URL in 
    
    # """Scrape the input website for hyperlinks. 
    # Return a list of urls from the input website that are present in the input graph.
    # """
    # page = bs(re.get(URL).content, "html.parser")
    # domain_names = list()
    # for a in page.find_all("a", href=True):
    #     link = str(a["href"])
    #     if link[0:4] != "http": continue
        
    #     pos1 = link.find("//")
    #     if pos1 == -1: break
    #     pos2 = link.find("/", pos1 + 2)
    #     if pos2 == -1: break
        
    #     if link[pos1 + 2: pos1 + 5] == "www":
    #         domain_names.append(link[pos1 + 5: pos2])
    #     else:
    #         domain_names.append(link[pos1 + 2: pos2])
    
    # domains_in_graph = [website.domain_name for website in g.get_vertices()]
    
    # valid_links = [name for name in domain_names if name in domains_in_graph]
    # return valid_links
  
  
g = cg.Webgraph()

launch_control_panel(g)

# g.add_vertex("maps.google.ca")

# print(scrape_website(g, "https://google.com"))

g.add_vertex(domain_name="google.com")
g.add_vertex(domain_name="maps.google.com")
g.add_vertex(domain_name="maps.google.ca")

# u = g.get_vertices[0]
# sum = 0

# for v in g._vertices:
#     if v == u: continue
    
#     path = g.directed_connected(v, u)
    
#     if path is not None:
#         sum += sum([(stats.calc_engagement_rating(g._vertices[path[i]])*
#                      ))])