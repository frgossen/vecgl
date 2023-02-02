from math import pi

from vecgl.export import write_svg
from vecgl.linalg import (get_frustum_mat4,   get_rotate_x_mat4,
                          get_rotate_y_mat4, get_translate_mat4, mul_mat4)
from vecgl.modellib import get_cube_model
from vecgl.rendering import render
from vecgl.viewer import perspective_update_fn, show, show_interactively

# Get a predefined cube model and choose nice colors.
# The cube will span from -1.0 to 1.0 in all dimensions.
cube = get_cube_model("lightblue", "black")

# Look at the model interactively.
show_interactively(cube, perspective_update_fn())

# Define the view and the projection matrices.
view_mat4 = mul_mat4(
    get_translate_mat4(0.0, 0.0, -3.0),
    get_rotate_x_mat4(-0.2 * pi),
    get_rotate_y_mat4(0.15 * pi),
)
projection_mat4 = get_frustum_mat4(-1.0, 1.0, -1.0, 1.0, 1.0, 100.0)

# Transform our cube model and bring it to the clip space.
transform_mat4 = mul_mat4(projection_mat4, view_mat4)
cube_in_ndc = cube.transform(transform_mat4)

# Render, display, and export the model.
rendered = render(cube_in_ndc)
show(rendered)
write_svg(rendered, "cube.svg")

# You can access the vector-based rendering result through the rendered model.
for ln in rendered.lines:
    print(ln)
