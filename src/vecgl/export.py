from math import isfinite
from typing import Iterator

from vecgl.linalg import Vec4, get_viewport_mat4, homogenious_vec4_to_vec3
from vecgl.model import Model
from vecgl.rendering import render

kDefaultWidth = 600
kDefaultHeight = 600
kDefaultStrokeWidth = 1


def to_svg(
    model: Model,
    height: int = kDefaultHeight,
    width: int = kDefaultWidth,
    stroke_width: int = kDefaultStrokeWidth,
) -> Iterator[str]:

    # Transform to canvas space.
    model = model.transform(get_viewport_mat4(0.0, height, width, -height))

    yield f"<svg version=\"1.1\" width=\"{width}\" height=\"{height}\" xmlns=\"http://www.w3.org/2000/svg\">\n"

    # Add the triangles.
    for tr in model.triangles:
        px, py, _ = homogenious_vec4_to_vec3(tr.p)
        qx, qy, _ = homogenious_vec4_to_vec3(tr.q)
        rx, ry, _ = homogenious_vec4_to_vec3(tr.r)
        if all(isfinite(c) for c in (px, py, qx, qy, rx, ry)):
            yield f"  <polygon points=\"{px},{py} {qx},{qy} {rx},{ry}\" fill=\"{tr.color}\"/>\n"

    # Add the lines.
    for ln in model.lines:
        px, py, _ = homogenious_vec4_to_vec3(ln.p)
        qx, qy, _ = homogenious_vec4_to_vec3(ln.q)
        if all(isfinite(c) for c in (px, py, qx, qy)):
            yield f"  <line x1=\"{px}\" y1=\"{py}\" x2=\"{qx}\" y2=\"{qy}\" stroke=\"{ln.color}\" stroke-linecap=\"round\" stroke-width=\"{stroke_width}\"/>\n"

    # Add the points.
    for pt in model.points:
        px, py, _ = homogenious_vec4_to_vec3(pt.p)
        if all(isfinite(c) for c in (px, py)):
            yield f"  <circle cx=\"{px}\" cy=\"{py}\" r=\"{stroke_width/2}\" fill=\"green\"/>\n"

    yield f"</svg>\n"


def write_svg(
    model: Model,
    path: str,
    height: int = kDefaultHeight,
    width: int = kDefaultWidth,
    stroke_width: int = kDefaultStrokeWidth,
) -> None:
    with open(path, "w") as fout:
        fout.writelines(to_svg(model, height, width, stroke_width))


def _p_to_json(p: Vec4) -> str:
    return "[ " + ", ".join(str(a) for a in p) + " ]"


def to_json(model: Model) -> Iterator[str]:
    yield "{\n"

    # Add the points.
    yield "  \"points\": [\n"
    for pt in model.points:
        is_last = pt == model.points[-1]
        yield f"    {{\n"
        yield f"      \"p\": {_p_to_json(pt.p)},\n"
        yield f"      \"color\": \"{pt.color}\"\n"
        yield f"    }}{'' if is_last else ','}\n"
    yield "  ],\n"

    # Add the lines.
    yield "  \"lines\": [\n"
    for ln in model.lines:
        is_last = ln == model.lines[-1]
        yield f"    {{\n"
        yield f"      \"p\": {_p_to_json(ln.p)},\n"
        yield f"      \"q\": {_p_to_json(ln.q)},\n"
        yield f"      \"color\": \"{ln.color}\"\n"
        yield f"    }}{'' if is_last else ','}\n"
    yield "  ],\n"

    # Add the triangles.
    yield "  \"triangles\": [\n"
    for tr in model.triangles:
        is_last = tr == model.triangles[-1]
        yield f"    {{\n"
        yield f"      \"p\": {_p_to_json(tr.p)},\n"
        yield f"      \"q\": {_p_to_json(tr.q)},\n"
        yield f"      \"r\": {_p_to_json(tr.r)},\n"
        yield f"      \"color\": \"{tr.color}\"\n"
        yield f"    }}{'' if is_last else ','}\n"
    yield "  ]\n"

    yield "}\n"


def write_json(model: Model, path: str) -> None:
    with open(path, "w") as fout:
        fout.writelines(to_json(model))


def to_python(model: Model) -> Iterator[str]:

    # Add the points.
    for pt in model.points:
        yield f"model.add_point({homogenious_vec4_to_vec3(pt.p)})\n"

    # Add the lines.
    for ln in model.lines:
        yield f"model.add_line({homogenious_vec4_to_vec3(ln.p)}, {homogenious_vec4_to_vec3(ln.q)})\n"

    # Add the triangles.
    for tr in model.triangles:
        yield f"model.add_triangle({homogenious_vec4_to_vec3(tr.p)}, {homogenious_vec4_to_vec3(tr.q)}, {homogenious_vec4_to_vec3(tr.r)})\n"


def write_python(model: Model, path: str) -> None:
    with open(path, "w") as fout:
        fout.writelines(to_python(model))
