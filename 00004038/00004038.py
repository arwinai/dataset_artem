import cadquery as cq

thickness = 10.0

hole_radius = 7.73
hole_spacing = 10.57

top_bottom_arc_radius = 12.73
side_arc_radius = 10.0

side_arc_center_x = 22.11

upper_arc_start = (-12.38, 1.78)
upper_arc_end = (-upper_arc_start[0], upper_arc_start[1])
lower_arc_start = (-upper_arc_start[0], -upper_arc_start[1])
lower_arc_end = (upper_arc_start[0], -upper_arc_start[1])

upper_arc_point = (0, hole_spacing / 2 + top_bottom_arc_radius)
lower_arc_point = (upper_arc_point[0], -upper_arc_point[1])

right_arc_point = (side_arc_center_x - side_arc_radius, 0)
left_arc_point = (-right_arc_point[0], right_arc_point[1])


solid = (
    cq.Workplane("XY")
    .moveTo(*upper_arc_start)
    .threePointArc(upper_arc_point, upper_arc_end)
    .threePointArc(right_arc_point, lower_arc_start)
    .threePointArc(lower_arc_point, lower_arc_end)
    .threePointArc(left_arc_point, upper_arc_start)
    .close()
    .extrude(thickness)
)

upper_hole_center = (0, hole_spacing / 2)
lower_hole_center = (upper_hole_center[0], -upper_hole_center[1])

solid = (
    solid.moveTo(*upper_hole_center)
    .circle(hole_radius)
    .cutThruAll()
    .moveTo(*lower_hole_center)
    .circle(hole_radius)
    .cutThruAll()
)

show_object(solid)
