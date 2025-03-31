"""
CSC111 Project 2: Final Submission

Module Description
==================
This module contains functions for calculating website engagement metrics based on graph-based data. 
It processes various statistics such as daily minutes spent per visitor, pageviews, search traffic ratios, 
and backlinks to compute composite scores like engagement ratings and predicted rankings. 
The module also includes functionality to load these computed statistics into a graph structure for further analysis.

Copyright and Usage Information
==============================
This file is part of the CSC111 Project 2 submission. All rights reserved.
"""
import numpy as np
import class_graph as clg


def calc_min_per_page(v: clg._Website) -> int:
    """Calculate the estimated average minutes spent per page.
    
    Preconditions:
        - 'daily_min' and 'daily_pageviews' are in v.stats.keys()
        - v.stats['daily_pageviews'] > 0
    
    >>> v = clg._Website('example.com', stats={'daily_min': 10, 'daily_pageviews': 5})
    >>> calc_min_per_page(v)
    2
    """
    daily_min = v.stats["daily_min"]
    daily_pageviews = v.stats["daily_pageviews"]

    if daily_pageviews == 0:
        raise ValueError("daily_pageviews can't be zero.")

    min_per_page = daily_min / daily_pageviews
    return round(min_per_page)


def calc_search_traffic(v: clg._Website) -> int:
    """Calculate the estimated traffic contribution from visitors via search engines.
    
    Preconditions:
        - 'daily_min' and 'traffic_ratio' are in v.stats.keys()
    
    >>> v = clg._Website('example.com', stats={'daily_min': 10, 'traffic_ratio': 0.5})
    >>> calc_search_traffic(v)
    50
    """
    traffic_ratio = v.stats["traffic_ratio"]

    search_traffic = traffic_ratio * 100
    return round(search_traffic)


def calc_links_traffic(v: clg._Website) -> int:
    """Calculate the estimated traffic contribution from visitors via linking websites.
    
    Preconditions:
        - 'daily_pageviews' and 'site_links' are in v.stats
        - v.stats['site_links'] >= 0
    
    >>> v = clg._Website('example.com', stats={'daily_pageviews': 100, 'site_links': 10})
    >>> calc_links_traffic(v)
    9
    """
    daily_pageviews = v.stats["daily_pageviews"]
    site_links = v.stats["site_links"]

    links_traffic = (site_links / (site_links + daily_pageviews)) * 100
    return round(links_traffic)


def calc_engagement_rating(v: clg._Website) -> int:
    """Calculate the overall success rating for a website based on various statistics.
    
    Preconditions:
        - All required stats exist in v.stats: 'daily_min', 'daily_pageviews', 'traffic_ratio', 'site_links'
        - v.stats['daily_pageviews'] > 0
        - v.stats['site_links'] >= 0
    
    >>> v = clg._Website('example.com', stats={'daily_min': 10, 'daily_pageviews': 5, 'traffic_ratio': 0.5, 'site_links': 10})
    >>> calc_engagement_rating(v)
    74
    """
    daily_min = v.stats["daily_min"]
    daily_pageviews = v.stats["daily_pageviews"]
    min_per_page = calc_min_per_page(v)
    search_traffic = calc_search_traffic(v)
    links_traffic = calc_links_traffic(v)

    weight1 = 0.5
    weight2 = 0.5
    weight3 = 0.5

    overall_activity = daily_min * daily_pageviews
    quality_factor = (min_per_page + search_traffic) / 2
    link_influence = np.log(links_traffic + 1)

    engagement_rating = overall_activity**weight1 * quality_factor**weight2 * link_influence**weight3
    return round(engagement_rating)


def percentify(value: int, key: callable, g: clg.Webgraph) -> int:
    """Returns the percentage difference between the given statistics value and the global average from the graph.
    
    Preconditions:
        - Graph `g` contains vertices with valid 'daily_min', 'daily_pageviews', 'traffic_ratio', 'site_links' stats.
        - The global average calculated by `key(g)` must be non-zero.
    """
    global_avg = key(g)

    if global_avg == 0:
        return 0
    percent_diff = ((value - global_avg) / global_avg) * 100
    return round(percent_diff)


def calc_global_daily_min(g: clg.Webgraph) -> int:
    """Calculates the global average for daily minutes on site across all vertices in the graph.
    
    Preconditions:
        - Each vertex in g.vertices has 'daily_min' in its stats.
    
    >>> g = clg.Webgraph()
    >>> g.add_vertex('site1', {'daily_min': 10})
    >>> g.add_vertex('site2', {'daily_min': 20})
    >>> calc_global_daily_min(g)
    15
    """
    vertices = g.get_vertices()
    count = 0
    total = 0

    for v in vertices:
        total += v.stats.get("daily_min", 0)
        count += 1

    if count == 0:
        return 0

    avg = total / count
    return round(avg)


def calc_global_daily_pageviews(g: clg.Webgraph) -> int:
    """Calculates the global average for daily pageviews per visitor across all vertices in the graph.
    
    Preconditions:
        - Each vertex in g.vertices has 'daily_pageviews' in its stats.
    
    >>> g = clg.Webgraph()
    >>> g.add_vertex('site1', {'daily_pageviews': 100})
    >>> g.add_vertex('site2', {'daily_pageviews': 200})
    >>> calc_global_daily_pageviews(g)
    150
    """
    vertices = g.get_vertices()
    count = 0
    total = 0

    for v in vertices:
        total += v.stats.get("daily_pageviews", 0)
        count += 1

    if count == 0:
        return 0

    avg = total / count
    return round(avg)


def calc_global_min_per_page(g: clg.Webgraph) -> int:
    """Calculates the global average for minutes per page by using calc_min_per_page for each vertex.
    
    Preconditions:
        - Each vertex has 'daily_min' and 'daily_pageviews' in its stats and daily_pageviews > 0.
    
    >>> g = clg.Webgraph()
    >>> g.add_vertex('site1', {'daily_min': 10, 'daily_pageviews': 5})
    >>> g.add_vertex('site2', {'daily_min': 20, 'daily_pageviews': 10})
    >>> calc_global_min_per_page(g)
    2
    """
    vertices = g.get_vertices()
    count = 0
    total = 0

    for v in vertices:
        total += calc_min_per_page(v)
        count += 1

    if count == 0:
        return 0

    avg = total / count
    return round(avg)


def calc_global_search_traffic(g: clg.Webgraph) -> int:
    """Calculates the global average for search traffic across all vertices.
    
    Preconditions:
        - Each vertex has 'daily_min' and 'traffic_ratio' in its stats.
    
    >>> g = clg.Webgraph()
    >>> g.add_vertex('site1', {'daily_min': 10, 'traffic_ratio': 0.5})
    >>> g.add_vertex('site2', {'daily_min': 20, 'traffic_ratio': 0.3})
    >>> calc_global_search_traffic(g)
    40
    """
    vertices = g.get_vertices()
    count = 0
    total = 0

    for v in vertices:
        total += calc_search_traffic(v)
        count += 1

    if count == 0:
        return 0

    avg = total / count
    return round(avg)


def calc_global_site_links(g: clg.Webgraph) -> int:
    """Calculates the global average for the total number of sites linking in across all vertices.
    
    Preconditions:
        - Each vertex in g.vertices has 'site_links' in its stats.
    
    >>> g = clg.Webgraph()
    >>> g.add_vertex('site1', {'site_links': 10})
    >>> g.add_vertex('site2', {'site_links': 20})
    >>> calc_global_site_links(g)
    15
    """
    vertices = g.get_vertices()
    count = 0
    total = 0

    for v in vertices:
        total += v.stats.get("site_links", 0)
        count += 1

    if count == 0:
        return 0

    avg = total / count
    return round(avg)


def calc_global_links_traffic(g: clg.Webgraph) -> int:
    """Calculates the global average for links traffic across all vertices.
    
    Preconditions:
        - Each vertex has 'daily_pageviews' and 'site_links' in its stats.
    
    >>> g = clg.Webgraph()
    >>> g.add_vertex('site1', {'daily_pageviews': 100, 'site_links': 10})
    >>> g.add_vertex('site2', {'daily_pageviews': 200, 'site_links': 20})
    >>> calc_global_links_traffic(g)
    9
    """
    vertices = g.get_vertices()
    count = 0
    total = 0

    for v in vertices:
        total += calc_links_traffic(v)
        count += 1

    if count == 0:
        return 0

    avg = total / count
    return round(avg)


def calc_global_engagement_rating(g: clg.Webgraph) -> int:
    """
    Calculates the global average engagement rating across all vertices in the graph.
    
    Preconditions:
        - Each vertex in g.vertices has the required stats to compute engagement rating.
    
    >>> g = clg.Webgraph()
    >>> g.add_vertex('site1', {'daily_min': 10, 'daily_pageviews': 5, 'traffic_ratio': 0.5, 'site_links': 10})
    >>> g.add_vertex('site2', {'daily_min': 20, 'daily_pageviews': 10, 'traffic_ratio': 0.3, 'site_links': 15})
    >>> calc_global_engagement_rating(g)
    94
    """
    vertices = g.get_vertices()
    count = 0
    total = 0

    for v in vertices:
        total += calc_engagement_rating(v)
        count += 1

    if count == 0:
        return 0

    avg = total / count
    return round(avg)


def predict_rank(g: clg.Webgraph, site: str) -> int:
    """Return the rank (index) of the specified vertex based on its engagement rating in the graph.
    
    Preconditions:
        - `g.vertices` must contain valid vertices with the required stats for engagement rating calculation.
        - `site` must be a valid key in `g.vertices`.
    
    >>> g = clg.Webgraph()
    >>> g.add_vertex('web1', {'daily_min': 10, 'daily_pageviews': 5, 'traffic_ratio': 0.5, 'site_links': 10})
    >>> g.add_vertex('web2', {'daily_min': 20, 'daily_pageviews': 10, 'traffic_ratio': 0.3, 'site_links': 15})
    >>> predict_rank(g, 'web1')
    1
    """
    # Calculate engagement ratings for all vertices
    engagement_ratings = []
    for vertex in g.get_vertices():
        engagement_ratings.append((vertex.domain_name, calc_engagement_rating(vertex)))
    # Sort vertices by engagement rating (in descending order)
    sorted_ratings = sorted(engagement_ratings, key=lambda x: x[1], reverse=True)
    # Extract the rank of the specified site
    for index, (site_item, _) in enumerate(sorted_ratings):
        if site_item == site:
            return index
    return 0


def loader(g: clg.Webgraph, stat_func: callable) -> None:
    """Load calculated statistics into all vertices in the graph.
    
    """
    # Grab the target statistics key based on function name
    func_name = stat_func.__name__
    # Special handling for predict_rank which needs graph and web name
    if func_name == 'predict_rank':
        key = 'predicted_rank'
        for v in g.get_vertices():
            rank = stat_func(g, v.domain_name)
            v.stats[key] = rank
    else:
        # Otherwise compute and load normally
        key = func_name.replace('calc_', '', 1)
        for v in g.get_vertices():
            value = stat_func(v)
            v.stats[key] = value


if __name__ == '__main__':
    import doctest
    doctest.testmod()

    import python_ta
    python_ta.check_all(config={
        'extra-imports': ["numpy", "math", "class_graph"],
        'allowed-io': [],
        'max-line-length': 120
    })
