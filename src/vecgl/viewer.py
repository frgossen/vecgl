from math import isfinite, pi
from tkinter import ROUND, Canvas, Tk
from typing import Callable, Optional

from vecgl.linalg import (get_frustum_mat4, get_lrbt_from_aspect,
                          get_ortho_mat4, get_rotate_x_mat4, get_rotate_y_mat4,
                          get_translate_mat4, get_viewport_mat4,
                          homogenious_vec4_to_vec3, mul_mat4)
from vecgl.model import Model
from vecgl.rendering import render
from vecgl.transforms import get_random_sample_model

kDefaultWidth = 600
kDefaultHeight = 600
kDefaultStrokeWidth = 1


def _render_on_canvas(canvas: Canvas,
                      model_in_ndc: Model,
                      height: int,
                      width: int,
                      stroke_width: int,
                      render_fn: Optional[Callable[[Model], Model]],
                      text: Optional[str] = None):

    # Clear canvas.
    coords = 0, 0, width + 1, 0, width + 1, height + 1, 0, height + 1
    canvas.create_polygon(*coords, fill="white")

    # Render and transform to screen coordinates.
    if render_fn:
        model_in_ndc = render_fn(model_in_ndc)
    model_in_screen_coords = model_in_ndc.transform(
        get_viewport_mat4(0.0, height, width, -height))

    # Draw the triangles first so that later drawn lines and points are visible.
    for tr in model_in_screen_coords.triangles:
        px, py, _ = homogenious_vec4_to_vec3(tr.p)
        qx, qy, _ = homogenious_vec4_to_vec3(tr.q)
        rx, ry, _ = homogenious_vec4_to_vec3(tr.r)
        coords = px, py, qx, qy, rx, ry
        if all(isfinite(c) for c in coords):
            canvas.create_polygon(coords, fill=tr.color)

    # Draw the lines.
    for ln in model_in_screen_coords.lines:
        px, py, _ = homogenious_vec4_to_vec3(ln.p)
        qx, qy, _ = homogenious_vec4_to_vec3(ln.q)
        coords = px, py, qx, qy
        if all(isfinite(c) for c in coords):
            canvas.create_line(*coords,
                               width=stroke_width,
                               fill=ln.color,
                               capstyle=ROUND,
                               joinstyle=ROUND)

    # Draw the points.
    for pt in model_in_screen_coords.points:
        px, py, _ = homogenious_vec4_to_vec3(pt.p)
        coords = px, py
        if all(isfinite(c) for c in coords):
            canvas.create_line(*coords,
                               *coords,
                               width=stroke_width,
                               fill=pt.color,
                               capstyle=ROUND,
                               joinstyle=ROUND)

    # Overlay text.
    if text:
        canvas.create_text(width / 2, height - 10, text=text, fill="black")

    canvas.update()


def show(model_in_ndc: Model,
         height: int = kDefaultHeight,
         width: int = kDefaultWidth,
         stroke_width: int = kDefaultStrokeWidth,
         render_fn: Optional[Callable[[Model], Model]] = render) -> None:

    # Create a canvas.
    frame = Tk()
    frame.title("Viewer")
    canvas = Canvas(frame, bg="white", height=height, width=width)
    canvas.pack()

    # Draw and enter loop.
    _render_on_canvas(canvas, model_in_ndc, height, width, stroke_width,
                      render_fn)
    frame.mainloop()


def perspective_update_fn(fov: float = 1.0, n: float = 1.0, f: float = 100.0) -> Callable[[Model, float, float, float, float], Model]:

    def update(model: Model, aspect: float, hrotate: float, vrotate: float, zoom: float) -> Model:

        # Perspective projection.
        l, r, b, t = get_lrbt_from_aspect(aspect, a=fov * n)
        projection = get_frustum_mat4(l, r, b, t, n, f)

        # View transform.
        ax = 0.5 * pi * vrotate
        ay = -0.5 * pi * hrotate
        tz = -n - 1.1**zoom
        view = mul_mat4(get_translate_mat4(0.0, 0.0, tz),
                        get_rotate_x_mat4(ax), get_rotate_y_mat4(ay))

        return model.transform(projection, view)

    return update


def ortho_update_fn(n: float = -100.0, f: float = 100.0) -> Callable[[Model, float, float, float, float], Model]:

    def update(model: Model, aspect: float, hrotate: float, vrotate: float, zoom: float) -> Model:

        # Orthogonal projection.
        a = 1.1**zoom
        l, r, b, t = get_lrbt_from_aspect(aspect, a)
        projection = get_ortho_mat4(l, r, b, t, n, f)

        # View transform.
        ax = 0.5 * pi * vrotate
        ay = -0.5 * pi * hrotate
        view = mul_mat4(get_rotate_x_mat4(ax), get_rotate_y_mat4(ay))
        return model.transform(projection, view)

    return update


def random_sample_fn(num_points:int=512, num_lines:int=512, num_triangles:int=0) -> Callable[[Model], Model ]:
    return lambda model: get_random_sample_model(model, num_points, num_lines, num_triangles)


def show_interactively(model: Model,
                       update_fn: Callable[[Model, float, float, float, float],Model],
                       height: int = kDefaultHeight,
                       width: int = kDefaultWidth,
                       stroke_width: int = kDefaultStrokeWidth,
                       render_fn: Optional[Callable[[Model], Model]] = render,
                       sample_fn: Optional[Callable[ [Model], Model]] = random_sample_fn(),
                       hrotate: float = 0.0,
                       vrotate: float = 0.0,
                       zoom: float = 6.0) -> None:

    # Get sample model for quick rendering.
    sample_model = model 
    if sample_fn is not None: 
        sample_model = sample_fn(model)

    # Create a canvas.
    frame = Tk()
    frame.title("Interactive viewer")
    canvas = Canvas(frame, bg="white", height=height, width=width)
    canvas.pack()

    # Changes to viewing state: h/v rotation per pixel and zoom per wheel click.
    dhrotate = 2.0 / width
    dvrotate = 2.0 / height
    dzoom = 1.0

    # The last cursor position of interest.
    x0, y0 = 0, 0

    # Aspect ration to be passed to the update function.
    aspect = width / height

    def quick_update_canvas():
        nonlocal sample_model, aspect, hrotate, vrotate, zoom, canvas, height, width
        transformed_model = update_fn(sample_model, aspect, hrotate, vrotate,
                                      zoom)
        text = "Press space to render"
        _render_on_canvas(canvas, transformed_model, height, width,
                          stroke_width, render_fn, text)

    def full_update_canvas():
        nonlocal model, aspect, hrotate, vrotate, zoom, canvas, height, width
        transformed_model = update_fn(model, aspect, hrotate, vrotate, zoom)
        _render_on_canvas(canvas, transformed_model, height, width,
                          stroke_width, render_fn)

    def on_mouse_wheel_up(_):
        nonlocal zoom, dzoom
        zoom += dzoom
        quick_update_canvas()

    def on_mouse_wheel_down(_):
        nonlocal zoom, dzoom
        zoom -= dzoom
        quick_update_canvas()

    def on_mouse_button(e):
        nonlocal x0, y0
        x0, y0 = e.x, e.y
        quick_update_canvas()

    def on_mouse_button_release(_):
        quick_update_canvas()

    def on_motion(e):
        nonlocal x0, y0, hrotate, dhrotate, vrotate, dvrotate
        hrotate += (e.x - x0) * dhrotate
        vrotate = max(-1.0, min(vrotate - (e.y - y0) * dvrotate, 1.0))
        x0, y0 = e.x, e.y
        quick_update_canvas()

    def on_key(e):
        if e.char == " ":
            full_update_canvas()

    # Register event handlers.
    frame.bind("<Button-1>", on_mouse_button)
    frame.bind("<Button-4>", on_mouse_wheel_up)
    frame.bind("<Button-5>", on_mouse_wheel_down)
    frame.bind("<ButtonRelease-1>", on_mouse_button_release)
    frame.bind("<B1-Motion>", on_motion)
    frame.bind("<Key>", on_key)

    # Draw and enter loop.
    quick_update_canvas()
    frame.mainloop()
