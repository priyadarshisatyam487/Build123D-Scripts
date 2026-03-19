from build123d import *
from ocp_vscode import show

# -----------------------------
# 1) Main box
# -----------------------------
with BuildPart() as part:
    Box(12, 7.982, 2.2)

result = part.part

# -----------------------------
# 2) Fillet outer vertical edges of the box
# -----------------------------
outer_vertical_edges = [
    e for e in result.edges()
    if abs(e.bounding_box().size.Z - 2.2) < 1e-3
]
result = fillet(outer_vertical_edges, 1.0)

# -----------------------------
# 3) Bottom rectangular pocket
#    Size: 10.4 x 6.382 x 0.3
# -----------------------------
bottom_z = result.bounding_box().min.Z

with BuildPart() as pocket_cut:
    with BuildSketch(Plane.XY.offset(bottom_z)):
        Rectangle(10.4, 6.382)
    extrude(amount=0.3)

pocket = pocket_cut.part

pocket_vertical_edges = [
    e for e in pocket.edges()
    if abs(e.bounding_box().size.Z - 0.3) < 1e-3
]
pocket = fillet(pocket_vertical_edges, 0.18)

result = result - pocket

# -----------------------------
# 4) Cylinder on bottom face
#    Dia: 6.52, Height: 0.3
# -----------------------------
with BuildPart() as cyl_add:
    with BuildSketch(Plane.XY.offset(bottom_z)):
        Circle(6.52 / 2)
    extrude(amount=0.3)

cylinder = cyl_add.part
result = result + cylinder

# -----------------------------
# 5) Rectangular slot
#    Size: 5.5 x 1.5 x 2.2
# -----------------------------
with BuildPart() as slot_cut:
    Box(5.5, 1.5, 2.2)

slot = slot_cut.part
slot_vertical_edges = [
    e for e in slot.edges()
    if abs(e.bounding_box().size.Z - 2.2) < 1e-3
]
slot = fillet(slot_vertical_edges, 0.5)

result = result - slot

# -----------------------------
# 6) Fillet the four vertical edges near given XY locations
# -----------------------------
target_points = [
    (0.667, 3.191),
    (-0.667, 3.191),
    (-0.667, -3.191),
    (0.667, -3.191),
]

# collect only vertical edges around the lower feature region
candidate_edges = [
    e for e in result.edges()
    if abs(e.bounding_box().size.Z - 0.3) < 1e-3
]

edges_to_fillet = []

for tx, ty in target_points:
    edge = min(
        candidate_edges,
        key=lambda e: (e.center().X - tx) ** 2 + (e.center().Y - ty) ** 2
    )
    edges_to_fillet.append(edge)
    candidate_edges.remove(edge)

result = fillet(edges_to_fillet, 0.5)

# -----------------------------
# Show final part
# -----------------------------
show(result)