from math import pi
from random import uniform

from pytest import approx

from vecgl.linalg import (angle_vec2, cwise_angle_vec2, get_frustum_mat4,
                          get_ortho_mat4, homogenious_vec4_to_vec3,
                          is_colinear_vec2, left_of_vec2, left_ortho_vec2,
                          mul_mat4_vec4, ortho_vec2, right_of_vec2,
                          right_ortho_vec2, scale_vec2,
                          vec3_to_homogenious_vec4)
from vecgl.random import get_random_vec2


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


def test_right_ortho_vec2():
    u = 0.5, 1.0
    expected = 1.0, -0.5
    actual = right_ortho_vec2(u)
    assert expected == actual


def test_left_ortho_vec2():
    u = 0.5, 1.0
    expected = -1.0, 0.5
    actual = left_ortho_vec2(u)
    assert expected == actual


def test_ortho_vec2():
    u = get_random_vec2()
    assert right_ortho_vec2(u) == ortho_vec2(u, right=True)
    assert left_ortho_vec2(u) == ortho_vec2(u, right=False)


def test_left_right_of_vec2_random_q1():
    u = 0.5, 1.0
    v = 1.0, 1.0
    assert left_of_vec2(u, v)
    assert not right_of_vec2(u, v)
    assert not left_of_vec2(v, u)
    assert right_of_vec2(v, u)


def test_left_right_of_vec2_random_q2():
    u = -0.5, 1.0
    v = -1.0, 1.0
    assert not left_of_vec2(u, v)
    assert right_of_vec2(u, v)
    assert left_of_vec2(v, u)
    assert not right_of_vec2(v, u)


def test_left_right_of_vec2_random():
    for _ in range(64):
        u, v = get_random_vec2(), get_random_vec2()
        if is_colinear_vec2(u, v):
            pass
        elif left_of_vec2(u, v):
            assert not left_of_vec2(v, u)
            assert right_of_vec2(v, u)
        elif right_of_vec2(u, v):
            assert not right_of_vec2(v, u)
            assert left_of_vec2(v, u)


def test_angle_vec2():
    u = 0.0, 1.0
    v = -1.0, 1.0
    assert angle_vec2(u, v) == approx(0.25 * pi)


def test_angle_vec2_invariant_of_length():
    for _ in range(16):
        u = get_random_vec2()
        v = get_random_vec2()
        a = uniform(0.5, 10.5)
        assert angle_vec2(u, v) == approx(
            angle_vec2(scale_vec2(a, u), scale_vec2(a, v)))


def test_cwise_angle_vec2():
    u = 0.0, 1.0
    v = -1.0, 1.0
    assert cwise_angle_vec2(u, v) == approx(-0.25 * pi)
