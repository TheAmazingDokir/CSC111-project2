import networkx as nx
import matplotlib
matplotlib.use('TkAgg')
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg, NavigationToolbar2Tk
import tkinter as tk
from tkinter import ttk
import class_graph as cg

#
#   Setup for tkinter window
#
root = tk.Tk()
root.wm_title("Graph :)")
fig = plt.figure(figsize=(8,8), dpi=100)
ax = fig.add_subplot()

scale_factor = 10


#
#   Sample details for graph; g is a class_graph graph instance
#
g = cg.Directed_Graph()
g.add_vertex(1)
g.add_vertex(2)
g.add_vertex(3)
g.add_vertex(4)
g.add_vertex(5)
g.add_vertex(6)
g.add_edge(1,2)
g.add_edge(1,3)
g.add_edge(2,4)
g.add_edge(2,5)
g.add_edge(3,6)
# G is a networkx directed graph
G = g.to_networkx()

# Calculate what the G will look like
pos = nx.spring_layout(G)
nx.draw_networkx_nodes(G,pos,node_size=50*scale_factor, ax=ax)
nx.draw_networkx_edges(G,pos,width=1.0,alpha=0.5, ax=ax)
nx.draw_networkx_labels(G,pos,font_size=1.5*scale_factor,font_family='sans-serif', ax=ax)


#
#   Load the visual into a tkinter window
#
canvas = FigureCanvasTkAgg(fig, master=root)
canvas.draw()
canvas.get_tk_widget().pack()
toolbar = NavigationToolbar2Tk(canvas, root)
toolbar.update()
canvas._tkcanvas.pack()

# Quit button; ONLY THE QUIT BUTTON CLOSES THE WINDOW; HITTING THE "X" LEAVES IT RUNNING IN THE BACKGROUND!
button_quit = ttk.Button(master=root, text="Quit", command=root.quit)
button_quit.pack()
# Launch tkinter window
root.mainloop()