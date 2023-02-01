from math import cos, pi, sin, sqrt
from typing import List

from vecgl.linalg import Vec3
from vecgl.model import Model, kDefaultLineColor, kDefaultSurfaceColor


def get_square_model(surface_color: str = kDefaultSurfaceColor,
                     line_color: str = kDefaultLineColor,
                     surfaces: bool = True,
                     lines: bool = True) -> Model:
    square = Model()

    # Create the 4 points.
    p = -1.0, 1.0, 0.0
    q = 1.0, 1.0, 0.0
    r = 1.0, -1.0, 0.0
    s = -1.0, -1.0, 0.0

    # Add the 4 lines if needed.
    if lines:
        square.add_line(p, q, line_color)
        square.add_line(q, r, line_color)
        square.add_line(r, s, line_color)
        square.add_line(s, p, line_color)

    # Add the 2 triangles if needed.
    if surfaces:
        square.add_triangle(p, q, r, surface_color)
        square.add_triangle(r, s, p, surface_color)

    return square


def get_cube_model(
    surface_color: str = kDefaultSurfaceColor,
    line_color: str = kDefaultLineColor,
    surfaces: bool = True,
    lines: bool = True,
) -> Model:
    cube = Model()

    # Create the 8 points.
    ps: List[Vec3] = []
    for i in range(8):
        px = 1.0 if i & 0x01 else -1.0
        py = 1.0 if i & 0x02 else -1.0
        pz = 1.0 if i & 0x04 else -1.0
        p = px, py, pz
        ps.append(p)

    # Add the 12 lines if needed.
    if lines:
        for i in range(8):
            for shift in range(3):
                mask = 0x01 << shift
                if not i & mask:
                    j = i | mask
                    cube.add_line(ps[i], ps[j], line_color)

    # Add the 12 triangles if needed.
    if surfaces:
        cube.add_triangle(ps[0], ps[1], ps[2], surface_color)
        cube.add_triangle(ps[0], ps[1], ps[4], surface_color)
        cube.add_triangle(ps[0], ps[2], ps[4], surface_color)
        cube.add_triangle(ps[1], ps[2], ps[3], surface_color)
        cube.add_triangle(ps[1], ps[3], ps[5], surface_color)
        cube.add_triangle(ps[1], ps[4], ps[5], surface_color)
        cube.add_triangle(ps[2], ps[3], ps[6], surface_color)
        cube.add_triangle(ps[2], ps[4], ps[6], surface_color)
        cube.add_triangle(ps[3], ps[5], ps[7], surface_color)
        cube.add_triangle(ps[3], ps[6], ps[7], surface_color)
        cube.add_triangle(ps[4], ps[5], ps[6], surface_color)
        cube.add_triangle(ps[5], ps[6], ps[7], surface_color)

    return cube


def get_tetrahedron_model(surface_color: str = kDefaultSurfaceColor,
                          line_color: str = kDefaultLineColor,
                          surfaces: bool = True,
                          lines: bool = True):
    tetrahedron = Model()

    # Create the 4 points.
    p = 1.0, -1.0 / sqrt(3), -1.0 / sqrt(6)
    q = -1.0, -1.0 / sqrt(3), -1.0 / sqrt(6)
    r = 0.0, 2.0 / sqrt(3), -1.0 / sqrt(6)
    s = 0.0, 0.0, 3.0 / sqrt(6)

    # Add the 6 lines if needed.
    if lines:
        tetrahedron.add_line(p, q, line_color)
        tetrahedron.add_line(q, r, line_color)
        tetrahedron.add_line(r, p, line_color)
        tetrahedron.add_line(p, s, line_color)
        tetrahedron.add_line(q, s, line_color)
        tetrahedron.add_line(r, s, line_color)

    # Add the 4 triangles if needed.
    if surfaces:
        tetrahedron.add_triangle(p, q, r, surface_color)
        tetrahedron.add_triangle(p, q, s, surface_color)
        tetrahedron.add_triangle(q, r, s, surface_color)
        tetrahedron.add_triangle(r, p, s, surface_color)

    return tetrahedron


def get_sphere_model(
    n: int = 8,
    m: int = 16,
    surface_color: str = kDefaultSurfaceColor,
    line_color: str = kDefaultLineColor,
    surfaces: bool = True,
    latitude_lines: bool = True,
    longitude_lines: bool = True,
) -> Model:
    sphere = Model()

    # Create the n*m points and a unique north and south pole.
    p_north = 0.0, 1.0, 0.0
    p_south = 0.0, -1.0, 0.0
    ps: List[List[Vec3]] = []
    for i in range(n):
        angle_latitude = (i + 1) / (n + 1) * pi
        py = cos(angle_latitude)
        radius_xz = sqrt(1.0 - py**2)
        ps_latitude: List[Vec3] = []
        for j in range(m):
            angle_longitude = j / m * 2.0 * pi
            px = radius_xz * sin(angle_longitude)
            pz = radius_xz * cos(angle_longitude)
            p = px, py, pz
            ps_latitude.append(p)
        ps.append(ps_latitude)

    # Add lines and triangles defined by the grid.
    for i in range(n - 1):
        i_next = i + 1
        for j in range(m):
            j_next = (j + 1) % m
            p = ps[i][j]
            q = ps[i][j_next]
            r = ps[i_next][j]
            s = ps[i_next][j_next]
            if surfaces:
                sphere.add_triangle(p, q, r, surface_color)
                sphere.add_triangle(q, r, s, surface_color)
            if latitude_lines:
                sphere.add_line(p, q, line_color)
            if longitude_lines:
                sphere.add_line(p, r, line_color)

    # Add lines and triangles to connect the north and south poles.
    for j in range(m):
        j_next = (j + 1) % m
        p = ps[0][j]
        q = ps[0][j_next]
        r = ps[-1][j]
        s = ps[-1][j_next]
        if surfaces:
            sphere.add_triangle(p_north, p, q, surface_color)
            sphere.add_triangle(p_south, r, s, surface_color)
        if latitude_lines:
            sphere.add_line(r, s, line_color)
        if longitude_lines:
            sphere.add_line(p_north, p, line_color)
            sphere.add_line(p_south, r, line_color)

    return sphere


def get_coordinate_system_model(color_x="red",
                                color_y="green",
                                color_z="blue") -> Model:
    model = Model()
    origin = 0.0, 0.0, 0.0
    tip_x = 1.0, 0.0, 0.0
    tip_y = 0.0, 1.0, 0.0
    tip_z = 0.0, 0.0, 1.0
    model.add_line(origin, tip_x, color_x)
    model.add_line(origin, tip_y, color_y)
    model.add_line(origin, tip_z, color_z)
    return model
