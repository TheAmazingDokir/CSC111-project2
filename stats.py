import math as m
import numpy as np
import class_graph as clg

    # Sample stats representation:
    # Website: math.toronto.edu
    # Avg daily min: 10 (-68% global)
    # Daily pageviews per visitor: 2304 (-38% global)
    # Ratio of traffic from search: 5 (+98% global)
    # Total sites linking in: 2 (-18% global)

    # Given Data:
    # daily_min: Estimated daily minutes on site per visitor to the site.
    # daily_pageviews: Estimated daily unique pageviews per visitor on the site.
    # traffic_ratio: The ratio of all referrals that came from Search engines over the trailing month. (e.g. 0.7)
    # site_links: The total number of sites that are linked to this website.


    # Display Data:
    # daily_min: Given.
    # daily_pageviews: Given.
    # min_per_page: daily_min / daily_pageviews
    # search_traffic: daily_min * traffic_ratio
    # site_links: Given.
    # links_traffic: daily_pageviews * log(site_links + 1)
    # engagement_rating: (daily_min * daily_pageviews)^0.5 * ((min_per_page + search_traffic) / 2)^0.5 * (ln(links_traffic + 1))^0.5
    # predicted_rank: Index of website when all sorted by engagement score.


    # Global Data:
    # global_daily_min
    # global_daily_pageviews
    # ....

    # Layout of graph & vertices in class_graph.py:

    # _Vertex:
    # item: Any
    # neighbours: set[_Vertex]
    # links_in: set[_Vertex]
    # links_out: set[_Vertex]
    # stats: dict[str, Any]

    # Directed_Graph:
    # _vertices: dict[Any, _Vertex]
    # _edges: dict[tuple[Any, Any], dict[str, Any]]


def calc_min_per_page(v: clg._Vertex) -> int:
    """Calculate the estimated average minutes spent per page.
    
    Preconditions:
        - 'daily_min' and 'daily_pageviews' are in v.stats.keys()
        - v.stats['daily_pageviews'] > 0
    
    >>> v = clg._Vertex('example.com', stats={'daily_min': 10, 'daily_pageviews': 5})
    >>> calc_min_per_page(v)
    2
    """
    daily_min = v.stats["daily_min"]
    daily_pageviews = v.stats["daily_pageviews"]

    if daily_pageviews == 0:
        raise ValueError("daily_pageviews can't be zero.")

    min_per_page = daily_min / daily_pageviews
    return round(min_per_page)

def calc_search_traffic(v: clg._Vertex) -> int:
    """Calculate the estimated traffic (minutes) from visitors via search engines.
    
    Preconditions:
        - 'daily_min' and 'traffic_ratio' are in v.stats.keys()
    
    >>> v = clg._Vertex('example.com', stats={'daily_min': 10, 'traffic_ratio': 0.5})
    >>> calc_search_traffic(v)
    5
    """
    daily_min = v.stats["daily_min"]
    traffic_ratio = v.stats["traffic_ratio"]

    search_traffic = daily_min * traffic_ratio
    return round(search_traffic)

def calc_links_traffic(v: clg._Vertex) -> int:
    """Calculate the estimated traffic (minutes) from visitors via linking websites.
    
    Preconditions:
        - 'daily_pageviews' and 'site_links' are in v.stats
        - v.stats['site_links'] >= 0
    
    >>> v = clg._Vertex('example.com', stats={'daily_pageviews': 100, 'site_links': 10})
    >>> calc_links_traffic(v)
    230
    """
    daily_pageviews = v.stats["daily_pageviews"]
    site_links = v.stats["site_links"]

    links_traffic = daily_pageviews * m.log(site_links + 1)
    return round(links_traffic)

def calc_engagement_rating(v: clg._Vertex) -> int:
    """Calculate the overall success rating for a website based on various statistics.
    
    Preconditions:
        - All required stats exist in v.stats: 'daily_min', 'daily_pageviews', 'traffic_ratio', 'site_links'
        - v.stats['daily_pageviews'] > 0
        - v.stats['site_links'] >= 0
    
    >>> v = clg._Vertex('example.com', stats={'daily_min': 10, 'daily_pageviews': 5, 'traffic_ratio': 0.5, 'site_links': 10})
    >>> calc_engagement_rating(v)
    11
    """
    daily_min = v.stats["daily_min"]
    daily_pageviews = v.stats["daily_pageviews"]
    min_per_page = calc_min_per_page(v)
    search_traffic = calc_search_traffic(v)
    links_traffic = calc_links_traffic(v)

    weight1 = 0.5
    weight2 = 0.5
    weight3 = 0.4

    overall_activity = daily_min * daily_pageviews
    quality_factor = (min_per_page + search_traffic) / 2
    link_influence = np.log(links_traffic + 1)

    engagement_rating = overall_activity**weight1 * quality_factor**weight2 * link_influence**weight3
    return round(engagement_rating)

def percentify(value: int, key: callable, g: clg.Directed_Graph) -> int:
    """Returns the percentage difference between the given statistics value and the global average from the graph.
    
    Preconditions:
        - The graph `g` must contain vertices with valid 'daily_min', 'daily_pageviews', 'traffic_ratio', and 'site_links' stats.
        - The global average calculated by `key(g)` must be non-zero.
    
    >>> percentify(10, calc_global_daily_min, g)
    -68
    """
    global_avg = key(g)

    if global_avg == 0:
        return 0
    
    percent_diff = ((value - global_avg) / global_avg) * 100
    return round(percent_diff)

def calc_global_daily_min(g: clg.Directed_Graph) -> int:
    """Calculates the global average for daily minutes on site across all vertices in the graph.
    
    Preconditions:
        - Each vertex in g._vertices has 'daily_min' in its stats.
    
    >>> g = clg.Directed_Graph()
    >>> g.add_vertex('site1', {'daily_min': 10})
    >>> g.add_vertex('site2', {'daily_min': 20})
    >>> calc_global_daily_min(g)
    15
    """
    vertices = g._vertices.values()
    count = 0
    total = 0

    for v in vertices:
        total += v.stats.get("daily_min", 0)
        count += 1

    if count == 0:
        return 0

    avg = total / count
    return round(avg)


def calc_global_daily_pageviews(g: clg.Directed_Graph) -> int:
    """Calculates the global average for daily pageviews per visitor across all vertices in the graph.
    
    Preconditions:
        - Each vertex in g._vertices has 'daily_pageviews' in its stats.
    
    >>> g = clg.Directed_Graph()
    >>> g.add_vertex('site1', {'daily_pageviews': 100})
    >>> g.add_vertex('site2', {'daily_pageviews': 200})
    >>> calc_global_daily_pageviews(g)
    150
    """
    vertices = g._vertices.values()
    count = 0
    total = 0

    for v in vertices:
        total += v.stats.get("daily_pageviews", 0)
        count += 1

    if count == 0:
        return 0

    avg = total / count
    return round(avg)

def calc_global_min_per_page(g: clg.Directed_Graph) -> int:
    """Calculates the global average for minutes per page by using calc_min_per_page for each vertex.
    
    Preconditions:
        - Each vertex has 'daily_min' and 'daily_pageviews' in its stats and daily_pageviews > 0.
    
    >>> g = clg.Directed_Graph()
    >>> g.add_vertex('site1', {'daily_min': 10, 'daily_pageviews': 5})
    >>> g.add_vertex('site2', {'daily_min': 20, 'daily_pageviews': 10})
    >>> calc_global_min_per_page(g)
    2
    """
    vertices = g._vertices.values()
    count = 0
    total = 0

    for v in vertices:
        total += calc_min_per_page(v)
        count += 1

    if count == 0:
        return 0

    avg = total / count
    return round(avg)

def calc_global_search_traffic(g: clg.Directed_Graph) -> int:
    """Calculates the global average for search traffic (in minutes) across all vertices.
    
    Preconditions:
        - Each vertex has 'daily_min' and 'traffic_ratio' in its stats.
    
    >>> g = clg.Directed_Graph()
    >>> g.add_vertex('site1', {'daily_min': 10, 'traffic_ratio': 0.5})
    >>> g.add_vertex('site2', {'daily_min': 20, 'traffic_ratio': 0.3})
    >>> calc_global_search_traffic(g)
    8
    """
    vertices = g._vertices.values()
    count = 0
    total = 0

    for v in vertices:
        total += calc_search_traffic(v)
        count += 1

    if count == 0:
        return 0

    avg = total / count
    return round(avg)

def calc_global_site_links(g: clg.Directed_Graph) -> int:
    """Calculates the global average for the total number of sites linking in across all vertices.
    
    Preconditions:
        - Each vertex in g._vertices has 'site_links' in its stats.
    
    >>> g = clg.Directed_Graph()
    >>> g.add_vertex('site1', {'site_links': 10})
    >>> g.add_vertex('site2', {'site_links': 20})
    >>> calc_global_site_links(g)
    15
    """
    vertices = g._vertices.values()
    count = 0
    total = 0

    for v in vertices:
        total += v.stats.get("site_links", 0)
        count += 1

    if count == 0:
        return 0

    avg = total / count
    return round(avg)

def calc_global_links_traffic(g: clg.Directed_Graph) -> int:
    """Calculates the global average for links traffic (in minutes) across all vertices.
    
    Preconditions:
        - Each vertex has 'daily_pageviews' and 'site_links' in its stats.
    
    >>> g = clg.Directed_Graph()
    >>> g.add_vertex('site1', {'daily_pageviews': 100, 'site_links': 10})
    >>> g.add_vertex('site2', {'daily_pageviews': 200, 'site_links': 20})
    >>> calc_global_links_traffic(g)
    360
    """
    vertices = g._vertices.values()
    count = 0
    total = 0

    for v in vertices:
        total += calc_links_traffic(v)
        count += 1

    if count == 0:
        return 0

    avg = total / count
    return round(avg)


def calc_global_engagement_rating(g: clg.Directed_Graph) -> int:
    """
    Calculates the global average engagement rating across all vertices in the graph.
    
    Preconditions:
        - Each vertex in g._vertices has the required stats to compute engagement rating.
    
    >>> g = clg.Directed_Graph()
    >>> g.add_vertex('site1', {'daily_min': 10, 'daily_pageviews': 5, 'traffic_ratio': 0.5, 'site_links': 10})
    >>> g.add_vertex('site2', {'daily_min': 20, 'daily_pageviews': 10, 'traffic_ratio': 0.3, 'site_links': 15})
    >>> calc_global_engagement_rating(g)
    10
    """
    vertices = g._vertices.values()
    count = 0
    total = 0

    for v in vertices:
        total += calc_engagement_rating(v)
        count += 1

    if count == 0:
        return 0

    avg = total / count
    return round(avg)

def predict_rank(g: clg.Directed_Graph, site: str) -> int:
    """Return the rank (index) of the specified vertex based on its engagement rating in the graph.
    
    Preconditions:
        - `g._vertices` must contain valid vertices with the required stats for engagement rating calculation.
        - `site` must be a valid key in `g._vertices`.
    
    >>> g = clg.Directed_Graph()
    >>> g.add_vertex('web1', {'daily_min': 10, 'daily_pageviews': 5, 'traffic_ratio': 0.5, 'site_links': 10})
    >>> g.add_vertex('web2', {'daily_min': 20, 'daily_pageviews': 10, 'traffic_ratio': 0.3, 'site_links': 15})
    >>> predict_rank(g, 'web1')
    1
    """
    # Calculate engagement ratings for all vertices
    engagement_ratings = []
    for vertex in g._vertices.values():
        engagement_ratings.append((vertex.item, calc_engagement_rating(vertex)))
    
    # Sort vertices by engagement rating (in descending order)
    sorted_ratings = sorted(engagement_ratings, key=lambda x: x[1], reverse=True)
    
    # Extract the rank of the specified site
    for index, (site_item, rating) in enumerate(sorted_ratings):
        if site_item == site:
            return index