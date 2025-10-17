from typing import List, Dict, Tuple
from collections import deque
from graph_abc import Graph


class GraphAlgorithms:
    """
    A collection of algorithms operating on Graph objects.
    NOTE: all algorithms are left as TODO stubs.
    They must utilize the representation methods implemented in Graph:
      - get_adjacency_list() - MUST be used
      - get_adjacency_matrix() - not required (but can be used for exta credit)
      - get_incidence_matrix() - not required (but can be used for extra credit)
    """
    
    @staticmethod
    def bfs(graph: Graph, start: int) -> List[int]:
        """
        TODO: Breadth-First Search (BFS) starting from vertex start.

        Implementation steps:
            1) Validate start: ensure 0 <= start < graph.vertices.
               Raise IndexError if invalid.
            2) Obtain the adjacency list: adj = graph.get_adjacency_list().
               It is expected that the neighbors of each vertex are already sorted.
            3) Implement standard BFS:
               - Use a queue (FIFO).
               - Maintain a visited array/list of size n.
               - Process neighbors in ascending order.
            4) Return a list of vertices in the order they are dequeued
               (visit order).

        Args:
            graph (Graph): the graph on which the traversal is performed.
            start (int): the starting vertex.

        Returns:
            List[int]: the order in which vertices are visited by BFS.

        Hints:
            - Use deque from collections for the queue.
            - Mark vertices as visited at the time of enqueueing,
              not when dequeued — this avoids duplicates.
        """
        if not (0 <= start < graph.vertices):
            raise IndexError(f"start vertex {start} is out of range [0, {graph.vertices - 1}]")

        adj = graph.get_adjacency_list()
        visited = [False] * graph.vertices
        queue = deque([start])
        visited[start] = True
        visit_order = []

        while queue:
            u = queue.popleft()
            visit_order.append(u)

            for v, _ in adj[u]:
                if not visited[v]:
                    visited[v] = True
                    queue.append(v)

        return visit_order

    @staticmethod
    def dfs(graph: Graph, start: int) -> List[int]:
        """
        TODO: Depth-First Search (DFS) starting from vertex start.

        Implementation steps:
            1) Validate start: ensure 0 <= start < graph.vertices.
               Raise IndexError if invalid.
            2) Obtain the adjacency list: adj = graph.get_adjacency_list().
               Neighbors should already be sorted in ascending order.
            3) Implement DFS (recursive or iterative with a stack):
               - Mark the vertex as visited upon entering it.
               - Visit neighbors in ascending order.
            4) Return the list of vertices in preorder (first-time visits).

        Args:
            graph (Graph): the graph on which the traversal is performed.
            start (int): the starting vertex.

        Returns:
            List[int]: order of vertices visited by DFS.

        Hints:
            - Recursion is simpler, but watch recursion depth for large graphs.
            - In the iterative version, the order of adding neighbors to the stack
              affects determinism.
        """
        if not (0 <= start < graph.vertices):
            raise IndexError(f"start vertex {start} is out of range [0, {graph.vertices - 1}]")

        adj = graph.get_adjacency_list()
        visited = [False] * graph.vertices
        visit_order = []

        def _dfs_recursive(u: int):
            visited[u] = True
            visit_order.append(u)

            for v, _ in adj[u]:
                if not visited[v]:
                    _dfs_recursive(v)

        _dfs_recursive(start)

        return visit_order

    @staticmethod
    def connected_components(graph: Graph) -> List[List[int]]:
        """
        TODO: Find connected components.

        Implementation steps:
            1) Get adjacency list: adj = graph.get_adjacency_list().
            2) If the graph is undirected:
               - Compute standard connected components.
            3) If the graph is directed:
               - Compute WEAKLY connected components (ignore edge directions).
                 You can build a temporary undirected adjacency list:
                 for each (u -> v), add both u-v and v-u.
            4) Traverse the graph (BFS or DFS) starting from unvisited vertices,
               collecting vertices of each component into a list.
            5) Sort vertices within each component in ascending order.
            6) Sort the list of components by the smallest vertex in each
               (deterministic ordering).

        Args:
            graph (Graph): the graph for which to compute connected components.

        Returns:
            List[List[int]]: list of components; each component is a sorted
            list of vertex indices.

        Hints:
            - Use a shared visited array to prevent revisiting vertices.
            - For directed graphs, build a temporary dict[int, List[int]]
              with symmetric edges, then perform BFS/DFS over it.
        """
        n = graph.vertices
        visited = [False] * n
        components = []

        temp_adj: Dict[int, List[int]] = {i: [] for i in range(n)}

        adj_list = graph.get_adjacency_list()

        for u in range(n):
            for v, _ in adj_list[u]:
                if v not in temp_adj[u]:
                    temp_adj[u].append(v)

                if u not in temp_adj[v]:
                    temp_adj[v].append(u)

        for u in range(n):
            temp_adj[u].sort()


        for i in range(n):
            if not visited[i]:
                component = []
                queue = deque([i]) # Используем BFS для поиска компонента
                visited[i] = True

                while queue:
                    u = queue.popleft()
                    component.append(u)

                    for v in temp_adj[u]:
                        if not visited[v]:
                            visited[v] = True
                            queue.append(v)

                component.sort()
                components.append(component)

        components.sort(key=lambda c: c[0])
        return components


    @staticmethod
    def components_with_stats(graph: Graph) -> List[Dict[str, object]]:
        """
        TODO: Return statistics for each connected component.

        Implementation steps:
            1) Obtain components: comps = GraphAlgorithms.connected_components(graph).
            2) For each component, compute:
               - vertices: the sorted list of vertices.
               - node_count: number of vertices.
               - edge_count:
                   * For undirected graphs: count each edge once.
                     You can iterate over adj and only consider pairs (u, v)
                     where u < v.
                   * For directed graphs: count directed edges (u -> v)
                     where both endpoints are in the same component.
               - smallest_vertex: the smallest vertex (vertices[0]).
            3) Return a list of dictionaries (one per component) and SORT it by:
               (-node_count, -edge_count, smallest_vertex)
               i.e., larger components first, then those with more edges,
               then by smallest vertex ascending.

        Result element format:
            {
                "vertices": List[int],
                "node_count": int,
                "edge_count": int,
                "smallest_vertex": int
            }

        Args:
            graph (Graph): the graph for which to compute component statistics.

        Returns:
            List[Dict[str, object]]: sorted list of component statistics.

        Hints:
            - Build a vertex -> component_index mapping for quick lookup.
            - For undirected graphs, use u < v (or a set of pairs) to avoid
              double-counting edges.
        """

        comps = GraphAlgorithms.connected_components(graph)
        stats_list = []
        adj = graph.get_adjacency_list()

        comp_sets = [set(c) for c in comps]

        for component_vertices in comps:
            node_count = len(component_vertices)
            smallest_vertex = component_vertices[0]
            edge_count = 0
            comp_set = set(component_vertices)

            if graph.directed:
                for u in component_vertices:
                    for v, _ in adj[u]:
                        if v in comp_set:
                            edge_count += 1
            else:
                for u in component_vertices:
                    for v, _ in adj[u]:
                        if u < v and v in comp_set:
                            edge_count += 1

            stats = {
                "vertices": component_vertices,
                "node_count": node_count,
                "edge_count": edge_count,
                "smallest_vertex": smallest_vertex
            }
            stats_list.append(stats)

        # Сортировка по (-node_count, -edge_count, smallest_vertex)
        stats_list.sort(key=lambda s: (-s["node_count"], -s["edge_count"], s["smallest_vertex"]))

        return stats_list
