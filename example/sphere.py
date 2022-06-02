from math import pi

from vecgl.export import show, write_svg
from vecgl.linalg import (
    get_frustum_mat4,
    get_rotate_x_mat4,
    get_rotate_y_mat4,
    get_translate_mat4,
    mul_mat4,
)
from vecgl.model import get_sphere_model
from vecgl.rendering import render

# Get a predefined sphere model and choose nice colors.
# The sphere will span from -1.0 to 1.0 in all dimensions.
sphere = get_sphere_model(16, 32, "lightblue", "black")

# Define the view and the projection matrices.
view_mat4 = mul_mat4(
    get_translate_mat4(0.0, 0.0, -2.0),
    get_rotate_x_mat4(-0.2 * pi),
    get_rotate_y_mat4(0.15 * pi),
)
projection_mat4 = get_frustum_mat4(-1.0, 1.0, -1.0, 1.0, 1.0, 100.0)

# Transform our sphere model and bring it to the clip space.
transform_mat4 = mul_mat4(projection_mat4, view_mat4)
sphere_in_ndc = sphere.transform(transform_mat4)

# Render and display the model.
rendered = render(sphere_in_ndc)
show(rendered)
write_svg(rendered, "sphere.svg")

# You can access the vector-based rendering result through the rendered model.
for ln in rendered.lines:
    print(ln)
