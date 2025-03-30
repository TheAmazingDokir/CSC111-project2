import networkx as nx
import matplotlib
matplotlib.use('TkAgg')
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg, NavigationToolbar2Tk
import tkinter as tk
from tkinter import ttk
import class_graph as cg

import requests as re
from bs4 import BeautifulSoup as bs

window = tk.Tk()
window.wm_title("Graph Control Window")

text_add_website = tk.Text(master=window, width=20, height=5, padx=5, pady=5)
text_add_website.pack()


button_quit = ttk.Button(master=window, text="Quit", padding=10, command=window.quit)
button_quit.pack()

window.mainloop()