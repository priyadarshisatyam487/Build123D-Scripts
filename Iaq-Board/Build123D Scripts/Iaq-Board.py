from build123d import *
from ocp_vscode import show

# --- Cuboid 1 ---
with BuildPart() as cuboid_1:
    Box(51.65399933,
        48.4,
        18.95109,
        align=(Align.CENTER, Align.CENTER, Align.MIN))
    
   # Fillet bottom edges parallel to X axis
    fillet(
        cuboid_1.faces().sort_by(Axis.Z).first
        .edges()
        .filter_by(Axis.X),
        1
    )

    # Fillet top-front edge parallel to X axis
    fillet(
        cuboid_1.faces().sort_by(Axis.Z).last
        .edges()
        .filter_by(Axis.X)
        .sort_by(Axis.Y)
        .first,
        1
    )
    # Filet top-back edge parallel to X axis
        # Fillet top-front edge parallel to X axis
    fillet(
        cuboid_1.faces().sort_by(Axis.Z).last
        .edges()
        .filter_by(Axis.X)
        .sort_by(Axis.Y)
        .last,0.5
    )

Cuboid_1 = cuboid_1.part

# --- Cuboid 2 ---
with BuildPart() as cuboid_2:
    with Locations((-21.82699965, 0.3, 3)):
        Box(
            48,
            37.20000076,
            12,
            align=(Align.MIN, Align.CENTER, Align.MIN)
        )


Cuboid_2 = cuboid_2.part


# --- Cuboid 3 ---
with BuildPart() as cuboid_3:
    with Locations((-(21.82699965 + 1.604), 0, 14.95109)):
        Box(
            49.754,
            43.6,
            2,
            align=(Align.MIN, Align.CENTER, Align.MIN)
        )

Cuboid_3 = cuboid_3.part


# --- Cuboid 4 ---
with BuildPart() as cuboid_4:
    with Locations((-21.33099965, -19.10770707, 16.95109)):
        Box(
            50,
            39.04219,
            5,
            align=(Align.MIN, Align.MIN, Align.MIN)
        )

Cuboid_4 = cuboid_4.part

# --- Triangular prism cut ---
with BuildLine(Plane.YZ) as tri_line:
    Line((-19.10770707, 18.95109), (-19.10770707, 16.95109))   # base along -Z
    Line((-19.10770707, 16.95109), (-22.57404707, 18.95109))     # hypotenuse
    Line((-22.57404707, 18.95109), (-19.10770707, 18.95109))      # height along -Y

tri_face = Face(Wire(tri_line.edges()))

with BuildPart() as triangle_cut:
    extrude(tri_face, amount=-25.82700)                  # +X
    extrude(tri_face, amount=21.330999650, mode=Mode.ADD)  # -X

Triangle_Cut = triangle_cut.part

# --- Final Result ---
Resulting_Solid = Cuboid_1 - Cuboid_2 - Cuboid_3 - Cuboid_4 - Triangle_Cut

# --- Fillet top-face edge parallel to Y at X = -21.33099965 ---
target_x = -21.33099965

top_face = Resulting_Solid.faces().sort_by(Axis.Z).last
y_edges = top_face.edges().filter_by(Axis.Y)

target_edge = min(
    y_edges,
    key=lambda e: abs(e.center().X - target_x)
)

Resulting_Solid = fillet(target_edge, 1.212)

# --- Fillet leftmost face edges ---
leftmost_face = Resulting_Solid.faces().sort_by(Axis.X).first

Resulting_Solid = fillet(
    leftmost_face.edges(),
    0.5
)

# --- Fillet edge parallel to X at (y,z) = (-22.57404707, 18.95109) ---
target_y = -22.57404707
target_z = 18.95109

x_edges = Resulting_Solid.edges().filter_by(Axis.X)

target_edge = min(
    x_edges,
    key=lambda e: abs(e.center().Y - target_y) + abs(e.center().Z - target_z)
)

Resulting_Solid = fillet(target_edge, 0.5)

# --- Fillet edge parallel to X at (y,z) = (-19.10770707, 16.95109) ---
target_y = -19.10770707
target_z = 16.95109

x_edges = Resulting_Solid.edges().filter_by(Axis.X)

target_edge = min(
    x_edges,
    key=lambda e: abs(e.center().Y - target_y) + abs(e.center().Z - target_z)
)

Resulting_Solid = fillet(target_edge, 0.3)

# --- fillet on edges parallel to Z on the rightmost face at Y = ±19.521095 ---
target_y_vals = [-19.521095]

right_face = Resulting_Solid.faces().sort_by(Axis.X).last
z_edges = right_face.edges().filter_by(Axis.Z)

edges_to_fillet = []
for ty in target_y_vals:
    edge = min(z_edges, key=lambda e: abs(e.center().Y - ty))
    edges_to_fillet.append(edge)

Resulting_Solid = fillet(edges_to_fillet, 0.5)

# --- fillet on edges parallel to Z on the rightmost face at Y = ±19.521095 ---
target_y_vals = [18]

right_face = Resulting_Solid.faces().sort_by(Axis.X).last
z_edges = right_face.edges().filter_by(Axis.Z)

edges_to_fillet = []
for ty in target_y_vals:
    edge = min(z_edges, key=lambda e: abs(e.center().Y - ty))
    edges_to_fillet.append(edge)

Resulting_Solid = fillet(edges_to_fillet, 0.5)

# --- fillet on edges parallel to Z on the rightmost face at Y = ±19.521095 ---
target_y_vals = [20]

right_face = Resulting_Solid.faces().sort_by(Axis.X).last
z_edges = right_face.edges().filter_by(Axis.Z)

edges_to_fillet = []
for ty in target_y_vals:
    edge = min(z_edges, key=lambda e: abs(e.center().Y - ty))
    edges_to_fillet.append(edge)

Resulting_Solid = fillet(edges_to_fillet, 0.5)

# --- 0.5 mm fillet on edge parallel to Y on rightmost face at Z = 5 ---
target_z = 5

right_face = Resulting_Solid.faces().sort_by(Axis.X).last
y_edges = right_face.edges().filter_by(Axis.Y)

target_edge = min(
    y_edges,
    key=lambda e: abs(e.center().Z - target_z)
)

Resulting_Solid = fillet(target_edge, 0.5)

# --- 0.5 mm fillet on edge parallel to Y on rightmost face at Z = 5 ---
target_z = 25

right_face = Resulting_Solid.faces().sort_by(Axis.X).last
y_edges = right_face.edges().filter_by(Axis.Y)

target_edge = min(
    y_edges,
    key=lambda e: abs(e.center().Z - target_z)
)

Resulting_Solid = fillet(target_edge, 0.5)

# --- Back-face slot cut ---
with BuildPart() as slot_cut:
    with BuildSketch(Plane.XZ.offset(-18.9)):
        with Locations((-12.723, 5.10109)):
            SlotCenterToCenter(7.9, 3)

    extrude(amount=-5.3)

Slot_Cut = slot_cut.part
Resulting_Solid = Resulting_Solid-Slot_Cut

# --- Select back face and fillet the semicircular slot edge by 1.5 ---
back_face = (
    Resulting_Solid.faces()
    .filter_by(GeomType.PLANE)
    .sort_by(Axis.Y)
    .last
)

semi_edges = [
    e for e in back_face.edges()
    if e.length < 5
]

target_edge = min(
    semi_edges,
    key=lambda e: abs(e.center().X - (-12.723)) + abs(e.center().Z - 5.10109)
)

Resulting_Solid = fillet(target_edge, 1.5)

# --- Drafted rectangular cut on the backmost face with 5.3 mm depth ---
back_face = min(
    Resulting_Solid.faces().filter_by(GeomType.PLANE),
    key=lambda f: f.center().Y
)

back_y = back_face.center().Y
depth = 5.3

with BuildPart() as drafted_cut:
    # Outer profile on the back face
    with BuildSketch(Plane.XZ.offset(back_y)):
        with Locations((14.82700, 6.35109)):
            Rectangle(16.5, 10)

    # Inner profile 5.3 mm inward
    with BuildSketch(Plane.XZ.offset(back_y + depth)):
        with Locations((14.82700, 6.35109)):
            Rectangle(13, 6.5)

    loft()

Drafted_Cut = drafted_cut.part
Resulting_Solid = Resulting_Solid - Drafted_Cut

# --- First inclined rectangular cut solid only ---
with BuildPart() as first_cut:
    with BuildSketch(Plane.XY) as cut_sketch:
        Rectangle(8, 2.5)

    extrude(amount=3)

    # fillet the vertical edges
    fillet(
        first_cut.edges().filter_by(Axis.Z),
        1
    )

First_Cut = first_cut.part

# rotate and move it into position
First_Cut = Pos(-17.16677, -14.01138, 0) * Rot(0, 0, 45) * First_Cut

# --- Create first row pattern along Y ---
cuts = []

for i in range(5):
    cut = Pos(-17.16677, -14.01138 + i * 7.02725, 0) * Rot(0, 0, 45) * first_cut.part
    cuts.append(cut)

# subtract all cuts in this row
for c in cuts:
    Resulting_Solid = Resulting_Solid - c

    # --- Create full 5x5 pattern ---
cuts = []

for col in range(5):
    for row in range(5):
        cut = (
            Pos(-17.16677 + col * 9.37698, -14.01138 + row * 7.02725, 0)
            * Rot(0, 0, 45)
            * first_cut.part
        )
        cuts.append(cut)

# subtract all cuts
for c in cuts:
    Resulting_Solid = Resulting_Solid - c

# subtract from main body
Resulting_Solid = Resulting_Solid - First_Cut

show(Resulting_Solid)

