from collections import defaultdict
from math import pi
from random import uniform
from typing import (Any, Callable, Dict, Iterable, Iterator, Optional, Set,
                    Tuple)

from vecgl.linalg import (Vec4, get_frustum_mat4, get_rotate_x_mat4,
                          get_rotate_y_mat4, get_rotate_z_mat4,
                          get_translate_mat4, homogenious_vec4_to_vec3,
                          homogenious_vec4_to_xy_vec2, mul_mat4)
from vecgl.model import Model
from vecgl.modellib import (get_cube_model, get_square_model,
                            get_tetrahedron_model)
from vecgl.rendering import kDefaultEps, render


def _get_random_vec3(a: float = -2.0, b: float = 2.0):
    return tuple(uniform(a, b) for _ in range(3))


def _get_random_angle() -> float:
    return uniform(0, 2 * pi)


def _is_in_cipping_space(p: Vec4, eps: float = kDefaultEps):
    p3 = homogenious_vec4_to_vec3(p)
    return all(-1.0 - eps <= a and a <= 1.0 + eps for a in p3)


def test_render_random_points():
    model = Model()
    n = 256
    for _ in range(n):
        p = _get_random_vec3()
        model.add_point(p)
    rendered = render(model)
    assert len(rendered.points) <= n
    for pt in rendered.points:
        assert _is_in_cipping_space(pt.p)


def test_render_random_lines():
    model = Model()
    n = 256
    for _ in range(n):
        p = _get_random_vec3()
        q = _get_random_vec3()
        model.add_line(p, q)
    rendered = render(model)
    assert len(rendered.points) <= n
    for ln in rendered.lines:
        assert _is_in_cipping_space(ln.p)
        assert _is_in_cipping_space(ln.q)


Graph = Dict[Any, Set[Any]]


def _get_xy_graph(rendered: Model) -> Graph:
    graph: Graph = defaultdict(set)
    for ln in rendered.lines:
        p = homogenious_vec4_to_xy_vec2(ln.p)
        q = homogenious_vec4_to_xy_vec2(ln.q)
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


def _is_isomorph_graph_perm(graph: Graph, nodes: Tuple[Any], idxs: Dict[Any,
                                                                        int],
                            other_graph: Graph, other_nodes: Tuple[Any],
                            other_idxs: Dict[Any, int], perm: Tuple[int]):

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
        _is_isomorph_graph_perm(graph, nodes, idxs, other_graph, other_nodes,
                                other_idxs, perm)
        for perm in _get_permutations(n))


def _get_graph_from_tuples(tuples: Iterable[Tuple[Any, Any]]) -> Graph:
    graph: Graph = defaultdict(set)
    for p, q in tuples:
        graph[p].add(q)
        graph[q].add(p)
    return graph


def _get_rotated_and_rendered_model(model: Model, ax: float, ay: float,
                                    az: float):
    view_mat4 = mul_mat4(get_translate_mat4(0.0, 0.0, -3.0),
                         get_rotate_x_mat4(ax), get_rotate_y_mat4(ay),
                         get_rotate_z_mat4(az))
    projection_mat4 = get_frustum_mat4(-1.0, 1.0, -1.0, 1.0, 1.0, 100.0)
    model_in_ndc = model.transform(mul_mat4(projection_mat4, view_mat4))
    rendered = render(model_in_ndc)
    return rendered


def _assert_rotated_and_rendered_model(rendered: Model,
                                       expected_graphs: Iterable[Graph],
                                       msg: Optional[str] = None):
    actual_graph = _get_xy_graph(rendered)
    assert any(_is_isomorph_graph(actual_graph, g) for g in expected_graphs)


def get_rotated_and_rendered_cube_model(ax: float, ay: float, az: float):
    return _get_rotated_and_rendered_model(get_cube_model(), ax, ay, az)


def _get_expected_cube_graph_4() -> Graph:
    #
    #   p ----- q
    #   |       |
    #   |       |
    #   s ----- r
    #
    p, q, r, s = 0, 1, 2, 3
    tuples = [(p, q), (q, r), (r, s), (s, p)]
    return _get_graph_from_tuples(tuples)


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
    return _get_graph_from_tuples(tuples)


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
    return _get_graph_from_tuples(tuples)


def assert_rotated_and_rendered_cube_model(rendered: Model,
                                           msg: Optional[str] = None):
    expected_graphs = [
        _get_expected_cube_graph_4(),
        _get_expected_cube_graph_6(),
        _get_expected_cube_graph_7(),
    ]
    _assert_rotated_and_rendered_model(rendered, expected_graphs, msg)


def _test_rotated_and_rendered_model(
        model_generator_fn: Callable[[float, float, float], Model],
        assertion_fn: Callable[[Model, str], None],
        n: int = 512):
    for _ in range(n):
        ax, ay, az = _get_random_angle(), _get_random_angle(
        ), _get_random_angle()
        rendered = model_generator_fn(ax, ay, az)
        msg = f"ax, ay, az = {ax}, {ay}, {az}"
        assertion_fn(rendered, msg)


def test_rotated_and_rendered_cube_model():
    _test_rotated_and_rendered_model(get_rotated_and_rendered_cube_model,
                                     assert_rotated_and_rendered_cube_model)


def get_rotated_and_rendered_square_model(ax: float, ay: float, az: float):
    square = get_square_model()
    view_mat4 = mul_mat4(get_translate_mat4(0.0, 0.0, -3.0),
                         get_rotate_x_mat4(ax), get_rotate_y_mat4(ay),
                         get_rotate_z_mat4(az))
    projection_mat4 = get_frustum_mat4(-1.0, 1.0, -1.0, 1.0, 1.0, 100.0)
    square_in_ndc = square.transform(mul_mat4(projection_mat4, view_mat4))
    rendered = render(square_in_ndc)
    return rendered


def _get_expected_square_graph() -> Graph:
    #
    #   p ----- q
    #   |       |
    #   |       |
    #   s ----- r
    #
    p, q, r, s = 0, 1, 2, 3
    tuples = [(p, q), (q, r), (r, s), (s, p)]
    return _get_graph_from_tuples(tuples)


def assert_rotated_and_rendered_square_model(rendered: Model,
                                             msg: Optional[str] = None):
    expected_graphs = [
        _get_expected_square_graph(),
    ]
    _assert_rotated_and_rendered_model(rendered, expected_graphs, msg)


def test_rotated_and_rendered_square_model():
    _test_rotated_and_rendered_model(get_rotated_and_rendered_square_model,
                                     assert_rotated_and_rendered_square_model)


def get_rotated_and_rendered_tetrahedron_model(ax: float, ay: float,
                                               az: float):
    tetrahedron = get_tetrahedron_model()
    view_mat4 = mul_mat4(get_translate_mat4(0.0, 0.0, -3.0),
                         get_rotate_x_mat4(ax), get_rotate_y_mat4(ay),
                         get_rotate_z_mat4(az))
    projection_mat4 = get_frustum_mat4(-1.0, 1.0, -1.0, 1.0, 1.0, 100.0)
    tetrahedron_in_ndc = tetrahedron.transform(
        mul_mat4(projection_mat4, view_mat4))
    rendered = render(tetrahedron_in_ndc)
    return rendered


def _get_expected_tetrahedron_graph_top() -> Graph:
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
    return _get_graph_from_tuples(tuples)


def _get_expected_tetrahedron_graph_bottom() -> Graph:
    #
    #   p ----- q
    #    \     /
    #     \   /
    #       r
    #
    p, q, r = 0, 1, 2
    tuples = [(p, q), (q, r), (r, p)]
    return _get_graph_from_tuples(tuples)


def _get_expected_tetrahedron_graph_side() -> Graph:
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
    return _get_graph_from_tuples(tuples)


def assert_rotated_and_rendered_tetrahedron_model(rendered: Model,
                                                  msg: Optional[str] = None):
    expected_graphs = [
        _get_expected_tetrahedron_graph_bottom(),
        _get_expected_tetrahedron_graph_top(),
        _get_expected_tetrahedron_graph_side()
    ]
    _assert_rotated_and_rendered_model(rendered, expected_graphs, msg)


def test_rotated_and_rendered_cube_tetrahedron_model():
    _test_rotated_and_rendered_model(
        get_rotated_and_rendered_tetrahedron_model,
        assert_rotated_and_rendered_tetrahedron_model)
