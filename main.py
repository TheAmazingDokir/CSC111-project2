from class_graph import Webgraph
from dataloader_pipeline import load_graph
import stats

VERTICES_FILE = "data/vertices.txt"
EDGES_FILE = "data/edges.txt"
WEBSITE_STATS_FILE = "data/website_stats.csv"

# Loading the data
webgraph = load_graph(VERTICES_FILE, EDGES_FILE, WEBSITE_STATS_FILE, load_with_stats_only=True)

# Calculating global stats
global_daily_min = stats.calc_global_daily_min(webgraph)
global_daily_pageviews = stats.calc_global_daily_pageviews(webgraph)
global_min_per_page = stats.calc_global_min_per_page(webgraph)
global_search_traffic = stats.calc_global_search_traffic(webgraph)
global_site_links = stats.calc_global_site_links(webgraph)
global_links_traffic = stats.calc_global_links_traffic(webgraph)
global_engagement_rating = stats.calc_global_engagement_rating(webgraph)

# Updating main graph with global stats
# TODO 


# Updating vertices with individual stats
stats.loader(webgraph, stats.calc_min_per_page)
stats.loader(webgraph, stats.calc_search_traffic)
stats.loader(webgraph, stats.calc_links_traffic)
stats.loader(webgraph, stats.calc_engagement_rating)
stats.loader(webgraph, stats.predict_rank)


# RENDER AND DISPLAY GRAPH
# TODO


if __name__ == '__main__':
    import python_ta
    python_ta.check_all(config={
        'extra-imports': [],  # the names (strs) of imported modules
        'allowed-io': [],  # the names (strs) of functions that call print/open/input
        'max-line-length': 120
    })
