from build123d import *
from ocp_vscode import show

# --- Cuboid 1 ---
with BuildPart() as cuboid_1:
    Box(
        5.60006, 28.19529, 1.8,
        align=(Align.CENTER, Align.CENTER, Align.CENTER)
    )

Cuboid_1 = cuboid_1.part


# --- Cylinder to subtract ---
with BuildPart() as cyl_cut:
    with Locations((2.80003, -5.59762, 0)):
        Cylinder(
            radius=2,      # 4 mm diameter
            height=1.8,    # pass fully through the cuboid
            align=(Align.CENTER, Align.CENTER, Align.CENTER)
        )

Cylinder_Cut = cyl_cut.part


# --- Subtract cylinder from cuboid ---
Resulting_Solid = Cuboid_1 - Cylinder_Cut

# --- Fillet all vertical edges ---
vertical_edges = Resulting_Solid.edges().filter_by(Axis.Z)

Resulting_Solid = fillet(vertical_edges, 1)

# --- Cuboid 2 ---
with BuildPart() as cuboid_2:
    with Locations((11.00015, 3.78204, 0)):
        Box(
            16.4003, 4.63114, 1.8,
            align=(Align.CENTER, Align.CENTER, Align.CENTER)
        )

Cuboid_2 = cuboid_2.part


# --- Add cuboid2 to the existing solid ---
Resulting_Solid = Resulting_Solid + Cuboid_2

# --- Cuboid 3 ---
with BuildPart() as cuboid_3:
    Box(
        5.60006, 28.19529, 1.8,
        align=(Align.CENTER, Align.CENTER, Align.CENTER)
    )

    # Fillet all vertical edges
    fillet(
        cuboid_3.edges().filter_by(Axis.Z),
        1
    )

Cuboid_3 = cuboid_3.part.located(Location((22.00031, 0, 0)))


# --- Add cuboid3 to the existing solid ---
Resulting_Solid = Resulting_Solid + Cuboid_3

# --- Two solid cylinders going in negative Z direction ---
with BuildPart() as cyl_features:
    with Locations(
        (-0.67310, -12.71549, -1.9),
        (-0.80003, 11.09765, -1.9)
    ):
        Cylinder(
            radius=0.95,   # 1.9 mm diameter
            height=3,
            align=(Align.CENTER, Align.CENTER, Align.CENTER)
        )

Cylinder_Features = cyl_features.part

# --- Add cylinders to the existing solid ---
Resulting_Solid = Resulting_Solid + Cylinder_Features

# --- Four cylinders 3.5mm ---
with BuildPart() as cyl_4:
    with Locations(
        (0, -11.17477, 0),
        (0, 10.82523, 0),
        (22.00031, -11.17477, 0),
        (22.00031, 10.82523, 0)
    ):
        Cylinder(
            radius=1.75,   # 3.5 mm diameter
            height=7.2,
            align=(Align.CENTER, Align.CENTER, Align.MIN)
        )

Cylinders_4 = cyl_4.part

# --- Four cylinders 2mm  ---
with BuildPart() as cyl_5:
    with Locations(
        (0, -11.17477, 7.2),
        (0, 10.82523, 7.2),
        (22.00031, -11.17477, 7.2),
        (22.00031, 10.82523, 7.2)
    ):
        Cylinder(
            radius=1,   # 2 mm diameter
            height=2,
            align=(Align.CENTER, Align.CENTER, Align.MIN)
        )

Cylinders_5 = cyl_5.part

# --- Add to existing solid ---
Resulting_Solid = Resulting_Solid + Cylinders_4 + Cylinders_5

show(Resulting_Solid)