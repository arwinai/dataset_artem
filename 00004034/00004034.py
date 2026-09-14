from math import cos, radians, sin

import cadquery as cq

part1_outer_radius = 16.46
part1_inner_radius = 13.35

part1_height = 74.96
part1_branch_extension = 20.90

part2_width = 15.88
part2_height = 25.68
part2_middle_depth = 22.86

part2_cylinder_radius = 0.76
part2_cylinder_count = 5
part2_cylinder_spacing_angle = 15
part2_cylinder_start_angle = 60

part2_extension_width = 15.88
part2_extension_height = 20.18
part2_extension_length = 28.58
part2_extension_chamfer_long = 6.35
part2_extension_chamfer_short = 3.05
part2_extension_tip_chamfer = 5.08

part2_lug_straight_length = 14.29
part2_lug_thickness = 3.18
part2_lug_spacing = 3.17

part2_lug_chamfer = 0.64
part2_lug_hole_radius = 2.54

part3_length = 50.80

part4_outer_radius = 13.28
part4_inner_radius = 10.06
part4_length = 50.80

part1_branch_length = part1_outer_radius + part1_branch_extension
part1_branch_center_z = part1_height / 2
part1_branch_position = (0, 0, part1_branch_center_z)

part1 = (
    cq.Workplane("XY")
    .circle(part1_outer_radius)
    .extrude(part1_height)
    .union(
        cq.Workplane("XZ", part1_branch_position)
        .circle(part1_outer_radius)
        .extrude(part1_branch_length)
    )
)

part1_cutter = (
    cq.Workplane("XY")
    .circle(part1_inner_radius)
    .extrude(part1_height)
    .union(
        cq.Workplane("XZ", part1_branch_position)
        .circle(part1_inner_radius)
        .extrude(part1_branch_length)
    )
)

part1 = part1.cut(part1_cutter)


part2_origin = (0, -part1_branch_length, part1_branch_center_z)

part2 = (
    cq.Workplane("XZ", part2_origin)
    .rect(part2_width, part2_height)
    .extrude(-part2_middle_depth)
    .cut(
        cq.Workplane("XZ", part2_origin)
        .circle(part2_height / 2)
        .circle(part2_height)
        .extrude(-part2_middle_depth)
    )
)

part2_cylinder_centers: list[tuple[float, float]] = []

for i in range(part2_cylinder_count):
    angle = radians(part2_cylinder_start_angle + i * part2_cylinder_spacing_angle)
    x = part2_height / 2 * cos(angle)
    y = part2_height / 2 * sin(angle)
    part2_cylinder_centers.append((x, y))
    part2_cylinder_centers.append((x, -y))

part2_cylinders = (
    cq.Workplane("XZ", part2_origin)
    .pushPoints(part2_cylinder_centers)
    .circle(part2_cylinder_radius)
    .extrude(-part2_middle_depth)
)

part2 = part2.union(part2_cylinders)

part2_extension_origin = (
    0,
    -part1_branch_length + part2_middle_depth,
    part1_branch_center_z,
)

part2_extension = (
    cq.Workplane("XZ", part2_extension_origin)
    .rect(part2_extension_width, part2_extension_height)
    .extrude(-part2_extension_length)
    .faces("<Z")
    .edges("|Y")
    .chamfer(part2_extension_chamfer_long, part2_extension_chamfer_short)
    .faces(">Z")
    .edges("|Y")
    .chamfer(part2_extension_chamfer_short, part2_extension_chamfer_long)
    .faces(">Y")
    .chamfer(part2_extension_tip_chamfer)
)

part2 = part2.union(part2_extension)

part2_lug_width = part2_extension_width
part2_lug_half_width = part2_lug_width / 2
part2_lug_total_length = part2_lug_straight_length + part2_lug_half_width

part2_lug = (
    cq.Workplane("XY", part2_origin)
    .moveTo(-part2_lug_half_width, 0)
    .lineTo(-part2_lug_half_width, -part2_lug_straight_length)
    .threePointArc(
        (0, -part2_lug_total_length),
        (part2_lug_half_width, -part2_lug_straight_length),
    )
    .lineTo(part2_lug_half_width, 0)
    .close()
    .extrude(part2_lug_thickness / 2, both=True)
)

part2_lug_excluded_edges = set(part2_lug.faces(">Y").edges())

part2_lug = (
    part2_lug.edges()
    .filter(lambda e: e not in part2_lug_excluded_edges)
    .chamfer(part2_lug_chamfer)
    .faces(">Z")
    .moveTo(0, -part2_lug_straight_length)
    .circle(part2_lug_hole_radius)
    .cutThruAll()
)

part2_lug_pitch = part2_lug_thickness + part2_lug_spacing

for z_offset in (0, part2_lug_pitch, -part2_lug_pitch):
    part2 = part2.union(part2_lug.translate((0, 0, z_offset)))

part3_origin = part2_origin

part3 = (
    cq.Workplane("XZ", part3_origin)
    .circle(part1_outer_radius)
    .extrude(-part3_length)
    .circle(part1_inner_radius)
    .cutThruAll()
)


part4 = (
    cq.Workplane(
        "XZ", (0, -part1_branch_length + part2_middle_depth, part1_branch_center_z)
    )
    .circle(part4_outer_radius)
    .extrude(-part4_length)
    .circle(part4_inner_radius)
    .cutThruAll()
)

solid = part1.union(part2).union(part3).union(part4)

show_object(solid)
