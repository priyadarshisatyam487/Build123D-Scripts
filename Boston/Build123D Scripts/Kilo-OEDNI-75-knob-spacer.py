from build123d import *
from ocp_vscode import show

# --- Main cylinder ---
with BuildPart() as main_part:
    Cylinder(
        radius=5.8 / 2,
        height=4.2,
        align=(Align.CENTER, Align.CENTER, Align.MIN)
    )

    # Chamfer top circular edge
    chamfer(
        main_part.faces().sort_by(Axis.Z).last.edges(),
        0.5
    )

    # Chamfer bottom circular edge
    chamfer(
        main_part.faces().sort_by(Axis.Z).first.edges(),
        0.5
    )

Main_Body = main_part.part


# --- Cutting block ---
with BuildPart() as cut_block:
    with Locations((0, -2.3, 2.1)):
        Box(
            5.2, 2, 4.2,
            align=(Align.CENTER, Align.CENTER, Align.CENTER)
        )

Cut_Block = cut_block.part


# --- Final result ---
Resulting_Solid = Main_Body - Cut_Block

show(Resulting_Solid)