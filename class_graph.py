# GRAPH IMPLEMENTATION ADAPTED FROM EXERCISE 3

from __future__ import annotations
from typing import Any, Optional
import networkx as nx

class _Website:
    """A vertex (representing a website) in a graph (the web. aptly named).

    Instance Attributes:
        - item: The data stored in this vertex
        - links_in: The vertices connnected to this vertex with incoming edges
        - links_out: The vertices connnected to this vertex with outgoing edges
        - stats: Mapping of relevant stat names to their values (e.g. engagement, display size, etc)

    Representation Invariants:
        - self not in self.links_in
        - self not in self.links_out
        - all([self in u.links_in for u in self.links_out])
        - all([self in u.links_out for u in self.links])
    """
    domain_name: str
    links_in: set[_Website]
    links_out: set[_Website]
    stats: dict[str, Any]

    def __init__(self, domain_name: str, links_in=None, links_out=None,
                 stats=None) -> None:
        """Initialize a new vertex with the given item, links_in and links_out, and stats.
        """
        if links_out is None:
            links_out = set()
        if links_in is None:
            links_in = set()
        if stats is None:
            stats = {}
        self.domain_name = domain_name
        self.links_in = links_in
        self.links_out = links_out
        self.stats = stats

    def check_connected(self, target_item: Any, visited=None) -> Optional[list]:
        """Return a path between self and the vertex corresponding to the target_item,
        WITHOUT using any of the vertices in visited.

        The returned list contains the ITEMS stored in the _Vertex objects, not the _Vertex
        objects themselves. The first list element is self.item, and the last is target_item.
        If there is more than one such path, any of the paths is returned.

        Return None if no such path exists (i.e., if self is not connected to a vertex with
        the target_item).

        Preconditions:
            - self not in visited
        """
        if visited is None:
            visited = list()
        visited += [self.domain_name]
        if self.domain_name == target_item:
            return visited
        else:
            for u in self.links_in.union(self.links_out):
                if u.domain_name not in visited:
                    return u.check_connected(target_item, visited)
        return None

    def check_directed_connected(self, target_item: str, visited=None) -> Optional[list]:
        """Return a directed path between self and the vertex corresponding to the target_item,
        WITHOUT using any of the vertices in visited.

        The returned list contains the ITEMS stored in the _Vertex objects, not the _Vertex
        objects themselves. The first list element is self.item, and the last is target_item.
        If there is more than one such path, any of the paths is returned.

        Return None if no such directed path exists (i.e., if self is not directed connected to a vertex with
        the target_item).

        Preconditions:
            - self not in visited
            
        >>> v1 = _Website("site1")
        >>> v2 = _Website("site2")
        >>> v3 = _Website("site3")
        >>> v4 = _Website("site4")
        >>> v1.links_out.add(v2)
        >>> v2.links_out.add(v3)
        >>> v3.links_out.add(v1)
        >>> v3.links_out.add(v4)
        >>> v1.check_directed_connected("site3")
        ['site1', 'site2', 'site3']
        >>> v2.check_directed_connected("site4")
        ['site2', 'site3', 'site4']
        >>> v4.check_directed_connected("site1")
        None
        """
        if visited is None:
            visited = list()
        visited += [self.domain_name]
        if self.domain_name == target_item:
            return visited
        else:
            for u in self.links_out:
                if u not in visited:
                    return u.check_directed_connected(target_item, visited)
            return None

    # def check_connected_distance(self, target_item: str, d: int, visited=None) -> bool:
    #     """Return whether this vertex is connected to a vertex corresponding to the target_item,
    #     WITHOUT using any of the vertices in visited, by a path of length <= d.

    #     Preconditions:
    #         - self not in visited
    #         - d >= 0
    #     """
    #     if visited is None:
    #         visited = set()
    #     if d == 0:
    #         if self.domain_name == target_item:
    #             return True
    #         else:
    #             return False
    #     else:
    #         for u in self.neighbours:
    #             if u not in visited:
    #                 if u.check_connected_distance(target_item, d - 1, visited.union({self})):
    #                     return True
    #         return False

    def check_directed_connected_distance(self, target_item: Any, d: int, visited=None) -> bool:
        """Return whether this vertex is directed connected to a vertex corresponding to the target_item,
        WITHOUT using any of the vertices in visited, by a directed path of length <= d.

        Preconditions:
            - self not in visited
            - d >= 0
        """
        if visited is None:
            visited = list()
        if d == 0:
            if self.domain_name == target_item:
                return True
            else:
                return False
        else:
            for u in self.links_out:
                if u not in visited:
                    if u.check_directed_connected_distance(target_item, d - 1, visited + [self]):
                        return True
            return False

class Webgraph:
    """A directed graph that in which each vertex is a website and every edge is hyperlink from one website to another.

    Instance Attributes:
        - global_stats: Mapping of stat names to the average of their values in the graph
        (e.g. engagement, display size, etc)
        - vertices: A collection of the vertices contained in this graph. Maps item to _Vertex object.

    Representation Invariants:
        - all(item == self.vertices[item].item for item in self.vertices)
    """

    # Private Instance Attributes:
    #     - _edges:
    #           A collection of the edges contained in this graph.
    #           Maps ordered tuples of items to a dict of stats attatched to the edge
    #           between the vertices with the items.

    vertices: dict[str, _Website]
    _edges: dict[tuple[str, str], dict[str, Any]]
    global_stats: dict[str, Any]

    def __init__(self) -> None:
        """Initialize an empty graph (no vertices or edges)."""
        self.vertices = dict()
        self._edges = dict()
        self.global_stats = dict()

    def add_vertex(self, item: str, vertex_stats=None) -> None:
        """Add a vertex with the given item and stats to this graph.

        The new vertex is not adjacent to any other vertices.

        Preconditions:
            - item not in self.vertices
        """
        if vertex_stats is None:
            vertex_stats = dict()
        if item not in self.vertices:
            self.vertices[item] = _Website(item, stats=vertex_stats)

    def add_edge(self, source: str, destination: str, edge_stats: Optional[dict[str, Any]] = None) -> None:
        """Add an edge from one vertex to the other with the respective items in this graph.
        Associates a dictionary "edge_stats" with the relevant edge stats.

        Raise a ValueError if source or destination do not appear as vertices in this graph.

        Preconditions:
            - source != destination
        """
        if source in self.vertices and destination in self.vertices:
            src_v = self.vertices[source]
            dest_v = self.vertices[destination]

            # Add the new edge
            src_v.links_out.add(dest_v)
            dest_v.links_in.add(src_v)

            self._edges[(source, destination)] = edge_stats if edge_stats is not None else {}
        else:
            # We didn't find an existing vertex for both items.
            raise ValueError

    def points_to(self, item1: str, item2: str) -> bool:
        """Return whether item1 is adjacent to and points to item2.

        Return False if item1 or item2 do not appear as vertices in this graph.
        """
        if item1 in self.vertices and item2 in self.vertices:
            v1 = self.vertices[item1]
            return any(v2.domain_name == item2 for v2 in v1.links_out)
        else:
            return False

    def connected(self, item1: str, item2: str) -> Optional[list]:
        """Check whether item1 and item2 are connected vertices in this graph.
        Return a path.

        The returned list contains the ITEMS along the path.
        Return None if no such path exists, including when item1 or item2
        do not appear as vertices in this graph.

        Return None if item1 or item2 do not appear as vertices in this graph.
        """
        if item1 in self.vertices and item2 in self.vertices:
            v1 = self.vertices[item1]
            return v1.check_connected(item2)
        else:
            return None

    def directed_connected(self, item1: str, item2: str) -> Optional[list]:
        """Check whether item1 and item2 are (directed) connected vertices in this graph.
        Return a path.

        The returned list contains the ITEMS along the path.
        Return None if no such path exists, including when item1 or item2
        do not appear as vertices in this graph.

        Return False if item1 or item2 do not appear as vertices in this graph.
        """
        if item1 in self.vertices and item2 in self.vertices:
            v1 = self.vertices[item1]
            return v1.check_directed_connected(item2)
        else:
            return None

    # def connected_distance(self, item1: str, item2: str, d: int) -> bool:
    #     """Return whether items1 and item2 are connected by a path of length <= d.

    #     Return False if item1 or item2 do not appear as vertices in this graph.

    #     Preconditions:
    #         - d >= 0
    #     """
    #     if item1 in self.vertices and item2 in self.vertices:
    #         v1 = self.vertices[item1]
    #         return v1.check_connected_distance(item2, d, set())
    #     else:
    #         return False

    def strongly_connected(self, item1: str, item2: str) -> tuple[
        Optional[list[_Website]], Optional[list[_Website]]
        ]:
        """Check whether two vertices are strongly connected;
        i.e. whether a directed path exists from one to the other and back.
        Return both respective paths (if they exist) as a tuple of lists.
        If one does not exist, None is returned instead of a list.
        """
        path_1 = self.directed_connected(item1, item2)
        path_2 = self.directed_connected(item2, item1)
        return (path_1, path_2)

    def get_vertices(self) -> list[_Website]:
        # """Return a view object of the dictionary of vertex stats associated with each vertex.
        # """
        """Return a list of the vertices in this graph.
        """
        return list(self.vertices.values())

    def num_vertices(self) -> int:
        """Return the number of vertices in this graph.
        """
        return len(self.vertices)

    def get_edges(self) -> list[tuple[str, str]]:
        # """Return a view object of the dictionary of edge stats associated with each edge.
        # """
        """Return a list of the edges in this graph.
        """
        return list(self._edges.keys())

    def num_edges(self) -> int:
        """Return the number of edges in this graph.
        """
        return len(self._edges)

    def to_networkx(self, max_vertices: int = 5000) -> nx.DiGraph:
        """Convert this graph into a networkx Graph.

        max_vertices specifies the maximum number of vertices that can appear in the graph.
        (This is necessary to limit the visualization output for large graphs.)

        The stats (dict) of a DiGraph G returned by this method can be accessed with G.nodes["item"]["stat_name"]
        """
        graph_nx = nx.DiGraph()
        for v in self.vertices.values():
            graph_nx.add_node(v.domain_name, links_in=v.links_in, links_out=v.links_out, stats=v.stats)

            for (item1, item2) in self._edges:
                if item1 == v.domain_name:
                    graph_nx.add_edge(item1, item2, stats=self._edges[(item1, item2)])

            if graph_nx.number_of_nodes() >= max_vertices:
                break

        return graph_nx

    def get_website_neighbours(self, item: str) -> set:
        """Return the domain names of the neighbours (links in and out) of the vertex with the given item.
        """
        if item in self.vertices:
            return {n.domain_name for n in self.vertices[item].links_in.union(self.vertices[item].links_out)}
        else:
            return set()

if __name__ == '__main__':
    # import doctest
    # doctest.testmod()

    # import python_ta
    # python_ta.check_all(config={
    #     'max-line-length': 120,
    #     'max-nested-blocks': 4
    # })
    pass
