# Rebuilding the panel-mount holders

From the project directory, run `python make_all.py`. The usual OOBB entry point
`python action_make_all.py` runs the same build. Use Python with PyYAML and the
OOMP v5 and OOBB v5 checkouts on its import path. The generator uses the OOBB
rounded-rectangle, nut and screw components. Put the OpenSCAD CLI and Blender on PATH. Install the
documentation dependencies with `python -m pip install -r requirements-presentation.txt`.
The holder recipe records its 7 mm corner radius explicitly for reproducible builds.

Shared libraries: [OOMP v5](https://github.com/oomlout/oomlout_oomp_version_5) and
[OOBB v5](https://github.com/oomlout/oomlout_oobb_version_5).

The build reads every `parts/*/working.yaml` in
`C:/gh/oomp_electronic_panel_mount_version_5`. If that checkout is absent, it
uses a clone in `.deps/oomp_electronic_panel_mount_version_5`. Git ignores
`.deps/`. Update the chosen checkout to build from a newer catalog revision.

- `working_oomp_populate.py` derives four entries per device and writes their
  definitions under `parts_source/`. Edit the fit and wall defaults in
  `holder_entries`.
- `working_oomp.py` materializes the selected entries under `parts/`.
- `working_scad.py` writes nominal `true.scad` and `true.stl`, plus
  `3dpr.scad` and `3dpr.stl` with OOBB print allowances for mounting holes.
- `working_presentation.py` renders both exported meshes in Blender and builds
  the three installation booklets, offline viewers and inventories. The device
  is a schematic envelope derived from the OOMP dimensions. The source catalog
  has no production mesh for the device. The cutter has a CAD-use guide in its README.
- `working_navigation.py` generates the root and part READMEs and taxonomy pages.
  Each navigation leaf includes the OOMP ID and a byte-checked STL copy. Physical
  holders use the production mesh and the cutter uses its nominal solid.
- `working_verify.py` checks the source, part and leaf IDs, navigation mesh
  hashes, local README links, manuals and hardware links. It runs at the end
  of the full build and can also be run independently before upload.

Local IDs retain the device type, manufacturer and model. The style is followed
by holder width and height in 15 mm OOBB units, then depth in mm. For the cutter
only, the grid counts describe the smallest containing OOBB envelope. The full
source device ID, including its dimensions, remains in each record.

The layout and viewer in `presentation/` are adapted from Oom Lout's OOBB v5
presentation templates and wave-drive assembly book. The logo source comes
from `oomlout_media/logos/logo_vector_unshaded`. The build uses these bundled
assets offline. The cover links to the holder repository. The device and
fastener entries link to their OOMP catalog records.
For a CAD-only rebuild, pass `run_presentation=False`. The full default build
also refreshes the documentation. Intermediate renders live in ignored `.build/`.

## Fit and orientation

The center of the front opening is the origin. X runs across the face, Y runs
up, and positive Z points into the box. To use `cutout_only`, align its small
end with the front of your block and subtract it. All holders subtract that same
stepped shape. On a 3 mm panel, only the narrow section cuts the panel. The box
retains the shoulder and continues the pocket all the way through the back.

The narrow section uses the catalog's cutout width, height and depth. Behind it,
the pocket allows 0.5 mm per side beyond the larger of the device and opening
dimensions, and 1 mm beyond the catalog depth. These are editable allowances
for the device and its clips. Confirm them on a physical fit sample.

The catalog box depth is the assembled depth. The XY-SMH box is 41 mm deep,
including its 38 mm open body and 3 mm removable rear plate. The nominal
`true.scad` and `true.stl` show the plate installed. In `3dpr.stl` both
pieces sit flat on the bed with an 8 mm gap. To print a replacement part, use
`body_3dpr.stl` or `back_plate_3dpr.stl`. All holder plates and the body have
7 mm plan corners and 1.5 mm rim radii. The clip shoulder and the CAD cutter
use the original device cutout dimensions.

Slide one M3 nut in from the outside of each side rail. Fasten the rear plate
with two M3 × 12 mm countersunk screws from the rear. The plate and body share
the same M6 and M3 through-bores. Each screw occupies the middle M3 bore on
its side. With the fasteners removed, those two bores are also clear for the
full 41 mm. The bottom-center wire opening measures 30 mm across and 30 mm up
from the lower edge, with 7 mm upper corner radii.

Four M3 through-holes flank the wire opening on 15 mm rows. Each accepts a
side-loaded nut for a future patch panel. Feed the nuts from the wire opening.
The 2.5 mm pockets leave nominal 0.25 mm retaining skins on each face of the
3 mm plate, with local overhang relief at the bore. Both sets of loading slots run parallel to the hex flats and
measure 5.50 mm nominal or 5.75 mm in print mode. Every screw and nut primitive
uses `overhang=True`. The screw illustration uses the OOMP M3 × 12 countersunk
display mesh from `oomp_hardware_screw_version_5`.

To check both delivered mesh modes for nut access, slot width, countersink
direction, screw reach and the open cable path, run
`python tests/test_rear_plate.py` with `trimesh` and `rtree` installed.

Vertical M6 centers lie at 15, 45, 75 mm and successive odd multiples of 15 mm
from the front. M3 infill uses the 7.5 mm offsets. The generator keeps holes
with enough material for the print diameter and a 1 mm wall around the pocket.
Vertical and front-to-back mounting holes can intersect.
