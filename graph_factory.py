from typing import List, Tuple, Union
from graph_building import UnweightedGraph, WeightedGraph
from graph_abc import Graph

Number = Union[int, float]


class GraphFactory:
    """
    Factory class for creating different types of graphs.
    Encapsulates the logic of constructing graph objects (weighted/unweighted,
    directed/undirected) from various data sources:
        - by number of vertices (create_unweighted / create_weighted),
        - from an adjacency matrix (from_adjacency_matrix),
        - from an edge list (from_edges).

    Notes on weighting:
        - Weighting is determined automatically for constructors "from data":
          if ALL non-zero weights are equal to 1.0 -> the graph is treated as unweighted;
          otherwise -> weighted.
        - For undirected graphs, each edge is added once (symmetry is handled
          by the add_edge methods of the corresponding graph classes).
    """

    @staticmethod
    def create_unweighted(vertices: int, directed: bool = False) -> UnweightedGraph:
        """Create an unweighted graph with a given number of vertices."""
        return UnweightedGraph(vertices, directed)

    @staticmethod
    def create_weighted(vertices: int, directed: bool = False) -> WeightedGraph:
        """Create a weighted graph with a given number of vertices."""
        return WeightedGraph(vertices, directed)

    @staticmethod
    def from_adjacency_matrix(matrix: List[List[Number]], directed: bool = False) -> Graph:
        """
        Create a graph from an adjacency matrix (provided by instructor or dataset).

        Validations:
          - The matrix must be square (n x n)
          - The diagonal must contain only 0.0 (no self-loops)
          - For an undirected graph, the matrix must be symmetric

        Weight determination:
          - If ALL non-zero elements == 1.0 -> unweighted
          - Otherwise -> weighted
        """
        if not isinstance(matrix, list) or not matrix:
            raise ValueError("matrix must be a non-empty list of lists")
        n = len(matrix)
        for row in matrix:
            if len(row) != n:
                raise ValueError("matrix must be square (n x n)")

        nonzeros: List[float] = []
        for i in range(n):
            if float(matrix[i][i]) != 0.0:
                raise ValueError("diagonal must be 0.0 (no self-loops)")
            for j in range(n):
                val = float(matrix[i][j])
                if val != 0.0:
                    nonzeros.append(val)

        if not directed:
            for i in range(n):
                for j in range(n):
                    if float(matrix[i][j]) != float(matrix[j][i]):
                        raise ValueError("undirected graph requires a symmetric matrix")

        weighted = any(val != 1.0 for val in nonzeros)
        g: Graph = WeightedGraph(n, directed) if weighted else UnweightedGraph(n, directed)

        if directed:
            for i in range(n):
                for j in range(n):
                    w = float(matrix[i][j])
                    if i != j and w != 0.0:
                        g.add_edge(i, j, w)
        else:
            # add each undirected edge only once
            for i in range(n):
                for j in range(i + 1, n):
                    w = float(matrix[i][j])
                    if w != 0.0:
                        g.add_edge(i, j, w)

        return g

    @staticmethod
    def from_edges(vertices: int, edges: List[Tuple[int, int, Number]], directed: bool = False) -> Graph:
        """
        Create a graph from an edge list (u, v, w).

        Weight determination:
            - If ALL edge weights w in the list are 1.0 -> creates UnweightedGraph.
            - Otherwise -> creates WeightedGraph.

        Rules and validations:
            - Vertex indices must be within [0, vertices-1].
            - Self-loops are not allowed (u != v).
            - For undirected graphs, the symmetric edge will be added automatically
              inside the add_edge method of the corresponding graph class.

        Args:
            vertices (int): Number of vertices (>= 0). Vertices are numbered 0..vertices-1.
            edges (List[Tuple[int, int, Number]]): List of edges in format (u, v, w),
                where u is the source vertex, v is the target vertex, and w is the weight (int/float).
            directed (bool, optional): True — directed graph; False — undirected graph.
                Defaults to False.

        Returns:
            Graph: An instance of UnweightedGraph or WeightedGraph (depending on weights),
            with all edges from the list added.

        Raises:
            ValueError:
                - If vertices < 0.
                - If edges is None.
                - If a self-loop is detected (u == v).
            IndexError:
                - If vertex u or v is out of range [0, vertices-1].
        """
        if vertices < 0:
            raise ValueError("vertices must be non-negative")
        if edges is None:
            raise ValueError("edges must be a list of (u, v, w)")

        weighted = any(float(w) != 1.0 for _, _, w in edges) if edges else False
        g: Graph = WeightedGraph(vertices, directed) if weighted else UnweightedGraph(vertices, directed)

        for (u, v, w) in edges:
            if not (0 <= u < vertices) or not (0 <= v < vertices):
                raise IndexError(f"edge ({u}, {v}) is out of vertex range [0, {vertices-1}]")
            if u == v:
                raise ValueError("self-loops are not allowed")
            g.add_edge(u, v, float(w))

        return g
