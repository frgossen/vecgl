from vecgl.linalg import (get_frustum_mat4, get_ortho_mat4,
                          homogenious_vec4_to_vec3, mul_mat4_vec4,
                          vec3_to_homogenious_vec4)


def test_frustum_mat4():
    p = 1.0, -1.0, -3.0
    expected = 1.0 / 6.0, -1.0 / 3.0, 1.0
    l, r, b, t, n, f = -2.0, 2.0, -1.0, 1.0, 1.0, 3.0
    actual = homogenious_vec4_to_vec3(
        mul_mat4_vec4(get_frustum_mat4(l, r, b, t, n, f),
                      vec3_to_homogenious_vec4(p)))
    assert expected == actual


def test_ortho_mat4():
    p = 1.0, -3.0, -2.0
    expected = 0.5, -0.75, 1.0
    l, r, b, t, n, f = -2.0, 2.0, -4.0, 4.0, -2.0, 2.0
    actual = homogenious_vec4_to_vec3(
        mul_mat4_vec4(get_ortho_mat4(l, r, b, t, n, f),
                      vec3_to_homogenious_vec4(p)))
    assert expected == actual
