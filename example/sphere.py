from math import pi

from vecgl.export import write_svg
from vecgl.linalg import (get_frustum_mat4, get_rotate_x_mat4,
                          get_rotate_y_mat4, get_translate_mat4, mul_mat4)
from vecgl.modellib import get_sphere_model
from vecgl.rendering import render
from vecgl.viewer import perspective_update_fn, show, show_interactively

# Get a predefined sphere model and choose nice colors.
# The sphere will span from -1.0 to 1.0 in all dimensions.
sphere = get_sphere_model(16, 32, "lightblue", "black")

# Look at the model interactively.
show_interactively(sphere, perspective_update_fn())

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
