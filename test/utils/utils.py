from vecgl.linalg import (Vec4, get_frustum_mat4, get_rotate_x_mat4,
                          get_rotate_y_mat4, get_rotate_z_mat4,
                          get_translate_mat4, homogenious_vec4_to_vec3,
                          kDefaultEps, mul_mat4)
from vecgl.model import Model
from vecgl.rendering import render


def is_in_cipping_space(p: Vec4, eps: float = kDefaultEps):
    p3 = homogenious_vec4_to_vec3(p)
    return all(-1.0 - eps <= a and a <= 1.0 + eps for a in p3)


def get_rotated_perspective_rendering(
    model: Model, ax: float, ay: float, az: float, tz: float = -3.0
):
    view_mat4 = mul_mat4(
        get_translate_mat4(0.0, 0.0, tz),
        get_rotate_x_mat4(ax),
        get_rotate_y_mat4(ay),
        get_rotate_z_mat4(az),
    )
    projection_mat4 = get_frustum_mat4(-1.0, 1.0, -1.0, 1.0, 1.0, 100.0)
    model_in_ndc = model.transform(mul_mat4(projection_mat4, view_mat4))
    # return model_in_ndc
    rendered = render(model_in_ndc)
    return rendered
