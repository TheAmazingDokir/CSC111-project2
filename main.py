from class_graph import Webgraph
from dataloader_pipeline import load_graph
import stats

VERTICES_FILE = "data/vertices.txt"
EDGES_FILE = "data/edges.txt"
WEBSITE_STATS_FILE = "data/website_stats.csv"


# Loading the data
webgraph = load_graph(VERTICES_FILE, EDGES_FILE, WEBSITE_STATS_FILE, load_with_stats_only=True)




# TODO: CALCULATE STATS

# global per-graph stats
# global_daily_min = g.calc_global_daily_min()
# global_daily_pageviews = g.calc_global_daily_pageviews()
# global_traffic_ratio = g.calc_global_traffic_ratio()
# global_site_links = g.calc_global_site_links()

# no more needed here since in next step, you can use the stats methods directly on vertices in a loop and update them


# TODO: MODIFY GRAPH PARAMETERS
#       1. update graph with global stats
#       2. update all vertices w/ their stats



# TODO: RENDER AND DISPLAY GRAPH
#       1.

if __name__ == '__main__':
    import python_ta
    python_ta.check_all(config={
        'extra-imports': [],  # the names (strs) of imported modules
        'allowed-io': [],  # the names (strs) of functions that call print/open/input
        'max-line-length': 120
    })
