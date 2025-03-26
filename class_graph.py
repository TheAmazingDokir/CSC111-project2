# GRAPH IMPLEMENTATION ADAPTED FROM EXERCISE 3

from __future__ import annotations
from typing import Any, Optional
import networkx as nx


class _Vertex:
    """A vertex (representing a website) in a graph (the web. aptly named).

    Instance Attributes:
        - item: The data stored in this vertex
        - neighbours: The vertices that are adjacent to this vertex
        - links_in: The vertices connnected to this vertex with incoming edges
        - links_out: The vertices connnected to this vertex with outgoing edges
        - engagement: The numerical engagement rating of this vertex (website)
        - display_size: The final intended display factor of this vertex (website)

    Representation Invariants:
        - self not in self.neighbours
        - all(self in u.neighbours for u in self.neighbours)
    """
    item: Any
    neighbours: set[_Vertex]
    links_in: set[_Vertex]
    links_out: set[_Vertex]
    engagement: float
    display_size: float

    def __init__(self, item: Any, neighbours: set[_Vertex]) -> None:
        """Initialize a new vertex with the given item and neighbours."""
        self.item = item
        self.neighbours = neighbours

    def check_connected(self, target_item: Any, visited: set[_Vertex]) -> bool:
        """Return whether this vertex is connected to a vertex corresponding to the target_item,
        WITHOUT using any of the vertices in visited.

        Preconditions:
            - self not in visited
        """
        if self.item == target_item:
            # Our base case: the target_item is the current vertex
            return True
        else:
            visited.add(self)         # Add self to the set of visited vertices
            for u in self.neighbours:
                if u not in visited:  # Only recurse on vertices that haven't been visited
                    if u.check_connected(target_item, visited):
                        return True

            return False

    def check_connected_path(self, target_item: Any, visited: set[_Vertex]) -> Optional[list]:
        """Return a path between self and the vertex corresponding to the target_item,
        WITHOUT using any of the vertices in visited.

        The returned list contains the ITEMS stored in the _Vertex objects, not the _Vertex
        objects themselves. The first list element is self.item, and the last is target_item.
        If there is more than one such path, any of the paths is returned.

        Return None if no such path exists (i.e., if self is not connected to a vertex with
        the target_item). Note that this is very similar to _Vertex.check_connected, except
        this method returns an Optional[list] instead of a bool.

        Preconditions:
            - self not in visited

        >>> v1 = _Vertex(1, set())
        >>> v2 = _Vertex(2, set())
        >>> v3 = _Vertex(3, set())
        >>> v4 = _Vertex(4, set())
        >>> v1.neighbours = {v2, v3}
        >>> v2.neighbours = {v4, v1}
        >>> v4.neighbours = {v2}
        >>> v3.neighbours = {v1}
        >>> v1.check_connected_path(4, set())
        [1, 2, 4]
        >>> v1.check_connected_path(4, {v2}) is None
        True
        """
        if self.item == target_item:
            return [self.item]

        for u in self.neighbours:
            if u not in visited:
                path = u.check_connected_path(target_item, visited.union({self}))
                if path is not None:
                    return [self.item] + path

        return None

    def check_connected_distance(self, target_item: Any, visited: set[_Vertex], d: int) -> bool:
        """Return whether this vertex is connected to a vertex corresponding to the target_item,
        WITHOUT using any of the vertices in visited, by a path of length <= d.

        Preconditions:
            - self not in visited
            - d >= 0

        >>> v1 = _Vertex(1, set())
        >>> v2 = _Vertex(2, set())
        >>> v3 = _Vertex(3, set())
        >>> v4 = _Vertex(4, set())
        >>> v5 = _Vertex(5, set())
        >>> v1.neighbours = {v2, v3}
        >>> v2.neighbours = {v3}
        >>> v3.neighbours = {v4}
        >>> v4.neighbours = {v5}
        >>> v1.check_connected_distance(5, set(), 3)  # Returns True: v1, v3, v4, v5
        True

        Implementation note (IMPORTANT):
            - Unlike check_connected, you should NOT mutate visited here (but instead
              create a new set that adds self, using set.union for example).
              This is less efficient, but also required to not introduce bugs.
              (Keep reading for details, but it's not required for implementing this method.)

              To see why, consider the doctest example.
              Since v1 has two neighbours (v2 and v3) stored in a set, the choice of which
              one to recurse on first is up to the Python interpreter. If we recurse on
              v2 first, then that recursive call will return False (since the path
              v1, v2, v3, v4, v5 is too long). But if we have every recursive call mutate
              visited, then when we're back to the original call v1.check_connected_distance,
              the loop will skip over v3, and fail to "find" the path v1, v3, v4, v5.

              This is subtle because this error would only happen if we make the first recursive
              call on v2---if we recurse on v3, the doctest would pass!
        """
        if d == 0:
            if self.item == target_item:
                return True
            else:
                return False
        else:
            for u in self.neighbours:
                if u not in visited:
                    if u.check_connected_distance(target_item, visited.union({self}), d - 1):
                        return True
            return False
        
    def check_directed_connected(self, target_item: Any, visited: list[_Vertex] = []) -> Optional[list[_Vertex]]:
        """Check whether self is connected to the vertex containing target_item, 
        avoiding vertices in visited; 
        i.e. whether a directed path exists from self to the target.
        Return a path (list of vertices) from self to the target if one exists, otherwise return None.
        """
        visited += [self]
        if self.item == target_item:
            return visited
        else:
            for u in self.links_out:
                if u not in visited:
                    path = u.check_directed_connected(target_item, visited)
                    if path is not None:
                        return path
            return None

class Graph:
    """A graph.

    Representation Invariants:
        - all(item == self._vertices[item].item for item in self._vertices)
    """
    # Private Instance Attributes:
    #     - _vertices:
    #         A collection of the vertices contained in this graph.
    #         Maps item to _Vertex object.
    _vertices: dict[Any, _Vertex]

    def __init__(self) -> None:
        """Initialize an empty graph (no vertices or edges)."""
        self._vertices = {}

    def add_vertex(self, item: Any) -> None:
        """Add a vertex with the given item to this graph.

        The new vertex is not adjacent to any other vertices.

        Preconditions:
            - item not in self._vertices
        """
        if item not in self._vertices:
            self._vertices[item] = _Vertex(item, set())

    def add_edge(self, item1: Any, item2: Any) -> None:
        """Add an edge between the two vertices with the given items in this graph.

        Raise a ValueError if item1 or item2 do not appear as vertices in this graph.

        Preconditions:
            - item1 != item2
        """
        if item1 in self._vertices and item2 in self._vertices:
            v1 = self._vertices[item1]
            v2 = self._vertices[item2]

            # Add the new edge
            v1.neighbours.add(v2)
            v2.neighbours.add(v1)
        else:
            # We didn't find an existing vertex for both items.
            raise ValueError

    def adjacent(self, item1: Any, item2: Any) -> bool:
        """Return whether item1 and item2 are adjacent vertices in this graph.

        Return False if item1 or item2 do not appear as vertices in this graph.
        """
        if item1 in self._vertices and item2 in self._vertices:
            v1 = self._vertices[item1]
            return any(v2.item == item2 for v2 in v1.neighbours)
        else:
            # We didn't find an existing vertex for both items.
            return False

    def connected(self, item1: Any, item2: Any) -> bool:
        """Return whether item1 and item2 are connected vertices in this graph.

        Return False if item1 or item2 do not appear as vertices in this graph.

        >>> g = Graph()
        >>> g.add_vertex(1)
        >>> g.add_vertex(2)
        >>> g.add_vertex(3)
        >>> g.add_vertex(4)
        >>> g.add_edge(1, 2)
        >>> g.add_edge(2, 3)
        >>> g.connected(1, 3)
        True
        >>> g.connected(1, 4)
        False
        """
        if item1 in self._vertices and item2 in self._vertices:
            v1 = self._vertices[item1]
            return v1.check_connected(item2, set())  # Pass in an empty "visited" set
        else:
            return False

    ############################################################################
    # Exercise 3 methods: These should work correctly after you complete Part 1
    ############################################################################
    def connected_path(self, item1: Any, item2: Any) -> Optional[list]:
        """Return a path between item1 and item2 in this graph.

        The returned list contains the ITEMS along the path.
        Return None if no such path exists, including when item1 or item2
        do not appear as vertices in this graph.
        """
        if item1 in self._vertices and item2 in self._vertices:
            v1 = self._vertices[item1]
            return v1.check_connected_path(item2, set())
        else:
            return None

    def connected_distance(self, item1: Any, item2: Any, d: int) -> bool:
        """Return whether items1 and item2 are connected by a path of length <= d.

        Return False if item1 or item2 do not appear as vertices in this graph.

        Preconditions:
            - d >= 0
        """
        if item1 in self._vertices and item2 in self._vertices:
            v1 = self._vertices[item1]
            return v1.check_connected_distance(item2, set(), d)
        else:
            return False
    
    def check_strongly_connected_path(self, item1: Any, item2: Any) -> tuple[
        Optional[list[_Vertex]], Optional[list[_Vertex]]
        ]:
        """Check whether two vertices are strongly connected; 
        i.e. whether a directed path exists from one to the other and back.
        Return both respective paths (if they exist) as a tuple of lists. 
        If one does not exist, None is returned instead of a list.
        """
        path_1 = self._vertices[item1].check_directed_connected(item2)
        path_2 = self._vertices[item2].check_directed_connected(item1)
        return (path_1, path_2)
    
    def to_networkx(self, max_vertices: int = 5000) -> nx.DiGraph:
        """Convert this graph into a networkx Graph.

        max_vertices specifies the maximum number of vertices that can appear in the graph.
        (This is necessary to limit the visualization output for large graphs.)

        Note that this method is provided for you, and you shouldn't change it.
        """
        graph_nx = nx.DiGraph()
        for v in self._vertices.values():
            graph_nx.add_node(v.item, v.links_in, v.links_out, v.engagement, v.display_size)

            for u in v.neighbours:
                if graph_nx.number_of_nodes() < max_vertices:
                    graph_nx.add_node(u.item, u.links_in, u.links_out, u.engagement, u.display_size)

                if u.item in graph_nx.nodes:
                    graph_nx.add_edge(v.item, u.item)

            if graph_nx.number_of_nodes() >= max_vertices:
                break

        return graph_nx


if __name__ == '__main__':
    # import doctest
    # doctest.testmod()

    # import python_ta
    # python_ta.check_all(config={
    #     'max-line-length': 120,
    #     'max-nested-blocks': 4
    # })
    pass