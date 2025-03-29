import class_graph.py
import stats.py



g = Directed_Graph()

# TODO: LOAD DATA
#       1. 

# to one who's loading data: wanna use daily_min, daily_pageviews, traffic_ratio, site_links as the names for the existing stats in dataset for consistency? ty


# TODO: CALCULATE STATS

# global per-graph stats
global_daily_min = g.calc_global_daily_min()
global_daily_pageviews = g.calc_global_daily_pageviews()
global_traffic_ratio = g.calc_global_traffic_ratio()
global_site_links = g.calc_global_site_links()

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
