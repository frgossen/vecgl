# VecGL

[![CI](https://github.com/frgossen/vecgl/actions/workflows/ci.yml/badge.svg)](https://github.com/frgossen/vecgl/actions/workflows/ci.yml)

__*VecGL* is a 3D rendering engine with vector output.__
It is inspired by OpenGL with the key difference that the rendering result is a
set of points, lines, and triangles - not a pixelated image. These geometric
primitives can be used to generate vector graphics or to drive
[pen plotters](https://www.generativehut.com/post/axidraw).

## Getting started

The VecGL package is available through `pip`.

```
$ python3 -m pip install vecgl
```

Let's create and render a simple model.
Here's the complete example for a sphere.

```py
from math import pi

from vecgl.export import write_svg
from vecgl.linalg import (get_frustum_mat4, get_rotate_x_mat4,
                          get_rotate_y_mat4, get_translate_mat4, mul_mat4)
from vecgl.modellib import get_sphere_model
from vecgl.rendering import render
from vecgl.viewer import show, show_interactively

# Get a predefined sphere model and choose nice colors.
# The sphere will span from -1.0 to 1.0 in all dimensions.
sphere = get_sphere_model(16, 32, "lightblue", "black")
simple_sphere = get_sphere_model(4, 8, "lightblue", "black")

# Look at the model interactively.
show_interactively(sphere, simple_model=simple_sphere)

# Define the view and the projection transforms.
view_mat4 = mul_mat4(
    get_translate_mat4(0.0, 0.0, -2.0),
    get_rotate_x_mat4(-0.2 * pi),
    get_rotate_y_mat4(0.15 * pi),
)
projection_mat4 = get_frustum_mat4(-1.0, 1.0, -1.0, 1.0, 1.0, 100.0)

# Transform our sphere model and bring it to the clip space.
transform_mat4 = mul_mat4(projection_mat4, view_mat4)
sphere_in_ndc = sphere.transform(transform_mat4)

# Render, display, and export the model.
rendered = render(sphere_in_ndc)
show(rendered)
write_svg(rendered, "sphere.svg")

# You can access the vector-based rendering result through the rendered model.
for ln in rendered.lines:
    print(ln)
```

VecGL will render and display the sphere and print the vector-based rendering
result to stdout.

![This is an image](./sphere.svg)

## Build and run tests

Clone the repository.

```
$ git clone git@github.com:frgossen/vecgl.git
$ cd vecgl
```

Create a virtual environment and activate it (recommended).

```
$ python3 -m venv .venv
$ source .venv/bin/activate
```

Install the `vecgl` package in editable mode.
This makes the package (and your changes) available when running the tests.
Also, install the development dependencies, e.g. `pytest` to run the tests.

```
$ python3 -m pip install --editable .[lint,test,release]
```

You're all set for contributing back to the project.
Run the tests with ...

```
$ python3 -m pytest --benchmark-skip
```

... and the benchmarks with ...

```sh
$ python3 -m pytest --benchmark-only
```
