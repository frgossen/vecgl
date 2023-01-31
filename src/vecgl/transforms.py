from random import sample
from typing import Iterable, Iterator

from vecgl.model import Line, Model, Triangle


def _get_triangles_grid(triangles: Iterable[Triangle]) -> Iterator[Line]:
    for tr in triangles:
        yield Line(tr.p, tr.q, tr.color)
        yield Line(tr.q, tr.r, tr.color)
        yield Line(tr.r, tr.p, tr.color)


def get_grid_model(model: Model) -> Model:
    grid_model = Model()
    grid_model.points = model.points
    grid_model.lines = list(_get_triangles_grid(model.triangles)) + model.lines
    return grid_model


def get_random_sample_model(model: Model, num_points: int, num_lines: int,
                            num_triangles: int) -> Model:
    sample_model = Model()
    sample_model.points = sample(model.points,
                                 min(len(model.points), num_points))
    sample_model.lines = sample(model.lines, min(len(model.lines), num_lines))
    sample_model.triangles = sample(model.triangles,
                                    min(len(model.triangles), num_triangles))
    return sample_model
