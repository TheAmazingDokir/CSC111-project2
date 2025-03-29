import math as m
import numpy as np
import class_graph

# Available Info:
# Name
# Daily minutes on site
# Daily pageviews per visitor
# Ratio of traffic from search
# Total sites linking in

# Potential stats to calculate:
# Website success rating (come complex formula using previously calculated stats)
# Average time per page (w/ daily minutes on site & daily pageviews per visitor)
# Search impact factor (w/ ratio of traffic from search & total sites linking in)
# Engagement density (w/ daily min on site & daily pageviews per visitor)
# Search efficiency score (w/ daily min on site & ratio of traffic from search & daily pageviews per visitor)
# Search conversion potential (w/ ratio of traffic from search & total sites linking in)
# Search & link synergy (w/ ratio of traffic from search & total sites linking in & daily minutes on site)
# Visitor impact score (w/ daily min on site & daily pageviews per visitor & total sites linking in)





    # Layout:

    # _Vertex:
    # item: Any
    # neighbours: set[_Vertex]
    # links_in: set[_Vertex]
    # links_out: set[_Vertex]
    # stats: dict[str, Any]

    # Directed_Graph:
    # _vertices: dict[Any, _Vertex]
    # _edges: dict[tuple[Any, Any], dict[str, Any]]



class Directed_Graph:

    # Calculating global stats

    def calc_global_daily_min() -> None:
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



class _Vertex:

    # Additional stats


    # coming soon....




    # Final success rating

    def calc_success_rating() -> None:
        """Calculates the overall success rating for the website based on present statistics."""
        pass