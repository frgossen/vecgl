from collections import defaultdict
from typing import Any, Dict, Iterable, Iterator, List, Optional, Set, Tuple

from vecgl.linalg import homogenious_vec4_to_vec3
from vecgl.model import Model

Graph = Dict[Any, Set[Any]]


def _get_line_graph(rendered: Model) -> Graph:
    graph: Graph = defaultdict(set)
    for ln in rendered.lines:
        p = homogenious_vec4_to_vec3(ln.p)
        q = homogenious_vec4_to_vec3(ln.q)
        graph[p].add(q)
        graph[q].add(p)
    return graph


def _get_permutations(n: int) -> Iterator[Tuple[int]]:
    if n == 0:
        yield tuple()
        return
    for perm in _get_permutations(n - 1):
        for i in range(n):
            yield perm[:i] + (n - 1, ) + perm[i:]


def _is_isomorph_graph_given_perm(
    graph: Graph,
    nodes: Tuple[Any],
    idxs: Dict[Any, int],
    other_graph: Graph,
    other_nodes: Tuple[Any],
    other_idxs: Dict[Any, int],
    perm: Tuple[int],
):
    # Check if the permutation respects node degrees.
    for p in nodes:
        i = idxs[p]
        other_i = perm[i]
        other_p = other_nodes[other_i]
        if len(graph[p]) != len(other_graph[other_p]):
            return False

    # Check if the permutation respects node adjacency.
    for p in nodes:
        i = idxs[p]
        other_i = perm[i]
        other_p = other_nodes[other_i]
        for q in graph[p]:
            j = idxs[q]
            other_j = perm[j]
            other_q = other_nodes[other_j]
            if other_q not in other_graph[other_p]:
                return False

    return True


def _is_isomorph_graph(graph: Graph, other_graph: Graph):
    # To be isomorphic, the graphs must have the same number of nodes.
    n = len(graph)
    if len(other_graph) != n:
        return False

    # Naively test all possible permutations.
    nodes = tuple(graph.keys())
    other_nodes = tuple(other_graph.keys())
    idxs = {nodes[i]: i for i in range(n)}
    other_idxs = {other_nodes[i]: i for i in range(n)}
    return any(
        _is_isomorph_graph_given_perm(graph, nodes, idxs, other_graph,
                                      other_nodes, other_idxs, perm)
        for perm in _get_permutations(n))


def get_graph_from_tuples(tuples: Iterable[Tuple[Any, Any]]) -> Graph:
    graph: Graph = defaultdict(set)
    for p, q in tuples:
        graph[p].add(q)
        graph[q].add(p)
    return graph


def assert_line_graph(model: Model,
                      expected_graphs: Iterable[Graph],
                      msg: Optional[str] = None):
    actual_graph = _get_line_graph(model)
    assert any(_is_isomorph_graph(actual_graph, g)
               for g in expected_graphs), msg


def _get_expected_cube_graph_4() -> Graph:
    #
    #   p ----- q
    #   |       |
    #   |       |
    #   s ----- r
    #
    p, q, r, s = 0, 1, 2, 3
    tuples = [(p, q), (q, r), (r, s), (s, p)]
    return get_graph_from_tuples(tuples)


def _get_expected_cube_graph_6() -> Graph:
    #
    #      t --- u
    #     /       \
    #    /         \
    #   p --------- q
    #    \         /
    #     \       /
    #      s --- r
    #
    p, q, r, s, t, u = 0, 1, 2, 3, 4, 5
    tuples = [(p, q), (q, r), (r, s), (s, p), (p, t), (t, u), (u, q)]
    return get_graph_from_tuples(tuples)


def _get_expected_cube_graph_7() -> Graph:
    #
    #      t ----- u
    #     /       /|
    #    /       / |
    #   p ----- q  v
    #   |       | /
    #   |       |/
    #   s ----- r
    #
    p, q, r, s, t, u, v = 0, 1, 2, 3, 4, 5, 6
    tuples = [(p, q), (q, r), (r, s), (s, p), (p, t), (t, u), (u, q), (u, v),
              (v, r)]
    return get_graph_from_tuples(tuples)


def get_expected_line_graphs_for_rendered_cube() -> List[Graph]:
    return [
        _get_expected_cube_graph_4(),
        _get_expected_cube_graph_6(),
        _get_expected_cube_graph_7(),
    ]


def _get_expected_square_graph() -> Graph:
    #
    #   p ----- q
    #   |       |
    #   |       |
    #   s ----- r
    #
    p, q, r, s = 0, 1, 2, 3
    tuples = [(p, q), (q, r), (r, s), (s, p)]
    return get_graph_from_tuples(tuples)


def get_expected_line_graphs_for_rendered_square() -> List[Graph]:
    return [_get_expected_square_graph()]


def _get_expected_tetrahedron_graph_4a() -> Graph:
    #
    #   p ----- q
    #   | \   / |
    #   |  \ /  |
    #   |   s   |
    #    \  |  /
    #     \ | /
    #       r
    #
    p, q, r, s = 0, 1, 2, 3
    tuples = [(p, q), (q, r), (r, p), (p, s), (q, s), (r, s)]
    return get_graph_from_tuples(tuples)


def _get_expected_tetrahedron_graph_3() -> Graph:
    #
    #   p ----- q
    #    \     /
    #     \   /
    #       r
    #
    p, q, r = 0, 1, 2
    tuples = [(p, q), (q, r), (r, p)]
    return get_graph_from_tuples(tuples)


def _get_expected_tetrahedron_graph_4b() -> Graph:
    #
    #       s
    #     / | \
    #    /  |  \
    #   |   |   |
    #   |   |   |
    #   |   |   |
    #   p - q - r
    #
    p, q, r, s = 0, 1, 2, 3
    tuples = [(p, q), (q, r), (p, s), (q, s), (r, s)]
    return get_graph_from_tuples(tuples)


def get_expected_line_graphs_for_rendered_tetrahedron():
    return [
        _get_expected_tetrahedron_graph_4a(),
        _get_expected_tetrahedron_graph_3(),
        _get_expected_tetrahedron_graph_4b(),
    ]
