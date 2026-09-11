import cadquery as cq

base_width = 83.43
base_length = 95.87
base_thickness = 7.0

pentagon_circumradius = 5

pentagon = cq.Sketch().regularPolygon(pentagon_circumradius, 5, 0)
pentagon_inverted = cq.Sketch().regularPolygon(pentagon_circumradius, 5, 180)

pentagon_count_x = 4
pentagon_count_y = 8

pentagon_spacing_x = 19.0
pentagon_spacing_y = 11.0

pentagon_array_origin = (-24.26, -36.69)
pentagon_inverted_array_origin = (-33.76, -39.77)

solid = (
    cq.Workplane("XY")
    .rect(base_width, base_length)
    .extrude(base_thickness)
    .workplane(origin=pentagon_array_origin)
    .rarray(
        pentagon_spacing_x,
        pentagon_spacing_y,
        pentagon_count_x,
        pentagon_count_y,
        center=False,
    )
    .placeSketch(pentagon)
    .cutThruAll()
    .faces(">Z")
    .workplane(origin=pentagon_inverted_array_origin)
    .rarray(
        pentagon_spacing_x,
        pentagon_spacing_y,
        pentagon_count_x,
        pentagon_count_y,
        center=False,
    )
    .placeSketch(pentagon_inverted)
    .cutThruAll()
)

show_object(solid)
