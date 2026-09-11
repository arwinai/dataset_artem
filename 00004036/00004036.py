from math import cos, pi, sin

import cadquery as cq

thickness = 3.0

flower_petals_count = 9
flower_petals_radius = 8.42
flower_petals_ring_center = (0, 0.7)
flower_petals_ring_radius = 24.37
flower_petals_start_angle = 90.0
flower_base_radius = 22.0

flower = (
    cq.Workplane("XY")
    .workplane(origin=flower_petals_ring_center)
    .polarArray(
        flower_petals_ring_radius, flower_petals_start_angle, 360, flower_petals_count
    )
    .circle(flower_petals_radius)
    .extrude(thickness)
    .faces("<Z")
    .circle(flower_base_radius)
    .extrude(thickness)
)

heart_tip = (0, -17.69)
heart_cleft = (0, 11.67)
heart_arc_start = (-14.5, -3.18)
heart_arc_radius = 10.38

heart = (
    cq.Workplane("XY")
    .moveTo(*heart_tip)
    .lineTo(*heart_arc_start)
    .radiusArc(heart_cleft, heart_arc_radius)
    .close()
    .extrude(thickness)
    .mirror("YZ", union=True)
)


def create_star_sketch(
    outer_radius: float, inner_radius: float, angle: float
) -> cq.Sketch:
    angle_rad = angle * pi / 180

    points: list[tuple[float, float]] = []
    for vertex_index in range(10):
        current_angle = pi * 0.2 * vertex_index + angle_rad
        radius = outer_radius if vertex_index % 2 == 0 else inner_radius

        x = radius * cos(current_angle)
        y = radius * sin(current_angle)

        points.append((x, y))

    return cq.Sketch().polygon(points)


star_outer_radius = 13.53
star_inner_radius = 5.18

star = (
    cq.Workplane("XY")
    .placeSketch(create_star_sketch(star_outer_radius, star_inner_radius, 90))
    .extrude(thickness)
)

solid = flower.cut(heart).union(star)

show_object(solid)
