from test.utils.graphisomorphism import (
    Graph, assert_line_graph, get_expected_line_graphs_for_rendered_cube,
    get_expected_line_graphs_for_rendered_square,
    get_expected_line_graphs_for_rendered_tetrahedron)
from test.utils.utils import (get_rotated_perspective_rendering,
                              is_in_cipping_space)
from typing import Iterable

from vecgl.model import Model
from vecgl.modellib import (get_cube_model, get_square_model,
                            get_tetrahedron_model)
from vecgl.random import get_random_angle, get_random_vec3
from vecgl.rendering import render


def test_render_random_points():
    model = Model()
    n = 256
    for _ in range(n):
        p = get_random_vec3()
        model.add_point(p)
    rendered = render(model)
    assert len(rendered.points) <= n
    for pt in rendered.points:
        assert is_in_cipping_space(pt.p)


def test_render_random_lines():
    model = Model()
    n = 256
    for _ in range(n):
        p = get_random_vec3()
        q = get_random_vec3()
        model.add_line(p, q)
    rendered = render(model)
    assert len(rendered.points) <= n
    for ln in rendered.lines:
        assert is_in_cipping_space(ln.p)
        assert is_in_cipping_space(ln.q)


def _test_rotated_perspective_rendering(model: Model,
                                        expected_line_graphs: Iterable[Graph],
                                        n: int = 512):
    for _ in range(n):
        ax, ay, az = get_random_angle(), get_random_angle(), get_random_angle()
        rendered = get_rotated_perspective_rendering(model, ax, ay, az)
        msg = f"ax, ay, az = {ax}, {ay}, {az}"
        assert_line_graph(rendered, expected_line_graphs, msg)


def test_rotated_perspective_cube_rendering():
    model = get_cube_model()
    expected_line_graphs = get_expected_line_graphs_for_rendered_cube()
    _test_rotated_perspective_rendering(model, expected_line_graphs)


def test_rotated_perspective_square_rendering():
    model = get_square_model()
    expected_line_graphs = get_expected_line_graphs_for_rendered_square()
    _test_rotated_perspective_rendering(model, expected_line_graphs)


def test_rotated_perspective_tetrahedron_rendering():
    model = get_tetrahedron_model()
    expected_line_graphs = get_expected_line_graphs_for_rendered_tetrahedron()
    _test_rotated_perspective_rendering(model, expected_line_graphs)
