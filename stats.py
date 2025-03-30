import math as m
import numpy as np
import class_graph.py as clg

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


# Individual stats

def calc_min_per_page(v: clg._Vertex) -> int:
    """calculates the estimated average minutes spent per page. 
    TODO: include doctests
    """
    daily_min = v.stats["daily_min"]
    daily_pageviews = v.stats["daily_pageviews"]

    if daily_pageviews == 0:
        raise ValueError("daily_pageviews can't be zero.")

    min_per_page = daily_min / daily_pageviews
    return round(min_per_page)

def calc_search_traffic(v: clg._Vertex) -> int:
    """calculates the estimated traffic (minutes) brought from visitors from search engines.
    TODO: include doctests
    """
    daily_min = v.stats["daily_min"]
    traffic_ratio = v.stats["traffic_ratio"]

    search_traffic = daily_min * traffic_ratio
    return round(search_traffic)

def calc_links_traffic(v: clg._Vertex) -> int:
    """calculates the estimated traffic (minutes) brought from visitors from linking websites.
    TODO: include doctests
    """
    daily_pageviews = v.stats["daily_pageviews"]
    site_links = v.stats["site_links"]

    links_traffic = daily_pageviews * log(site_links + 1)
    return round(links_traffic)


def calc_engagement_rating(v: clg._Vertex) -> int:
    """Calculates the overall success rating for the website based on previously calculated statistics.
    TODO: include doctests
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
    link_influence = ln(links_traffic + 1)

    engagement_rating = overall_activity^weight1 * quality_factor^weight2 * link_influence^weight3
    return round(engagement_rating)

















# Global stats


def calc_global_daily_min(g: Directed_Graph) -> None:
    """Calculates the global average for daily minutes on site."""
    pass

def calc_global_daily_pageviews() -> None:
    """Calculates the global average for daily pageviews per visitor."""
    pass

def calc_global_traffic_ratio() -> None:
    """Calculates the global average for traffic ratio from search."""
    pass

def calc_global_site_links() -> None:
    """Calculates the global average for site linking in."""
    pass

    # more to be added...




