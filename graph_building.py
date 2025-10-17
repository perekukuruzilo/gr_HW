from graph_abc import Graph


class UnweightedGraph(Graph):
    """Unweighted graph. Represents a graph where all edges have the same weight (1.0). 
       Can be directed or undirected.
       Inherits from the abstract base class Graph.
    """

    def __init__(self, vertices: int, directed: bool = False):
        super().__init__(vertices, directed=directed, weighted=False)

    def add_edge(self, u: int, v: int, weight: float = 1.0) -> None:
        """Add an edge u -> v with a fixed weight of 1.0 (the weight parameter is ignored).
           Used to create a connection between vertices u and v. The edge weight is always 1.0.

        Args:
            u (int): source vertex (0 <= u < vertices).
            v (int): target vertex (0 <= v < vertices).
            weight (float, optional): ignored. Defaults to 1.0.
        """
        self._check_vertex(u)
        self._check_vertex(v)
        if u == v:
            raise ValueError("self-loops are not allowed")

        # add unique edge u->v
        if (v, 1.0) not in self._adjacency_list[u]:
            self._adjacency_list[u].append((v, 1.0))

        # if the graph is undirected — add symmetric edge v->u
        if not self.directed:
            if (u, 1.0) not in self._adjacency_list[v]:
                self._adjacency_list[v].append((u, 1.0))


class WeightedGraph(Graph):
    """Weighted graph. Each edge has an explicit float weight.
       Can be directed or undirected.
       Inherits from the abstract base class Graph.
    """

    def __init__(self, vertices: int, directed: bool = False):
        super().__init__(vertices, directed=directed, weighted=True)

    def add_edge(self, u: int, v: int, weight: float = 1.0) -> None:
        """Add or update edge u -> v with the specified weight.

        Args:
            u (int): source vertex (0 <= u < vertices).
            v (int): target vertex (0 <= v < vertices).
            weight (float, optional): edge weight. Defaults to 1.0.
        """
        self._check_vertex(u)
        self._check_vertex(v)
        if u == v:
            raise ValueError("self-loops are not allowed")

        w = float(weight)

        # deterministically "update if exists, otherwise add"
        def _set_edge(src: int, dst: int, w: float):
            lst = self._adjacency_list[src]
            for i, (nbr, _) in enumerate(lst):
                if nbr == dst:
                    lst[i] = (dst, w)
                    break
            else:
                lst.append((dst, w))

        _set_edge(u, v, w)
        if not self.directed:
            _set_edge(v, u, w)
